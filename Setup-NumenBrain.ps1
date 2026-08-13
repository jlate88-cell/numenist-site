<#
    Setup-NumenBrain.ps1
    ---------------------------------------------------------------
    One-command builder for the Numen Local Brain on Windows 11.

    It INSPECTS what is already on this machine, ADVISES what is
    missing, and INSTALLS only what is needed:
      - Git            (to pull the Numen corpus)
      - Ollama         (runs DeepSeek locally)
      - DeepSeek models + embedding model
      - Python 3.11    (for Open WebUI)
      - Open WebUI     (the chat + knowledge-base interface)
      - Tailscale      (private phone access)
    It also AUTO-DETECTS your Obsidian vault(s) so you know exactly
    what to feed the brain.

    HOW TO RUN (do this once):
      1. Save this file to your Desktop.
      2. Right-click the Start button -> "Terminal (Admin)".
      3. Paste and run:
           Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass -Force
           & "$HOME\Desktop\Setup-NumenBrain.ps1"

    Safe to re-run. It skips anything already done.
    A few steps open a browser or a prompt (GitHub sign-in for a
    private repo, Tailscale sign-in) - those are yours to complete.
#>

$ErrorActionPreference = 'Continue'
$BrainsRoot = 'C:\Brains'
$RepoUrl     = 'https://github.com/jlate88-cell/numenist-site.git'

function Say  ($m) { Write-Host "`n>> $m" -ForegroundColor Cyan }
function Ok   ($m) { Write-Host "   [OK]   $m" -ForegroundColor Green }
function Warn ($m) { Write-Host "   [!]    $m" -ForegroundColor Yellow }
function Info ($m) { Write-Host "   $m"       -ForegroundColor Gray }

function Refresh-Path {
    # Pull PATH from the registry so tools installed this session are usable now.
    $machine = [Environment]::GetEnvironmentVariable('Path','Machine')
    $user    = [Environment]::GetEnvironmentVariable('Path','User')
    $env:Path = "$machine;$user"
}

function Have ($cmd) { [bool](Get-Command $cmd -ErrorAction SilentlyContinue) }

function Winget-Install ($id, $name) {
    Say "Checking $name ..."
    if (-not (Have winget)) {
        Warn "winget (App Installer) not found. Install 'App Installer' from the Microsoft Store, then re-run this script."
        return $false
    }
    $installed = winget list --id $id -e 2>$null | Select-String $id
    if ($installed) { Ok "$name already installed."; return $true }
    Info "Installing $name (a UAC prompt may appear - approve it)..."
    winget install -e --id $id --accept-package-agreements --accept-source-agreements
    Refresh-Path
    Ok "$name install attempted."
    return $true
}

Write-Host "==================================================" -ForegroundColor DarkYellow
Write-Host "   THE NUMEN LOCAL BRAIN - one-command setup"        -ForegroundColor DarkYellow
Write-Host "==================================================" -ForegroundColor DarkYellow

# ---------------------------------------------------------------
# 0. Admin check (needed for firewall rules)
# ---------------------------------------------------------------
$isAdmin = ([Security.Principal.WindowsPrincipal] `
    [Security.Principal.WindowsIdentity]::GetCurrent() `
   ).IsInRole([Security.Principal.WindowsBuiltinRole]::Administrator)
if (-not $isAdmin) {
    Warn "Not running as Administrator. Installs will work, but the firewall step will be skipped."
    Warn "For the full run, relaunch Terminal as Admin."
}

# ---------------------------------------------------------------
# 1. Git + clone the Numen corpus (Brain 1)
# ---------------------------------------------------------------
Winget-Install 'Git.Git' 'Git' | Out-Null
Refresh-Path
if (Have git) {
    if (-not (Test-Path $BrainsRoot)) { New-Item -ItemType Directory -Path $BrainsRoot | Out-Null }
    $repoPath = Join-Path $BrainsRoot 'numenist-site'
    if (Test-Path $repoPath) {
        Say "Numen corpus already cloned - pulling any updates..."
        Push-Location $repoPath; git pull; Pop-Location
        Ok "Corpus up to date at $repoPath"
    } else {
        Say "Cloning the Numen corpus (a GitHub sign-in window may open for the private repo)..."
        git clone $RepoUrl $repoPath
        if (Test-Path $repoPath) { Ok "Corpus cloned to $repoPath" } else { Warn "Clone did not complete - sign in to GitHub and re-run." }
    }
} else {
    Warn "Git not available yet. Re-open the terminal and re-run this script."
}

# ---------------------------------------------------------------
# 2. Detect Obsidian vault(s) (Brain 2) - inspect, don't move
# ---------------------------------------------------------------
Say "Looking for your Obsidian vault(s)..."
$obsidianJson = Join-Path $env:APPDATA 'obsidian\obsidian.json'
if (Test-Path $obsidianJson) {
    $vaults = (Get-Content $obsidianJson -Raw | ConvertFrom-Json).vaults
    $paths  = $vaults.PSObject.Properties.Value.path
    if ($paths) {
        Ok "Found these vault folder(s) - these are what you'll feed the brain:"
        $paths | ForEach-Object { Write-Host "        $_" -ForegroundColor White }
        $paths -join "`n" | Set-Content (Join-Path $BrainsRoot 'obsidian-vault-paths.txt')
        Info "Saved the list to $BrainsRoot\obsidian-vault-paths.txt"
    } else { Warn "Obsidian is installed but no vaults are registered yet. Open a vault in Obsidian, then re-run." }
} else {
    Warn "No Obsidian config found. If your vault is on this laptop, open it in Obsidian once, then re-run."
}

