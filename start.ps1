$ErrorActionPreference = "Stop"

$Root = Split-Path -Parent $MyInvocation.MyCommand.Path
$Backend = Join-Path $Root "backend"
$Frontend = Join-Path $Root "frontend"
$Venv = Join-Path $Backend ".venv"
$PythonExe = Join-Path $Venv "Scripts\python.exe"

function Stop-WithError([string]$Message) {
    Write-Host "" 
    Write-Host "ERREUR: $Message" -ForegroundColor Red
    Write-Host "La stack n'a pas ete lancee. Regarde l'erreur affichee juste au-dessus." -ForegroundColor Yellow
    Read-Host "Appuie sur Entree pour fermer"
    exit 1
}

function Assert-LastExitCode([string]$Step) {
    if ($LASTEXITCODE -ne 0) {
        Stop-WithError "$Step a echoue (code $LASTEXITCODE)."
    }
}

function Get-FreePort([int]$StartPort, [int]$MaxPort) {
    for ($port = $StartPort; $port -le $MaxPort; $port++) {
        $listener = $null
        try {
            $listener = [System.Net.Sockets.TcpListener]::new([System.Net.IPAddress]::Loopback, $port)
            $listener.Start()
            $listener.Stop()
            return $port
        } catch {
            if ($listener) { try { $listener.Stop() } catch {} }
        }
    }
    throw "Aucun port libre entre $StartPort et $MaxPort"
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "       StudySprint - demarrage local" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Python : le launcher Windows 'py' est prioritaire.
$PythonLauncher = $null
if (Get-Command py -ErrorAction SilentlyContinue) {
    $PythonLauncher = "py"
} elseif (Get-Command python -ErrorAction SilentlyContinue) {
    $PythonLauncher = "python"
} else {
    Stop-WithError "Python 3 n'est pas installe ou n'est pas dans le PATH."
}

if (-not (Get-Command npm -ErrorAction SilentlyContinue)) {
    Stop-WithError "Node.js/npm n'est pas installe ou n'est pas dans le PATH."
}

Write-Host "Versions detectees :" -ForegroundColor DarkGray
& $PythonLauncher --version
Assert-LastExitCode "Detection de Python"
node --version
Assert-LastExitCode "Detection de Node.js"
npm --version
Assert-LastExitCode "Detection de npm"
Write-Host ""

# 1) Environnement virtuel backend.
if (-not (Test-Path $PythonExe)) {
    Write-Host "[1/7] Creation de backend/.venv ..." -ForegroundColor Yellow
    & $PythonLauncher -m venv $Venv
    Assert-LastExitCode "Creation du venv Python"
} else {
    Write-Host "[1/7] backend/.venv deja present." -ForegroundColor Green
}

Write-Host "      Python utilise par le backend :" -NoNewline
& $PythonExe --version
Assert-LastExitCode "Verification du Python du venv"

# 2) Outils pip a jour.
Write-Host "[2/7] Mise a jour de pip/setuptools/wheel ..." -ForegroundColor Yellow
& $PythonExe -m pip install --upgrade pip setuptools wheel
Assert-LastExitCode "Mise a jour de pip"

# 3) Toutes les dependances Python sont installees avec LE MEME Python que celui qui lancera FastAPI.
Write-Host "[3/7] Installation/mise a jour de TOUTES les dependances backend ..." -ForegroundColor Yellow
& $PythonExe -m pip install --upgrade -r (Join-Path $Backend "requirements.txt")
Assert-LastExitCode "Installation des requirements Python"

# 4) Verification explicite des imports avant de lancer le serveur.
Write-Host "[4/7] Verification des dependances backend ..." -ForegroundColor Yellow
Push-Location $Backend
& $PythonExe -c "import fastapi, uvicorn, sqlalchemy, pydantic, pydantic_settings, email_validator, psycopg; import app.main; print('      Backend OK - FastAPI', fastapi.__version__, '- Pydantic', pydantic.__version__)"
$BackendCheckExit = $LASTEXITCODE
Pop-Location
if ($BackendCheckExit -ne 0) {
    Stop-WithError "Une dependance backend n'a pas pu etre importee. N'installe pas les libs une par une : copie l'erreur affichee ci-dessus."
}

# Fichiers .env locaux.
$BackendEnv = Join-Path $Backend ".env"
if (-not (Test-Path $BackendEnv)) {
    Copy-Item (Join-Path $Backend ".env.example") $BackendEnv
    Write-Host "      backend/.env cree." -ForegroundColor Green
}
$FrontendEnv = Join-Path $Frontend ".env"
if (-not (Test-Path $FrontendEnv)) {
    Copy-Item (Join-Path $Frontend ".env.example") $FrontendEnv
    Write-Host "      frontend/.env cree." -ForegroundColor Green
}

# 5) Dependances frontend.
Write-Host "[5/7] Installation/mise a jour des dependances frontend ..." -ForegroundColor Yellow
Push-Location $Frontend
npm install
$NpmInstallExit = $LASTEXITCODE
Pop-Location
if ($NpmInstallExit -ne 0) {
    Stop-WithError "npm install a echoue. Supprime frontend/node_modules et frontend/package-lock.json puis relance start.bat si npm signale un probleme de dependances optionnelles."
}

# Ports : on choisit automatiquement le premier port libre.
$BackendPort = Get-FreePort 8000 8010
$FrontendPort = Get-FreePort 5174 5190
$FrontendOrigin = "http://localhost:$FrontendPort"
$ApiUrl = "http://localhost:$BackendPort/api"

# 6) Backend. Les variables du processus remplacent les valeurs locales .env pour les ports choisis.
Write-Host "[6/7] Lancement de FastAPI sur http://localhost:$BackendPort ..." -ForegroundColor Yellow
$BackendCommand = "Set-Location -LiteralPath '$Backend'; `$env:FRONTEND_ORIGIN='$FrontendOrigin'; `$env:SITE_URL='$FrontendOrigin'; & '$PythonExe' -m uvicorn app.main:app --reload --host 0.0.0.0 --port $BackendPort"
Start-Process powershell -ArgumentList "-NoExit", "-ExecutionPolicy", "Bypass", "-Command", $BackendCommand

Start-Sleep -Seconds 2

# 7) Frontend.
Write-Host "[7/7] Lancement de React/Vite sur $FrontendOrigin ..." -ForegroundColor Yellow
$FrontendCommand = "Set-Location -LiteralPath '$Frontend'; `$env:VITE_API_URL='$ApiUrl'; npm run dev -- --port $FrontendPort --strictPort"
Start-Process powershell -ArgumentList "-NoExit", "-ExecutionPolicy", "Bypass", "-Command", $FrontendCommand

Write-Host ""
Write-Host "StudySprint est lance." -ForegroundColor Green
Write-Host "Application : $FrontendOrigin" -ForegroundColor Cyan
Write-Host "API         : http://localhost:$BackendPort" -ForegroundColor Cyan
Write-Host "Swagger     : http://localhost:$BackendPort/docs" -ForegroundColor Cyan
Write-Host ""
Write-Host "Les ports sont choisis automatiquement s'ils sont deja occupes." -ForegroundColor DarkGray
Write-Host "Deux fenetres PowerShell ont ete ouvertes. Ferme-les pour arreter les serveurs." -ForegroundColor DarkGray
