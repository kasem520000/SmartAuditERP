using System.Collections.Generic;
using System.Text;

namespace SmartAuditERP
{
    // Repair R-020 (audit finding P1-029): upgrade/setup scripts were divided with the textual
    // String.Split("GO"), which cuts on EVERY occurrence of the letters - inside comments (--GO),
    // inside string literals (PRINT N'GO'), inside bracketed names, and even inside unrelated words
    // such as CATEGORY or MONGO - producing broken batches. This splitter follows the actual T-SQL
    // batch rule instead: a batch separator is a line whose ONLY content (besides surrounding
    // whitespace and an optional repeat count) is GO, written while NOT inside a string, delimited
    // identifier, line comment or block comment. Behaviour notes:
    //   * '' inside a single-quoted literal is handled as an escaped quote;
    //   * /* */ blocks nest, like T-SQL itself;
    //   * "GO n" repeat counts are accepted syntactically but the batch is emitted once (the old
    //     splitter had no repeat support either); executing repeats is documented residual work.
    // The result for every well-formed script that the old splitter happened to survive is the same
    // set of batches; scripts containing GO-like text now survive too.
    public static class SqlBatchSplitter
    {
        public static List<string> SplitBatches(string script)
        {
            var batches = new List<string>();
            if (string.IsNullOrWhiteSpace(script))
                return batches;

            var current = new StringBuilder();

            bool inSingleQuote = false;
            bool inDoubleQuote = false;
            bool inBracket = false;
            int blockCommentDepth = 0;

            foreach (string rawLine in script.Split('\n'))
            {
                string line = rawLine.EndsWith("\r")
                    ? rawLine.Substring(0, rawLine.Length - 1)
                    : rawLine;

                bool lineStartedExposed =
                    !inSingleQuote && !inDoubleQuote && !inBracket && blockCommentDepth == 0;

                if (lineStartedExposed && IsGoLine(line))
                {
                    EmitBatch(batches, current);
                    continue;                       // the delimiter line itself is not content
                }

                current.Append(line);
                current.Append('\n');

                ScanLineState(line, ref inSingleQuote, ref inDoubleQuote,
                              ref inBracket, ref blockCommentDepth);
            }

            EmitBatch(batches, current);
            return batches;
        }

        private static void EmitBatch(List<string> batches, StringBuilder current)
        {
            string text = current.ToString().Trim('\n', '\r', ' ', '\t');
            current.Clear();
            if (text.Length > 0)
                batches.Add(text);
        }

        private static bool IsGoLine(string line)
        {
            string trimmed = line.Trim(' ', '\t');
            if (trimmed.Length < 2)
                return false;
            if (!string.Equals(trimmed.Substring(0, 2), "GO",
                               System.StringComparison.OrdinalIgnoreCase))
                return false;
            string rest = trimmed.Substring(2).Trim(' ', '\t');
            if (rest.Length == 0)
                return true;
            int n;                                  // tolerate "GO 5" without honouring the count
            return int.TryParse(rest, out n) && n >= 0;
        }

        private static void ScanLineState(string line, ref bool inSingleQuote,
                                          ref bool inDoubleQuote, ref bool inBracket,
                                          ref int blockCommentDepth)
        {
            bool inLineComment = false;
            int i = 0;
            while (i < line.Length)
            {
                char c = line[i];
                char next = i + 1 < line.Length ? line[i + 1] : '\0';

                if (inLineComment)
                    break;                          // the rest of this line cannot change state

                if (blockCommentDepth > 0)
                {
                    if (c == '*' && next == '/')
                    {
                        blockCommentDepth--;
                        i += 2;
                        continue;
                    }
                    if (c == '/' && next == '*')
                    {
                        blockCommentDepth++;        // T-SQL block comments nest
                        i += 2;
                        continue;
                    }
                    i++;
                    continue;
                }

                if (inSingleQuote)
                {
                    if (c == '\'')
                    {
                        if (next == '\'')           // '' escape stays inside the literal
                            i += 2;
                        else
                        {
                            inSingleQuote = false;
                            i++;
                        }
                        continue;
                    }
                    i++;
                    continue;
                }

                if (inDoubleQuote)
                {
                    if (c == '"')
                        inDoubleQuote = false;
                    i++;
                    continue;
                }

                if (inBracket)
                {
                    if (c == ']')
                        inBracket = false;
                    i++;
                    continue;
                }

                if (c == '-' && next == '-')
                {
                    inLineComment = true;
                    break;
                }
                if (c == '/' && next == '*')
                {
                    blockCommentDepth++;
                    i += 2;
                    continue;
                }
                if (c == '\'')
                {
                    inSingleQuote = true;
                    i++;
                    continue;
                }
                if (c == '"')
                {
                    inDoubleQuote = true;
                    i++;
                    continue;
                }
                if (c == '[')
                {
                    inBracket = true;
                    i++;
                    continue;
                }
                i++;
            }
        }
    }
}
