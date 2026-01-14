# Automated GitHub Upload Script
Write-Host ""
Write-Host "============================================" -ForegroundColor Cyan
Write-Host "  Library Desk Agent - GitHub Upload" -ForegroundColor Cyan
Write-Host "============================================" -ForegroundColor Cyan
Write-Host ""

# Check if Git is installed
try {
    $gitVersion = git --version 2>&1
    Write-Host "[1/7] Git is installed: $gitVersion" -ForegroundColor Green
} catch {
    Write-Host "[ERROR] Git is not installed!" -ForegroundColor Red
    Write-Host ""
    Write-Host "Please install Git first:" -ForegroundColor Yellow
    Write-Host "1. Download from: https://git-scm.com/download/win" -ForegroundColor Yellow
    Write-Host "2. Install Git" -ForegroundColor Yellow
    Write-Host "3. Restart PowerShell and run this script again" -ForegroundColor Yellow
    Write-Host ""
    Read-Host "Press Enter to exit"
    exit 1
}

# Navigate to project directory
Set-Location $PSScriptRoot
Write-Host "[2/7] Current directory: $(Get-Location)" -ForegroundColor Green
Write-Host ""

# Initialize Git if not already initialized
if (Test-Path ".git") {
    Write-Host "[3/7] Git repository already initialized." -ForegroundColor Yellow
} else {
    Write-Host "[3/7] Initializing Git repository..." -ForegroundColor Cyan
    git init
    if ($LASTEXITCODE -ne 0) {
        Write-Host "[ERROR] Failed to initialize Git!" -ForegroundColor Red
        Read-Host "Press Enter to exit"
        exit 1
    }
    Write-Host "Git repository initialized successfully!" -ForegroundColor Green
}
Write-Host ""

# Check status
Write-Host "[4/7] Checking files to commit..." -ForegroundColor Cyan
git status --short
Write-Host ""

# Add all files
Write-Host "[5/7] Adding all files..." -ForegroundColor Cyan
git add .
if ($LASTEXITCODE -ne 0) {
    Write-Host "[ERROR] Failed to add files!" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}
Write-Host "Files added successfully!" -ForegroundColor Green
Write-Host ""

# Create commit if there are changes
$status = git status --porcelain
if ([string]::IsNullOrWhiteSpace($status)) {
    Write-Host "[6/7] No changes to commit. Checking existing commits..." -ForegroundColor Yellow
    git log --oneline -1
} else {
    Write-Host "[6/7] Creating initial commit..." -ForegroundColor Cyan
    git commit -m "Initial commit: Library Desk Agent - Complete implementation"
    if ($LASTEXITCODE -ne 0) {
        Write-Host "[ERROR] Failed to create commit!" -ForegroundColor Red
        Read-Host "Press Enter to exit"
        exit 1
    }
    Write-Host "Commit created successfully!" -ForegroundColor Green
}
Write-Host ""

# Check remote
Write-Host "[7/7] Checking remote repository..." -ForegroundColor Cyan
$remote = git remote get-url origin 2>&1
if ($LASTEXITCODE -eq 0) {
    Write-Host "Remote repository configured: $remote" -ForegroundColor Green
    Write-Host ""
    Write-Host "To push to GitHub, run:" -ForegroundColor Yellow
    Write-Host "  git branch -M main" -ForegroundColor White
    Write-Host "  git push -u origin main" -ForegroundColor White
} else {
    Write-Host "Remote repository not configured." -ForegroundColor Yellow
    Write-Host ""
    Write-Host "============================================" -ForegroundColor Cyan
    Write-Host "  NEXT STEPS:" -ForegroundColor Cyan
    Write-Host "============================================" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "1. Create GitHub repository:" -ForegroundColor Yellow
    Write-Host "   - Go to: https://github.com/new" -ForegroundColor White
    Write-Host "   - Name: library-desk-agent" -ForegroundColor White
    Write-Host "   - Choose Public or Private" -ForegroundColor White
    Write-Host "   - DO NOT initialize with README" -ForegroundColor White
    Write-Host "   - Click 'Create repository'" -ForegroundColor White
    Write-Host ""
    Write-Host "2. Copy the repository URL" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "3. Run these commands:" -ForegroundColor Yellow
    Write-Host "   git remote add origin YOUR_REPO_URL" -ForegroundColor White
    Write-Host "   git branch -M main" -ForegroundColor White
    Write-Host "   git push -u origin main" -ForegroundColor White
    Write-Host ""
    Write-Host "4. When prompted for password, use Personal Access Token:" -ForegroundColor Yellow
    Write-Host "   - Get token from: https://github.com/settings/tokens" -ForegroundColor White
    Write-Host "   - Create token with 'repo' scope" -ForegroundColor White
    Write-Host "   - Use token as password (not your GitHub password)" -ForegroundColor White
    Write-Host ""
}

Write-Host "============================================" -ForegroundColor Cyan
Write-Host "  Current Git Status" -ForegroundColor Cyan
Write-Host "============================================" -ForegroundColor Cyan
git status
Write-Host ""

Read-Host "Press Enter to exit"
