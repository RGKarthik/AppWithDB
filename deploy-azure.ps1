# Azure Deployment PowerShell Script
# This script helps deploy your Bollywood Quiz app to Azure App Service

param(
    [Parameter(Mandatory=$true)]
    [string]$AppName,
    
    [Parameter(Mandatory=$false)]
    [string]$ResourceGroup = "bollywood-quiz-rg",
    
    [Parameter(Mandatory=$false)]
    [string]$Location = "East US"
)

Write-Host "🚀 Starting Azure deployment for Bollywood Quiz App..." -ForegroundColor Green

# Check if Azure CLI is installed
try {
    az --version | Out-Null
    Write-Host "✅ Azure CLI is installed" -ForegroundColor Green
} catch {
    Write-Host "❌ Azure CLI is not installed. Please install it from: https://docs.microsoft.com/en-us/cli/azure/install-azure-cli" -ForegroundColor Red
    exit 1
}

# Login to Azure
Write-Host "🔐 Logging in to Azure..." -ForegroundColor Yellow
az login

# Create resource group
Write-Host "📁 Creating resource group: $ResourceGroup" -ForegroundColor Yellow
az group create --name $ResourceGroup --location $Location

# Create App Service plan
Write-Host "📋 Creating App Service plan..." -ForegroundColor Yellow
az appservice plan create --name "$AppName-plan" --resource-group $ResourceGroup --sku FREE --is-linux

# Create web app
Write-Host "🌐 Creating web app: $AppName" -ForegroundColor Yellow
$deploymentOutput = az webapp create --resource-group $ResourceGroup --plan "$AppName-plan" --name $AppName --runtime "PYTHON|3.11" --deployment-local-git --output json | ConvertFrom-Json

if ($deploymentOutput) {
    Write-Host "✅ Web app created successfully!" -ForegroundColor Green
    Write-Host "🌍 Your app URL: https://$AppName.azurewebsites.net" -ForegroundColor Cyan
    
    # Configure app settings
    Write-Host "⚙️ Configuring app settings..." -ForegroundColor Yellow
    az webapp config appsettings set --resource-group $ResourceGroup --name $AppName --settings SCM_DO_BUILD_DURING_DEPLOYMENT=true
    az webapp config appsettings set --resource-group $ResourceGroup --name $AppName --settings FLASK_ENV=production
    
    # Set up deployment source
    Write-Host "📤 Setting up deployment..." -ForegroundColor Yellow
    $gitUrl = $deploymentOutput.deploymentLocalGitUrl
    
    Write-Host "🔧 Adding Azure remote..." -ForegroundColor Yellow
    git remote remove azure 2>$null  # Remove if exists
    git remote add azure $gitUrl
    
    Write-Host "📦 Pushing to Azure..." -ForegroundColor Yellow
    git push azure main
    
    Write-Host "🎉 Deployment completed!" -ForegroundColor Green
    Write-Host "🌍 Visit your app at: https://$AppName.azurewebsites.net" -ForegroundColor Cyan
    Write-Host "📊 Monitor your app in Azure Portal: https://portal.azure.com" -ForegroundColor Cyan
    
} else {
    Write-Host "❌ Failed to create web app" -ForegroundColor Red
    exit 1
}

Write-Host "✨ Next steps:" -ForegroundColor Yellow
Write-Host "1. Test your app at: https://$AppName.azurewebsites.net" -ForegroundColor White
Write-Host "2. Monitor logs in Azure Portal" -ForegroundColor White
Write-Host "3. Set up custom domain (optional)" -ForegroundColor White
Write-Host "4. Configure application insights for monitoring" -ForegroundColor White