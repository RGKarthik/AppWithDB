# Azure Deployment Guide

## Prerequisites

1. **Azure Account**: Sign up at https://azure.microsoft.com
2. **Azure CLI**: Install from https://docs.microsoft.com/en-us/cli/azure/install-azure-cli
3. **Git Repository**: Your code should be in a Git repository (GitHub, Azure DevOps, etc.)

## Option 1: Deploy via Azure Portal (Easiest)

### Step 1: Create Azure App Service
1. Go to Azure Portal (portal.azure.com)
2. Click "Create a resource"
3. Search for "Web App"
4. Fill in the details:
   - **Subscription**: Your Azure subscription
   - **Resource Group**: Create new or use existing
   - **Name**: Your app name (must be globally unique)
   - **Runtime**: Python 3.11
   - **Region**: Choose closest to your users
   - **Pricing**: Free tier (F1) for testing, Basic (B1) for production

### Step 2: Configure Deployment
1. In your App Service, go to "Deployment Center"
2. Choose your source (GitHub, Azure Repos, etc.)
3. Select your repository and branch
4. Azure will automatically deploy your app

### Step 3: Configure Application Settings
1. Go to "Configuration" > "Application settings"
2. Add these settings:
   - `SCM_DO_BUILD_DURING_DEPLOYMENT` = `true`
   - `FLASK_ENV` = `production`
   - `PYTHONPATH` = `/home/site/wwwroot`

## Option 2: Deploy via Azure CLI

### Step 1: Login to Azure
```bash
az login
```

### Step 2: Create Resource Group
```bash
az group create --name bollywood-quiz-rg --location "East US"
```

### Step 3: Create App Service Plan
```bash
az appservice plan create --name bollywood-quiz-plan --resource-group bollywood-quiz-rg --sku FREE --is-linux
```

### Step 4: Create Web App
```bash
az webapp create --resource-group bollywood-quiz-rg --plan bollywood-quiz-plan --name your-unique-app-name --runtime "PYTHON|3.11" --deployment-local-git
```

### Step 5: Configure Deployment
```bash
# Set deployment credentials
az webapp deployment user set --user-name <username> --password <password>

# Deploy from local Git
git remote add azure <git-url-from-previous-command>
git push azure main
```

## Option 3: Deploy via VS Code Azure Extension

### Step 1: Install Azure Extension
1. Install "Azure App Service" extension in VS Code
2. Sign in to your Azure account

### Step 2: Deploy
1. Right-click on your project folder
2. Select "Deploy to Web App..."
3. Choose subscription and create/select App Service
4. VS Code will handle the deployment

## Production Considerations

### 1. Database Migration
For production, consider migrating from SQLite to Azure Database for PostgreSQL:

```python
# Update app.py database configuration
import os

if os.environ.get('AZURE_POSTGRESQL_CONNECTIONSTRING'):
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('AZURE_POSTGRESQL_CONNECTIONSTRING')
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bollywood_quiz.db'
```

### 2. Environment Variables
Set these in Azure App Service Configuration:
- `SECRET_KEY`: Generate a strong secret key
- `FLASK_ENV`: Set to 'production'
- `DATABASE_URL`: Your database connection string

### 3. Static Files (Optional)
For better performance, consider using Azure CDN for static files:
1. Create Azure Storage Account
2. Upload static files to blob storage
3. Configure CDN endpoint

### 4. Custom Domain (Optional)
1. In App Service, go to "Custom domains"
2. Add your domain name
3. Configure DNS settings with your domain provider

## Monitoring and Logging

1. **Application Insights**: Monitor performance and errors
2. **Log Stream**: View real-time logs in Azure Portal
3. **Metrics**: Monitor CPU, memory, and response times

## Troubleshooting

### Common Issues:
1. **Build Fails**: Check requirements-azure.txt for correct package versions
2. **Database Issues**: Ensure init_db.py runs during deployment
3. **Import Errors**: Verify PYTHONPATH is set correctly
4. **Port Issues**: Azure automatically assigns PORT environment variable

### Debug Commands:
```bash
# View logs
az webapp log tail --name your-app-name --resource-group your-rg

# SSH into container
az webapp ssh --name your-app-name --resource-group your-rg

# View configuration
az webapp config show --name your-app-name --resource-group your-rg
```

## Cost Optimization

- **Free Tier**: Good for development/testing (60 CPU minutes/day)
- **Basic Tier**: ~$13/month for production
- **Auto-scaling**: Configure based on traffic patterns
- **Reserved Instances**: Save up to 72% for predictable workloads

## Security Best Practices

1. Use Azure Key Vault for secrets
2. Enable HTTPS only
3. Configure CORS if needed
4. Regular security updates
5. Monitor with Azure Security Center

## Next Steps After Deployment

1. **Test thoroughly**: Verify all features work in production
2. **Set up monitoring**: Configure alerts for errors/performance
3. **Backup strategy**: Regular database backups
4. **CI/CD Pipeline**: Automate deployments with GitHub Actions
5. **Load testing**: Test with expected user load