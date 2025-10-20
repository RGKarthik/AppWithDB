# PowerShell script to run Bollywood Quiz
Write-Host "================================================================" -ForegroundColor Cyan
Write-Host "                BOLLYWOOD QUIZ APPLICATION" -ForegroundColor Cyan  
Write-Host "================================================================" -ForegroundColor Cyan
Write-Host ""

# Function to test Python command
function Test-PythonCommand {
    param($cmd)
    try {
        & $cmd --version 2>$null | Out-Null
        return $LASTEXITCODE -eq 0
    }
    catch {
        return $false
    }
}

# Try to find Python
$pythonCmd = $null

# Try different Python commands
$pythonCommands = @(
    "python",
    "py", 
    "python3",
    "C:\Users\$env:USERNAME\AppData\Local\Microsoft\WindowsApps\python.exe"
)

foreach ($cmd in $pythonCommands) {
    if (Test-PythonCommand $cmd) {
        $pythonCmd = $cmd
        Write-Host "[INFO] Found Python: $cmd" -ForegroundColor Green
        break
    }
}

if (-not $pythonCmd) {
    Write-Host "[ERROR] Python not found!" -ForegroundColor Red
    Write-Host ""
    Write-Host "SOLUTIONS:" -ForegroundColor Yellow
    Write-Host "1. Install Python from: https://www.python.org/downloads/"
    Write-Host "   - Check 'Add Python to PATH' during installation"
    Write-Host ""
    Write-Host "2. Fix Microsoft Store Python:"
    Write-Host "   - Settings > Apps > Advanced app settings > App execution aliases"
    Write-Host "   - Enable python.exe and python3.exe"
    Write-Host ""
    Read-Host "Press Enter to exit"
    exit 1
}

# Show Python version
Write-Host ""
& $pythonCmd --version

# Check dependencies
Write-Host "[INFO] Checking dependencies..." -ForegroundColor Yellow
try {
    & $pythonCmd -c "import flask" 2>$null
    if ($LASTEXITCODE -ne 0) {
        Write-Host "[INFO] Installing dependencies..." -ForegroundColor Yellow
        & $pythonCmd -m pip install -r requirements.txt
        if ($LASTEXITCODE -ne 0) {
            Write-Host "[ERROR] Failed to install dependencies!" -ForegroundColor Red
            Read-Host "Press Enter to exit"
            exit 1
        }
    }
}
catch {
    Write-Host "[ERROR] Error checking dependencies: $_" -ForegroundColor Red
    Read-Host "Press Enter to exit"  
    exit 1
}

Write-Host "[INFO] Dependencies OK. Starting application..." -ForegroundColor Green
Write-Host ""
Write-Host "================================================================" -ForegroundColor Cyan
Write-Host " QUIZ ACCESS INFO:" -ForegroundColor White
Write-Host " - Open browser to: http://localhost:5000" -ForegroundColor White
Write-Host " - Database status: http://localhost:5000/status" -ForegroundColor White  
Write-Host " - Manual DB init: http://localhost:5000/init_db" -ForegroundColor White
Write-Host ""
Write-Host " Press Ctrl+C to stop the server" -ForegroundColor White
Write-Host "================================================================" -ForegroundColor Cyan
Write-Host ""

# Start the application
try {
    & $pythonCmd app.py
}
catch {
    Write-Host "[ERROR] Failed to start application: $_" -ForegroundColor Red
}

Write-Host ""
Write-Host "Quiz application stopped." -ForegroundColor Yellow
Read-Host "Press Enter to exit"