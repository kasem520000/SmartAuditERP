using System;
using System.Collections.Generic;
using System.IO;
using System.Net.Http;
using System.Text;
using System.Threading.Tasks;
using Newtonsoft.Json;

namespace SmartAuditERP
{
    public class SupportTicketApiClient
    {
        #region Fields

        private readonly HttpClient _httpClient;
        private readonly string _apiBaseUrl;

        #endregion

        #region Constructor

        public SupportTicketApiClient(string apiBaseUrl)
        {
            _apiBaseUrl = apiBaseUrl.TrimEnd('/');
            _httpClient = new HttpClient
            {
                Timeout = TimeSpan.FromSeconds(30)
            };
        }

        #endregion

        #region Public Methods

        public async Task<TicketResponse> CreateTicketAsync(
            string customerName,
            string customerEmail,
            string customerPhone,
            string subject,
            string description,
            string priority,
            string category,
            string ticketType,
            int branch,
            List<string> attachments)
        {
            try
            {
                var attachmentDtos = new List<TicketAttachmentDto>();

                if (attachments != null)
                {
                    foreach (string filePath in attachments)
                    {
                        string fileContent =
                            Convert.ToBase64String(File.ReadAllBytes(filePath));

                        attachmentDtos.Add(new TicketAttachmentDto
                        {
                            FileName = Path.GetFileName(filePath),
                            FileType = Path.GetExtension(filePath).Replace(".", ""),
                            FileContent = fileContent
                        });
                    }
                }

                var dto = new CreateTicketDto
                {
                    CustomerName = customerName,
                    CustomerEmail = customerEmail,
                    CustomerPhone = customerPhone,
                    Subject = subject,
                    Description = description,
                    Priority = priority,
                    Category = category,
                    Type = ticketType,
                    Branch = branch,
                    Attachments = attachmentDtos
                };

                var content = new StringContent(
                    JsonConvert.SerializeObject(dto),
                    Encoding.UTF8,
                    "application/json");

                var response = await _httpClient
                    .PostAsync($"{_apiBaseUrl}/api/Tickets/Create", content);

                string responseBody = await response.Content.ReadAsStringAsync();

                if (response.IsSuccessStatusCode)
                {
                    var apiResponse =
                        JsonConvert.DeserializeObject<ApiResponse>(responseBody)
                        ?? new ApiResponse();

                    // P6-025 fix: نجاح الأعمال لا يُستنتج من HTTP2xx وحده — جسم
                    // الرد يحمل Success/Message من الخدمة ويُحترم: رد 2xx برسالة
                    // رفض من الخدمة = فشل فعلي برسالة الخدمة (كان أي 2xx = نجاح).
                    if (!apiResponse.Success)
                    {
                        return new TicketResponse
                        {
                            Success = false,
                            Message = string.IsNullOrEmpty(apiResponse.Message)
                                ? $"رفضت الخدمة إنشاء التذكرة ({response.StatusCode})"
                                : apiResponse.Message
                        };
                    }

                    return new TicketResponse
                    {
                        Success = true,
                        Message = apiResponse.Message,
                        TicketNumber = apiResponse.TicketNumber
                    };
                }

                return new TicketResponse
                {
                    Success = false,
                    Message = $"فشل إنشاء التذكرة ({response.StatusCode})"
                };
            }
            catch (Exception ex)
            {
                return new TicketResponse
                {
                    Success = false,
                    Message = "خطأ: " + ex.Message
                };
            }
        }

