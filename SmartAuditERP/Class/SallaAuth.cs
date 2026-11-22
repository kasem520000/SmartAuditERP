using System;
using System.Collections.Generic;
using System.Net.Http;
using System.Threading.Tasks;
using Newtonsoft.Json.Linq;

namespace SmartAuditERP
{

	// P6-029 fix: نتيجة OAuth كاملة دورةً — الدورة كانت تقف عند تبادل code
	// بعائد access_token فقط (بلا refresh_token/expiry فلا يمكن للجلسة أن
	// تتجدد دون إعادة التفويض كاملًا)، وredirect_uri كان ثابتًا نصيًا
	// («YOUR_REDIRECT_URI») لا قيمة فعلية.
	public class SallaTokenResult
	{
		public string AccessToken { get; set; }
		public string RefreshToken { get; set; }
		public int ExpiresIn { get; set; }
	}

	public class SallaAuth
	{
		private const string AuthUrl = "https://accounts.salla.sa/oauth2/token";

		public async Task<SallaTokenResult> GetAccessToken(string clientId, string clientSecret, string code, string redirectUri)
		{
			using HttpClient httpClient = new HttpClient();
			HttpResponseMessage httpResponseMessage;
			httpResponseMessage = await httpClient.PostAsync("https://accounts.salla.sa/oauth2/token", new FormUrlEncodedContent(new Dictionary<string, string>
		{
			{ "grant_type", "authorization_code" },
			{ "client_id", clientId },
			{ "client_secret", clientSecret },
			{ "code", code },
			{ "redirect_uri", redirectUri }
		}));
			string text;
			text = await httpResponseMessage.Content.ReadAsStringAsync();
			if (httpResponseMessage.IsSuccessStatusCode)
			{
				JObject jObject = JObject.Parse(text);
				return new SallaTokenResult
				{
					AccessToken = jObject["access_token"]?.ToString(),
					RefreshToken = jObject["refresh_token"]?.ToString(),
					ExpiresIn = (int?)jObject["expires_in"] ?? 0
				};
			}
			throw new Exception($"خطأ في الحصول على Access Token: {text}");
		}

		// P6-029 fix: دورة التجديد — تحديث التوكن بـ refresh_token دون إعادة
		// تفويض المستخدم (كانت الدورة في المستودع لا تتجاوز التبادل الأول أبدًا).
		public async Task<SallaTokenResult> RefreshAccessToken(string clientId, string clientSecret, string refreshToken)
		{
			using HttpClient httpClient = new HttpClient();
			HttpResponseMessage httpResponseMessage;
			httpResponseMessage = await httpClient.PostAsync("https://accounts.salla.sa/oauth2/token", new FormUrlEncodedContent(new Dictionary<string, string>
		{
			{ "grant_type", "refresh_token" },
			{ "client_id", clientId },
			{ "client_secret", clientSecret },
			{ "refresh_token", refreshToken }
		}));
			string text;
			text = await httpResponseMessage.Content.ReadAsStringAsync();
			if (httpResponseMessage.IsSuccessStatusCode)
			{
				JObject jObject = JObject.Parse(text);
				return new SallaTokenResult
				{
					AccessToken = jObject["access_token"]?.ToString(),
					RefreshToken = jObject["refresh_token"]?.ToString(),
					ExpiresIn = (int?)jObject["expires_in"] ?? 0
				};
			}
			throw new Exception($"خطأ في تجديد Access Token: {text}");
		}
	}
}