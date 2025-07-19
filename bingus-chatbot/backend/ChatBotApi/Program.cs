using ChatBotApi.Hubs;
using ChatBotApi.Services;

var builder = WebApplication.CreateBuilder(args);

// Add services to the container
builder.Services.AddControllers();
builder.Services.AddSignalR();

// Add HttpClient factory for external API calls
builder.Services.AddHttpClient();

// Register our custom services
builder.Services.AddScoped<IPythonAiService, PythonAiService>();

// Add CORS to allow React frontend
builder.Services.AddCors(options =>
{
    options.AddPolicy("ReactApp", policy =>
    {
        policy.WithOrigins("http://localhost:3000", "http://localhost:5173")
              .AllowAnyHeader()
              .AllowAnyMethod()
              .AllowCredentials();
    });
});

var app = builder.Build();

// Configure the HTTP request pipeline
if (app.Environment.IsDevelopment())
{
    app.UseDeveloperExceptionPage();
}

// Enable CORS
app.UseCors("ReactApp");

app.UseHttpsRedirection();

app.UseRouting();

// Map SignalR hub
app.MapHub<ChatHub>("/chatHub");

app.MapControllers();

app.Run();