# ---------------------------------------------------------------
# 3. Ollama + models
# ---------------------------------------------------------------
Winget-Install 'Ollama.Ollama' 'Ollama' | Out-Null
Refresh-Path
Start-Sleep -Seconds 3
if (Have ollama) {
    foreach ($m in @('deepseek-r1:7b','deepseek-r1:14b','nomic-embed-text')) {
        Say "Pulling model: $m (skips if already present)..."
        ollama pull $m
    }
    Ok "Models ready. Installed models:"
    ollama list
} else {
    Warn "Ollama command not on PATH yet. Close this window, open a NEW Terminal (Admin), and re-run - the model pulls will then work."
}

# ---------------------------------------------------------------
# 4. Make Ollama reachable from your phone (bind all interfaces)
# ---------------------------------------------------------------
Say "Setting Ollama to accept connections from your phone over Tailscale..."
[Environment]::SetEnvironmentVariable('OLLAMA_HOST','0.0.0.0','User')
[Environment]::SetEnvironmentVariable('OLLAMA_ORIGINS','*','User')
Ok "Set OLLAMA_HOST=0.0.0.0 and OLLAMA_ORIGINS=* (takes effect after Ollama restarts)."
Info "Fully quit Ollama from the system tray and relaunch it so this takes hold."

# ---------------------------------------------------------------
# 5. Python 3.11 + Open WebUI
# ---------------------------------------------------------------
Winget-Install 'Python.Python.3.11' 'Python 3.11' | Out-Null
Refresh-Path
if (Have pip) {
    Say "Installing Open WebUI (this can take a few minutes)..."
    pip install --upgrade open-webui
    Ok "Open WebUI installed."
    Info "To start it, run:  open-webui serve"
    Info "Then open http://localhost:8080 in your browser and create your owner account."
} else {
    Warn "pip not on PATH yet. Open a NEW terminal and run:  pip install open-webui"
}

# ---------------------------------------------------------------
# 6. Firewall (admin only) - let the phone reach the web UI + API
# ---------------------------------------------------------------
if ($isAdmin) {
    Say "Opening firewall ports 8080 (Open WebUI) and 11434 (Ollama) for private networks..."
    foreach ($p in 8080,11434) {
        if (-not (Get-NetFirewallRule -DisplayName "Numen $p" -ErrorAction SilentlyContinue)) {
            New-NetFirewallRule -DisplayName "Numen $p" -Direction Inbound -Protocol TCP -LocalPort $p -Action Allow -Profile Private | Out-Null
        }
    }
    Ok "Firewall rules in place."
} else {
    Warn "Skipped firewall (needs Admin). Later, in an Admin terminal, run:"
    Info 'New-NetFirewallRule -DisplayName "Numen 8080" -Direction Inbound -Protocol TCP -LocalPort 8080 -Action Allow -Profile Private'
    Info 'New-NetFirewallRule -DisplayName "Numen 11434" -Direction Inbound -Protocol TCP -LocalPort 11434 -Action Allow -Profile Private'
}

# ---------------------------------------------------------------
# 7. Tailscale (phone access)
# ---------------------------------------------------------------
Winget-Install 'Tailscale.Tailscale' 'Tailscale' | Out-Null

# ---------------------------------------------------------------
# Done - what's left for you
# ---------------------------------------------------------------
Write-Host "`n==================================================" -ForegroundColor DarkYellow
Write-Host "   SETUP PASS COMPLETE - your remaining steps:"       -ForegroundColor DarkYellow
Write-Host "==================================================" -ForegroundColor DarkYellow
Write-Host @"
  1. Restart Ollama from the system tray (Quit -> relaunch) so the
     phone-access setting takes hold.
  2. Start the interface:   open-webui serve
     Open http://localhost:8080 and create your owner account.
  3. In Open WebUI: Admin Settings -> Documents ->
        Embedding Engine = Ollama, Model = nomic-embed-text,
        Content Extraction = Docling.
  4. Workspace -> Knowledge -> +  ("Numen Brain"). Drag in:
        - your Obsidian vault folder (listed above)
        - C:\Brains\numenist-site  (markdown + PDFs)
  5. Open Tailscale (tray) -> sign in. Sign in on your PHONE's
     Tailscale app with the SAME account. Then on the phone browse to
        http://<this-laptop's-Tailscale-IP>:8080
     Get the IP with:   tailscale ip -4
  6. Keep this laptop awake: Settings -> Power -> Sleep (plugged in) = Never;
     lid close = Do nothing.
"@ -ForegroundColor White
Write-Host "  The brain is local. Nothing left this machine.`n" -ForegroundColor Green
