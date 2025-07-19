namespace ChatBotApi.Services
{
    public interface IPythonAiService
    {
        Task<string> GetAiResponseAsync(string userMessage);
    }
} 