        public async Task<TicketDetailsResponse> GetTicketAsync(string ticketNumber)
        {
            try
            {
                var response = await _httpClient
                    .GetAsync($"{_apiBaseUrl}/api/Tickets/Number/{ticketNumber}");

                string responseBody = await response.Content.ReadAsStringAsync();

                if (response.IsSuccessStatusCode)
                {
                    // P6-024 fix: الجسم المحلل هو مصدر بيانات التذكرة — كان يُحلل
                    // إلى نموذج مختزل ثم يُرمى وتُعاد استجابة Success=true بتذكرة
                    // غير مهيأة (Ticket=null) فيسقط المستدعي بمرجع فارغ عند
                    // result.Ticket.Subject. الآن: التفاصيل المحللة تُعاد في
                    // Ticket، والنجاح مشروط بتذكرة موجودة فعلًا.
                    var ticket =
                        JsonConvert.DeserializeObject<TicketDetails>(responseBody);

                    if (ticket != null && !string.IsNullOrEmpty(ticket.TicketNumber))
                    {
                        return new TicketDetailsResponse
                        {
                            Success = true,
                            Ticket = ticket
                        };
                    }

                    return new TicketDetailsResponse
                    {
                        Success = false,
                        Message = "جسم الرد لا يحمل تذكرة صالحة"
                    };
                }

                return new TicketDetailsResponse
                {
                    Success = false,
                    Message = "التذكرة غير موجودة"
                };
            }
            catch (Exception ex)
            {
                return new TicketDetailsResponse
                {
                    Success = false,
                    Message = "حدث خطأ: " + ex.Message
                };
            }
        }

        public async Task<List<TicketDetails>> GetCustomerTicketsAsync(string customerName)
        {
            try
            {
                var response = await _httpClient
                    .GetAsync($"{_apiBaseUrl}/api/Tickets/GetTicketsBycustomer" +
                              $"?cust={customerName}");

                if (response.IsSuccessStatusCode)
                {
                    string body = await response.Content.ReadAsStringAsync();
                    return JsonConvert.DeserializeObject<List<TicketDetails>>(body)
                           ?? new List<TicketDetails>();
                }

                // P6-025 fix: الفشل لا يُنكر كقائمة فارغة — تعاد null فيميز
                // المستدعي بين «لا تذاكر للعميل» (قائمة فارغة) و«تعذر الجلب»
                // (null) فلا تعرض الشاشة فشلًا كأنه غياب تذاكر.
                return null;
            }
            catch (Exception ex)
            {
                System.Diagnostics.Debug.WriteLine(
                    $"خطأ في GetCustomerTicketsAsync: {ex.Message}");
                return null;
            }
        }

        public async Task<ApiResponseBase> AddReplyAsync(
            int ticketID,
            string senderName,
            string senderType,
            string message)
        {
            try
            {
                var payload = new
                {
                    TicketId = ticketID,
                    SenderName = senderName,
                    SenderType = senderType,
                    Message = message
                };

                var content = new StringContent(
                    JsonConvert.SerializeObject(payload),
                    Encoding.UTF8,
                    "application/json");

                var response = await _httpClient
                    .PostAsync($"{_apiBaseUrl}/api/Tickets/AddReply", content);

                // P6-025 fix: جسم الرد يُحلل ويُحترم — نجاح الأعمال في الرسالة
                // لا في HTTP2xx وحده (كان الجسم يُقرأ ويُرمى).
                string replyBody = await response.Content.ReadAsStringAsync();
                if (response.IsSuccessStatusCode)
                {
                    ApiResponseBase parsed = null;
                    try
                    {
                        parsed = JsonConvert.DeserializeObject<ApiResponseBase>(replyBody);
                    }
                    catch
                    {
                        // جسم غير قابل للتحليل — نكتفي بنجاح النقل
                    }
                    if (parsed != null && !parsed.Success)
                    {
                        return new ApiResponseBase
                        {
                            Success = false,
                            Message = string.IsNullOrEmpty(parsed.Message)
                                ? "رفضت الخدمة إضافة الرد"
                                : parsed.Message
                        };
                    }
                    return new ApiResponseBase
                    {
                        Success = true,
                        Message = (parsed != null && !string.IsNullOrEmpty(parsed.Message))
                            ? parsed.Message
                            : "تم إضافة الرد بنجاح"
                    };
                }

                return new ApiResponseBase
                {
                    Success = false,
                    Message = "فشل إضافة الرد"
                };
            }
            catch (Exception ex)
            {
                return new ApiResponseBase
                {
                    Success = false,
                    Message = "حدث خطأ: " + ex.Message
                };
            }
        }

        #endregion
    }
}