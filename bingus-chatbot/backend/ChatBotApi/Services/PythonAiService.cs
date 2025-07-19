using System.Diagnostics;
using System.Text;
using System.Text.Json;

namespace ChatBotApi.Services
{
    public class PythonAiService : IPythonAiService
    {
        private readonly IConfiguration _configuration;
        private readonly ILogger<PythonAiService> _logger;
        private readonly IHttpClientFactory _httpClientFactory;

        public PythonAiService(
            IConfiguration configuration,
            ILogger<PythonAiService> logger,
            IHttpClientFactory httpClientFactory)
        {
            _configuration = configuration;
            _logger = logger;
            _httpClientFactory = httpClientFactory;
        }

        public async Task<string> GetAiResponseAsync(string userMessage)
        {
            try
            {
                // Get Python AI HTTP endpoint from configuration
                var pythonApiUrl = "http://localhost:5001/ai-chat";
                var client = _httpClientFactory.CreateClient();

                var requestBody = new
                {
                    message = userMessage
                };
                var json = JsonSerializer.Serialize(requestBody);
                var content = new StringContent(json, Encoding.UTF8, "application/json");

                _logger.LogInformation($"Sending request to Python AI API: {pythonApiUrl}");

                var response = await client.PostAsync(pythonApiUrl, content);

                if (!response.IsSuccessStatusCode)
                {
                    var error = await response.Content.ReadAsStringAsync();
                    _logger.LogError($"Python AI API failed with status code {response.StatusCode}. Error: {error}");
                    return $"Error: Python AI API failed - {error}";
                }

                var responseContent = await response.Content.ReadAsStringAsync();

                if (string.IsNullOrWhiteSpace(responseContent))
                {
                    _logger.LogWarning("Python AI API returned empty output");
                    return "Error: No response from AI service";
                }

                _logger.LogInformation($"AI response received: {responseContent.Trim()}");
                return responseContent.Trim();
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error calling Python AI service");
                return $"Error: {ex.Message}";
            }
        }
    }
} 