@echo off
REM ============================================
REM Automated GitHub Upload Script
REM ============================================

echo.
echo ============================================
echo   Library Desk Agent - GitHub Upload
echo ============================================
echo.

REM Check if Git is installed
where git >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Git is not installed!
    echo.
    echo Please install Git first:
    echo 1. Download from: https://git-scm.com/download/win
    echo 2. Install Git
    echo 3. Restart this script
    echo.
    pause
    exit /b 1
)

echo [1/7] Git is installed. Proceeding...
echo.

REM Check if already initialized
if exist ".git" (
    echo [2/7] Git repository already initialized.
) else (
    echo [2/7] Initializing Git repository...
    git init
    if errorlevel 1 (
        echo [ERROR] Failed to initialize Git repository!
        pause
        exit /b 1
    )
    echo Git repository initialized successfully!
)
echo.

REM Check what will be committed
echo [3/7] Checking files to commit...
git status --short
echo.

REM Add all files
echo [4/7] Adding all files...
git add .
if errorlevel 1 (
    echo [ERROR] Failed to add files!
    pause
    exit /b 1
)
echo Files added successfully!
echo.

REM Check if there are changes to commit
git diff --cached --quiet
if %ERRORLEVEL% EQU 0 (
    echo [5/7] No changes to commit. Files may already be committed.
    git log --oneline -1
) else (
    echo [5/7] Creating initial commit...
    git commit -m "Initial commit: Library Desk Agent - Complete implementation"
    if errorlevel 1 (
        echo [ERROR] Failed to create commit!
        pause
        exit /b 1
    )
    echo Commit created successfully!
)
echo.

REM Check if remote already exists
git remote get-url origin >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    echo [6/7] Remote repository already configured.
    git remote -v
    echo.
    echo To push to existing remote, run:
    echo   git push -u origin main
) else (
    echo [6/7] Remote repository not configured.
    echo.
    echo ============================================
    echo   NEXT STEPS (Manual):
    echo ============================================
    echo.
    echo 1. Create a GitHub repository:
    echo    - Go to: https://github.com/new
    echo    - Name: library-desk-agent
    echo    - Choose Public or Private
    echo    - DO NOT initialize with README
    echo    - Click "Create repository"
    echo.
    echo 2. Copy the repository URL
    echo.
    echo 3. Run this command (replace YOUR_URL):
    echo    git remote add origin YOUR_REPO_URL
    echo.
    echo 4. Then push:
    echo    git branch -M main
    echo    git push -u origin main
    echo.
    echo 5. When prompted for password, use Personal Access Token:
    echo    - Get token from: https://github.com/settings/tokens
    echo    - Create token with 'repo' scope
    echo    - Use token as password
    echo.
)

echo.
echo ============================================
echo   Current Git Status
echo ============================================
git status
echo.

pause
