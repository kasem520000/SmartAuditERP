namespace SmartAuditERP
{

        public class StartupData
        {
                public bool Remember { get; set; }

                public string ConnType { get; set; }

                public string Server { get; set; }

                public string DatabaseName { get; set; }

                public string Branch { get; set; }

                public string UserName { get; set; }

                public string Password { get; set; }

                public string Language { get; set; }

                public string ServerUserName { get; set; }

                public string ServerPassword { get; set; }

                // P2-012 fix: سياسة قناة SQL Server الاختيارية — الغياب = الافتراضي
                // المتوافق (بلا تشفير). راجع MainClass.SqlEncrypt.
                public bool? SqlEncrypt { get; set; }

                public bool? SqlTrustServerCertificate { get; set; }

                public StartupData()
                {
                        this.Remember = false;
                        this.ConnType = "";
                        this.Server = "";
                        this.DatabaseName = "";
                        this.Branch = "";
                        this.UserName = "";
                        this.Password = "";
                        this.Language = "";
                        this.ServerUserName = "";
                        this.ServerPassword = "";
                }
        }
}