using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Security.Cryptography;
using System.Text;
using SmartAuditERP.Class.Security;
using SmartAuditUpdater;
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
        // مسحة التحقق: التجزئة الفارغة كانت تقبل أي كلمة مرور (GetBytes(0) => FixedTimeEquals(فارغ,فارغ)=true)
        [InlineData("PBKDF2$100000$AAAA$")]
        [InlineData("PBKDF2$1$AAAA$")]
        [InlineData("PBKDF2$0$AAAA$AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA=")]  // تكرارات < 1
        [InlineData("PBKDF2$999999999$AAAA$AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA=")] // تكرارات مرضية (DoS)
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

    // مسحة التحقق — اختبارات ManifestSignatureVerifier (تحصين P1-020):
    // حارس اجتياز المسار كان يقارن بالبادئة وحدها فيمرر مجلداً شقيقاً يشترك
    // في البادئة، وSplit(' ') كان يرفض المسارات ذات الفراغات.
    public class ManifestSignatureVerifierTests : IDisposable
    {
        private readonly string _root;
        private readonly string _sibling;
        private readonly string _pubKey;
        private readonly string _privKey;

        public ManifestSignatureVerifierTests()
        {
            _root = Path.Combine(Path.GetTempPath(), "mft-" + Guid.NewGuid().ToString("N"));
            _sibling = _root + "-evil";
            Directory.CreateDirectory(_root);
            Directory.CreateDirectory(_sibling);
            using (var rsa = RSA.Create())
            {
                _pubKey = rsa.ToXmlString(false);
                _privKey = rsa.ToXmlString(true);
            }
        }

        private string WritePackage(params string[] files)
        {
            var entries = new List<string>();
            foreach (var rel in files)
            {
                string full = Path.Combine(_root, rel);
                Directory.CreateDirectory(Path.GetDirectoryName(full));
                File.WriteAllText(full, "content of " + rel);
                entries.Add(ManifestSignatureVerifier.BuildManifestEntry(_root, rel));
            }
            string payload = string.Join("\n", entries) + "\n";
            string sig;
            using (var rsa = new RSACryptoServiceProvider())
            {
                rsa.FromXmlString(_privKey);
                byte[] sign = rsa.SignData(
                    Encoding.UTF8.GetBytes(payload),
                    HashAlgorithmName.SHA256, RSASignaturePadding.Pkcs1);
                sig = "SIG " + Convert.ToBase64String(sign);
            }
            string manifest = Path.Combine(_root, "manifest.txt");
            File.WriteAllText(manifest, payload + sig, new UTF8Encoding(false));
            return manifest;
        }

        [Fact]
        public void Verify_ValidManifestPasses_IncludingPathsWithSpaces()
        {
            string manifest = WritePackage("update.exe", "sub dir/new plugin.dll");
            Assert.True(ManifestSignatureVerifier.VerifyManifest(manifest, _root, _pubKey));
        }

        [Fact]
        public void Verify_SiblingPrefixDirectoryIsRejected()
        {
            // الملف داخل مجلد شقيق يشترك في البادئة (root vs root-evil):
            // المقارنة بالبادئة وحدها كانت تمرره — يجب رفضه الآن.
            // التجزئة هنا صحيحة فعلاً للملف الشرير: الرفض الوحيد الممكن هو حارس المسار.
            WritePackage("update.exe");
            File.WriteAllText(Path.Combine(_sibling, "evil.exe"), "malicious");

            string evilHex = ManifestSignatureVerifier
                .BuildManifestEntry(_sibling, "evil.exe")
                .Split(' ')[1];

            // مانيفست موقّع يذكر مساراً يهرب بالـ .. إلى المجلد الشقيق
            string payload = ManifestSignatureVerifier.BuildManifestEntry(_root, "update.exe") + "\n" +
                             "SHA256 " + evilHex + " ../" + Path.GetFileName(_sibling) + "/evil.exe\n";
            string sig;
            using (var rsa = new RSACryptoServiceProvider())
            {
                rsa.FromXmlString(_privKey);
                sig = "SIG " + Convert.ToBase64String(rsa.SignData(
                    Encoding.UTF8.GetBytes(payload),
                    HashAlgorithmName.SHA256, RSASignaturePadding.Pkcs1));
            }
            string m2 = Path.Combine(_root, "manifest-evil.txt");
            File.WriteAllText(m2, payload + sig, new UTF8Encoding(false));

            Assert.False(ManifestSignatureVerifier.VerifyManifest(m2, _root, _pubKey));
        }

        [Fact]
        public void Verify_TamperedFileFails()
        {
            string manifest = WritePackage("update.exe");
            File.WriteAllText(Path.Combine(_root, "update.exe"), "tampered");
            Assert.False(ManifestSignatureVerifier.VerifyManifest(manifest, _root, _pubKey));
        }

        [Fact]
        public void Verify_TamperedManifestFails()
        {
            string manifest = WritePackage("update.exe");
            string text = File.ReadAllText(manifest);
            File.WriteAllText(manifest, text.Replace("update.exe", "other.exe"));
            Assert.False(ManifestSignatureVerifier.VerifyManifest(manifest, _root, _pubKey));
        }

        public void Dispose()
        {
            try { Directory.Delete(_root, true); } catch { }
            try { Directory.Delete(_sibling, true); } catch { }
        }
    }
}
