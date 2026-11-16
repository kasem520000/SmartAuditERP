using System.Text;

namespace SmartAuditERP
{
    public static class SecureVault
    {
        // GitHub User: AlbaraaQ
        private static readonly byte[] _ghUser =
        {
            0x41, 0x6C, 0x62, 0x61,
            0x72, 0x61, 0x61, 0x51
        };

        // GitHub Repo: MyApp-Updates
        private static readonly byte[] _ghRepo =
{
    0x75, 0x70, 0x64, 0x61, 0x74, 0x65, 0x5F,   // update_
    0x53, 0x6D, 0x61, 0x72, 0x74, 0x41, 0x75,   // SmartAu
    0x64, 0x69, 0x74, 0x45, 0x52, 0x50            // ditERP
};

        public static string GetGitHubUser()
        {
            return Encoding.ASCII.GetString(_ghUser);
        }

        public static string GetGitHubRepo()
        {
            return Encoding.ASCII.GetString(_ghRepo);
        }
    }
}