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
                        JsonConvert.DeserializeObject<ApiResponse>(responseBody);

                    // Repair R-068 (audit finding P6-025): HTTP 2xx alone is transport, not business success;
                    // trust the envelope's own flag when the body carries one.
                    return new TicketResponse
                    {
                        Success = apiResponse != null && apiResponse.Success,
                        Message = apiResponse?.Message ?? "تعذر قراءة رد الخادم",
                        TicketNumber = apiResponse?.TicketNumber
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
                // Repair R-067 (audit finding P6-024): encode the path value, honour the business body instead
                // of discarding it, and never report success with an empty Ticket - consumers read its fields
                // directly. The wrapper only guarantees the number today; subject/status render as unavailable
                // until the details DTO is completed server-side (tracked residual).
                var response = await _httpClient
                    .GetAsync($"{_apiBaseUrl}/api/Tickets/Number/{Uri.EscapeDataString(ticketNumber)}");

                string responseBody = await response.Content.ReadAsStringAsync();

                if (response.IsSuccessStatusCode)
                {
                    var apiDetails = JsonConvert.DeserializeObject<TicketDetailsApiResponse>(responseBody);
                    if (apiDetails == null || !apiDetails.Success)
                    {
                        return new TicketDetailsResponse
                        {
                            Success = false,
                            Message = "رفض الطلب أو تعذر قراءة رد الخادم"
                        };
                    }
                    return new TicketDetailsResponse
                    {
                        Success = true,
                        Ticket = new TicketDetails
                        {
                            TicketNumber = string.IsNullOrWhiteSpace(apiDetails.TicketNumber)
                                ? ticketNumber
                                : apiDetails.TicketNumber
                        }
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
                              $"?cust={Uri.EscapeDataString(customerName ?? "")}");

                // Repair R-068 (audit finding P6-025): a genuine empty list stays empty, but transport or
                // business failures now surface to the caller's existing error handler instead of silently
                // masquerading as "no tickets". Query values are URI-encoded.
                if (!response.IsSuccessStatusCode)
                {
                    throw new HttpRequestException(
                        $"فشل جلب التذاكر ({(int)response.StatusCode})");
                }
                string body = await response.Content.ReadAsStringAsync();
                return JsonConvert.DeserializeObject<List<TicketDetails>>(body)
                       ?? new List<TicketDetails>();
            }
            catch (Exception ex)
            {
                System.Diagnostics.Debug.WriteLine(
                    $"خطأ في GetCustomerTicketsAsync: {ex.Message}");
                throw;
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

                string replyBody = await response.Content.ReadAsStringAsync();

                if (!response.IsSuccessStatusCode)
                {
                    return new ApiResponseBase { Success = false, Message = "فشل إضافة الرد" };
                }
                // Repair R-068 (audit finding P6-025): respect a business failure carried by an HTTP-success body;
                // a shape-less 2xx body keeps the legacy acceptance rather than inventing a stricter contract.
                var parsedReply = string.IsNullOrWhiteSpace(replyBody)
                    ? null
                    : JsonConvert.DeserializeObject<ApiResponseBase>(replyBody);
                if (parsedReply != null && !parsedReply.Success)
                {
                    return new ApiResponseBase
                    {
                        Success = false,
                        Message = string.IsNullOrWhiteSpace(parsedReply.Message)
                            ? "رفض الخادم إضافة الرد"
                            : parsedReply.Message
                    };
                }
                return new ApiResponseBase { Success = true, Message = "تم إضافة الرد بنجاح" };
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