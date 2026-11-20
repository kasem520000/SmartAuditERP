using System.Data;
using System.Data.SqlClient;
using Microsoft.VisualBasic.CompilerServices;

namespace SmartAuditERP
{

	public class Treasury
	{
		public int ID { get; set; }

		public string Name { get; set; }

		public string AccCode { get; set; }

		public string City { get; set; }

		public string Country { get; set; }

		public string Region { get; set; }

		public Treasury(int Id)
		{
			this.Name = "";
			this.AccCode = "1211001";
			this.City = "";
			this.Country = "";
			this.Region = "";
			if (Id > -1)
			{
				this.ID = Id;
				SqlDataAdapter sqlDataAdapter;
				sqlDataAdapter = new SqlDataAdapter(selectConnection: MainClass.ConnObj(), selectCommandText: "select Acc_Code,name from Stocks where  id=" + Conversions.ToString(Id));
				DataTable dataTable;
				dataTable = new DataTable();
				sqlDataAdapter.Fill(dataTable);
				if (dataTable.Rows.Count > 0)
				{
					this.Name = Conversions.ToString(dataTable.Rows[0]["name"]);
					// Repair R-040 (audit finding P3-008): same as Bank - the treasury's own Acc_Code
					// is selected above; prefer that stored link over a non-unique name search,
					// keeping the name fallback for unlinked legacy rows.
					object storedAcc;
					storedAcc = dataTable.Rows[0]["Acc_Code"];
					this.AccCode = (storedAcc != DBNull.Value && !string.IsNullOrWhiteSpace(Conversions.ToString(storedAcc)))
						? Conversions.ToString(storedAcc)
						: Common.GetAccountCode(this.Name);
				}
			}
		}
	}
}