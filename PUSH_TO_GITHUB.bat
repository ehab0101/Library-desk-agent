@echo off
REM ============================================
REM Push to GitHub - Quick Script
REM ============================================

echo.
echo ============================================
echo   Push Library Desk Agent to GitHub
echo ============================================
echo.

REM Refresh PATH
for /f "tokens=2*" %%A in ('reg query "HKLM\SYSTEM\CurrentControlSet\Control\Session Manager\Environment" /v PATH') do set "MACHINE_PATH=%%B"
for /f "tokens=2*" %%A in ('reg query "HKCU\Environment" /v PATH') do set "USER_PATH=%%B"
set "PATH=%MACHINE_PATH%;%USER_PATH%"

echo Current Git Status:
git status
echo.

echo ============================================
echo   Repository Status
echo ============================================
git log --oneline -1
echo.

echo ============================================
echo   Next Steps:
echo ============================================
echo.
echo 1. Create GitHub repository at: https://github.com/new
echo    - Name: library-desk-agent
echo    - DO NOT initialize with README
echo    - Click "Create repository"
echo.
echo 2. Copy the repository URL
echo.
echo 3. Run this command (replace YOUR_USERNAME):
echo    git remote add origin https://github.com/YOUR_USERNAME/library-desk-agent.git
echo.
echo 4. Then push:
echo    git push -u origin main
echo.
echo 5. When prompted, use Personal Access Token as password:
echo    - Get token from: https://github.com/settings/tokens
echo    - Create token with 'repo' scope
echo.

set /p REPO_URL="Enter your GitHub repository URL (or press Enter to skip): "

if not "%REPO_URL%"=="" (
    echo.
    echo Adding remote repository...
    git remote add origin %REPO_URL%
    
    if errorlevel 1 (
        echo.
        echo Remote might already exist. Checking...
        git remote set-url origin %REPO_URL%
    )
    
    echo.
    echo Pushing to GitHub...
    git push -u origin main
    
    if errorlevel 1 (
        echo.
        echo [ERROR] Push failed. Common issues:
        echo - Repository doesn't exist yet
        echo - Authentication failed (use Personal Access Token)
        echo - Check your repository URL
    ) else (
        echo.
        echo ============================================
        echo   SUCCESS! Project uploaded to GitHub!
        echo ============================================
    )
) else (
    echo.
    echo Skipped. You can add remote manually later.
)

echo.
pause
