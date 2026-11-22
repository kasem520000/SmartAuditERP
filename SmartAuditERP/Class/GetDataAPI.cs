using System.Net.Http;
using System.Threading.Tasks;

namespace SmartAuditERP
{

        public class GetDataAPI
        {
                public async Task<string> GetItems()
                {
                        HttpResponseMessage httpResponseMessage;
                        // FIX NEW-012 (D2-N5): استخدام HTTPS بدل HTTP المكشوف
                        httpResponseMessage = await new HttpClient().GetAsync("https://update.auditorerp.cloud/CashierApp/CashierApp.asmx/GetItems");
                        string result;
                        result = "";
                        if (httpResponseMessage.IsSuccessStatusCode)
                        {
                                result = await httpResponseMessage.Content.ReadAsStringAsync();
                        }
                        return result;
                }
        }
}