using System;
using SmartAuditERP.Class.Security;
using Xunit;

namespace SmartAuditERP.SecurityTests
{
    // P1-005 fix: اختبارات Stage1 — PasswordHasher (P1-008/009/010)
    public class PasswordHasherTests
    {
        [Fact]
        public void Hash_ProducesVerifyableSelfDescribingFormat()
        {
            string hash = PasswordHasher.Hash("auditor2021");

            Assert.StartsWith("PBKDF2$100000$", hash);
            Assert.Equal(4, hash.Split('$').Length);
            Assert.True(PasswordHasher.Verify("auditor2021", hash));
        }

        [Fact]
        public void Hash_SamePasswordProducesDifferentHashes_Salted()
        {
            string h1 = PasswordHasher.Hash("same-password");
            string h2 = PasswordHasher.Hash("same-password");

            Assert.NotEqual(h1, h2); // ملح عشوائي لكل عملية
            Assert.True(PasswordHasher.Verify("same-password", h1));
            Assert.True(PasswordHasher.Verify("same-password", h2));
        }

        [Theory]
        [InlineData("")]
        [InlineData(" ")]
        [InlineData(null)]
        [InlineData("PBKDF2$99999$notbase64$$$")]
        [InlineData("garbage")]
        [InlineData("PBKDF2$100000$AAAA$AAAA")]
        public void Verify_FailClosed_OnMissingCorruptOrUnknownStored(string stored)
        {
            // fail-closed: أي قيمة مخزنة غير صالحة = رفض
            Assert.False(PasswordHasher.Verify("whatever", stored));
        }

        [Fact]
        public void Verify_WrongPasswordFails()
        {
            string hash = PasswordHasher.Hash("correct-horse");
            Assert.False(PasswordHasher.Verify("battery-staple", hash));
        }

        [Fact]
        public void NeedsMigration_TrueForLegacyOrMissing_FalseForHash()
        {
            Assert.True(PasswordHasher.NeedsMigration(null));
            Assert.True(PasswordHasher.NeedsMigration(""));
            Assert.True(PasswordHasher.NeedsMigration("plaintext-old"));
            Assert.False(PasswordHasher.NeedsMigration(PasswordHasher.Hash("x")));
        }

        [Fact]
        public void Hash_EmptyPasswordThrows()
        {
            Assert.Throws<ArgumentException>(() => PasswordHasher.Hash(""));
        }
    }

    // P1-005 fix: اختبارات Stage1 — SqlBatchSplitter (P1-029)
    public class SqlBatchSplitterTests
    {
        [Fact]
        public void Split_SplitsOnlyOnRealGoLines()
        {
            string script =
                "CREATE TABLE t1 (id int)\r\nGO\r\n" +
                "INSERT INTO t1 VALUES (1)\r\nGO\r\n" +
                "SELECT * FROM t1";

            var batches = SqlBatchSplitter.Split(script);

            Assert.Equal(3, batches.Count);
        }

        [Fact]
        public void Split_DoesNotBreakOnGoInsideWordsOrStrings()
        {
            // "GO" داخل كلمة/نص لا يفصل — كانت المشكلة الموثقة في P1-029
            string script =
                "SELECT 'GOLDEN GATE' AS g, GOLDEN AS word\r\nGO\r\n" +
                "SELECT 2";

            var batches = SqlBatchSplitter.Split(script);

            Assert.Single(batches.FindAll(b => b.Contains("GOLDEN")));
            Assert.Equal(2, batches.Count);
        }

        [Theory]
        [InlineData("go")]
        [InlineData("Go")]
        [InlineData("  GO  ")]
        [InlineData("\tGO\t")]
        [InlineData("GO 5")]
        public void Split_AcceptsCaseAndWhitespaceVariants(string goLine)
        {
            string script = "SELECT 1\r\n" + goLine + "\r\nSELECT 2";
            Assert.Equal(2, SqlBatchSplitter.Split(script).Count);
        }

        [Fact]
        public void Split_EmptyAndWhitespaceOnlyBatchesAreDropped()
        {
            string script = "GO\r\n\r\nGO\r\n   \r\nGO";
            Assert.Empty(SqlBatchSplitter.Split(script));
        }

        [Fact]
        public void Split_NullOrEmptyReturnsEmpty()
        {
            Assert.Empty(SqlBatchSplitter.Split(null));
            Assert.Empty(SqlBatchSplitter.Split(""));
        }
    }

    // P1-005 fix: اختبارات Stage1 — PermissionGate (P1-012)
    public class PermissionGateTests
    {
        [Fact]
        public void Decide_FailClosed_QueryFailed()
        {
            Assert.Equal(PermissionGate.Decision.Deny,
                PermissionGate.Decide(querySucceeded: false, permissionRowExists: true, permissionValue: true));
        }

        [Fact]
        public void Decide_FailClosed_RowMissing()
        {
            Assert.Equal(PermissionGate.Decision.Deny,
                PermissionGate.Decide(querySucceeded: true, permissionRowExists: false, permissionValue: true));
        }

        [Fact]
        public void Decide_AllowOnlyWithRowAndValue()
        {
            Assert.Equal(PermissionGate.Decision.Allow,
                PermissionGate.Decide(querySucceeded: true, permissionRowExists: true, permissionValue: true));
            Assert.Equal(PermissionGate.Decision.Deny,
                PermissionGate.Decide(querySucceeded: true, permissionRowExists: true, permissionValue: false));
        }

        [Fact]
        public void LogDeny_NeverThrows()
        {
            // حتى مع مدخلات فارغة — التسجيل لا يعطل قرار المنع
            PermissionGate.LogDeny(null, null, null);
            PermissionGate.LogDeny("user", "key", "reason");
        }
    }
}
