$ErrorActionPreference = "Stop"

Write-Host "Starting PhishGuard stack..."

# Get the directory where this script is located
$ScriptDir = Split-Path -Parent -Path $MyInvocation.MyCommand.Definition
$VenvPythonPath = Join-Path $ScriptDir "venv\Scripts\python.exe"

# Try to find Python: prefer venv, then system PATH, then check common installation paths
$PythonPath = $null

if (Test-Path $VenvPythonPath) {
    $PythonPath = $VenvPythonPath
    Write-Host "Using virtual environment Python: $PythonPath"
} else {
    # Try to find python in PATH
    $PythonExe = Get-Command python -ErrorAction SilentlyContinue
    if ($PythonExe) {
        $PythonPath = $PythonExe.Source
        Write-Host "Using system Python from PATH: $PythonPath"
    } else {
        Write-Error "Python executable not found. Please ensure Python is installed and available in PATH, or create a virtual environment at $VenvPythonPath"
        exit 1
    }
}

# always start processes in the project root so modules can be imported correctly
Start-Process powershell -WorkingDirectory $ScriptDir -ArgumentList "-NoExit", "-Command", "$PythonPath -m rules.consumer"
Start-Process powershell -WorkingDirectory $ScriptDir -ArgumentList "-NoExit", "-Command", "$PythonPath soc\consumer.py"
Start-Process powershell -WorkingDirectory $ScriptDir -ArgumentList "-NoExit", "-Command", "$PythonPath ingestion\smtp_gateway\server.py"
Start-Process powershell -WorkingDirectory $ScriptDir -ArgumentList "-NoExit", "-Command", "$PythonPath -m uvicorn soc.ui.app:app --host 127.0.0.1 --port 8000"

Write-Host "PhishGuard deployed locally."
