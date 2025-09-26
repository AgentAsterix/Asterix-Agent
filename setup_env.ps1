# Agent-Aster Environment Setup Script for PowerShell

Write-Host "🔧 Setting up Agent-Aster Environment Variables..." -ForegroundColor Blue

# Set environment variables for this session - Replace with your actual keys
$env:OPENAI_API_KEY = "your-openai-api-key-here"
$env:ASTER_API_KEY = "your-aster-api-key-here"
$env:ASTER_API_SECRET = "your-aster-api-secret-here"
$env:ASTER_FERNET_KEY = "dGVzdF9lbmNyeXB0aW9uX2tleV9mb3JfZGV2ZWxvcG1lbnRfb25seQ=="
$env:ASTER_TESTNET = "false"

Write-Host "✅ Environment variables set!" -ForegroundColor Green

# Verify the setup
Write-Host "`n🔍 Verifying setup..." -ForegroundColor Yellow
Write-Host "OpenAI API Key: $($env:OPENAI_API_KEY.Substring(0,20))..." -ForegroundColor White
Write-Host "Aster API Key: $($env:ASTER_API_KEY.Substring(0,16))..." -ForegroundColor White
Write-Host "Aster API Secret: $($env:ASTER_API_SECRET.Substring(0,16))..." -ForegroundColor White

Write-Host "`n🚀 Ready to launch Agent-Aster!" -ForegroundColor Green
Write-Host "Run: streamlit run ui.py --server.port 8501" -ForegroundColor Cyan
