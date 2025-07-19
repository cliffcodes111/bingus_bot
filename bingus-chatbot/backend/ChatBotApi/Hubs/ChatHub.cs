using Microsoft.AspNetCore.SignalR;
using ChatBotApi.Services;

namespace ChatBotApi.Hubs
{
    public class ChatHub : Hub
    {
        private readonly IPythonAiService _pythonAiService;

        public ChatHub(IPythonAiService pythonAiService)
        {
            _pythonAiService = pythonAiService;
        }

        public async Task SendMessage(string message)
        {
            try
            {
                // Send user message to all clients immediately
                await Clients.All.SendAsync("ReceiveMessage", "User", message);
                
                // Get AI response from Python script
                var aiResponse = await _pythonAiService.GetAiResponseAsync(message);
                
                // Send AI response to all clients
                await Clients.All.SendAsync("ReceiveMessage", "AI", aiResponse);
            }
            catch (Exception ex)
            {
                // Send error message to clients
                await Clients.All.SendAsync("ReceiveMessage", "System", $"Error: {ex.Message}");
            }
        }
    }
} 