# push_report.ps1 - 生成并推送非亚渠道业绩报告到 GitHub Pages
$ErrorActionPreference = "Stop"

$PYTHON   = "C:\Users\liche\.workbuddy\binaries\python\versions\3.11.9\python.exe"
$SCRIPT   = "C:\Users\liche\AppData\Roaming\WorkBuddy\User\globalStorage\tencent-cloud.coding-copilot\brain\b11f38441fcf41bfa1758005f67019af\generate_report.py"
$SRC_HTML = "D:\claw\业绩统计\业绩统计输出\惠时尚非亚渠道业绩报告.html"
$REPO     = "D:\claw\report-dashboard"
$DST_HTML = "$REPO\sales-channel.html"
$TIMESTAMP = Get-Date -Format "yyyy-MM-dd HH:mm:ss"

Write-Host "========================================"
Write-Host "  Push Sales Channel Report to GitHub"
Write-Host "========================================"
Write-Host ""

# Step 1: 生成报告
Write-Host "[1/3] Generating report..."
& $PYTHON $SCRIPT
if ($LASTEXITCODE -ne 0) {
    Write-Host "[FAIL] Report generation failed. Check source Excel file." -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}
Write-Host "[OK] Report generated." -ForegroundColor Green
Write-Host ""

# Step 2: 复制到仓库并注入密码
Write-Host "[2/3] Copying report to repo and injecting password overlay..."
Copy-Item -Path $SRC_HTML -Destination $DST_HTML -Force
& powershell -NoProfile -ExecutionPolicy Bypass -File "$REPO\inject_pwd.ps1" -file $DST_HTML -titleCode "sales-channel"
if ($LASTEXITCODE -ne 0) {
    Write-Host "[FAIL] Password injection failed." -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}
Write-Host "[OK] Copied and password injected." -ForegroundColor Green
Write-Host ""

# Step 3: Git 提交并推送
Write-Host "[3/3] Committing and pushing to GitHub..."
Set-Location $REPO

git add sales-channel.html

# 检查是否有实质变更
git diff --cached --quiet
if ($LASTEXITCODE -eq 0) {
    Write-Host "[INFO] No changes detected, skipping commit." -ForegroundColor Yellow
} else {
    git commit -m "update: sales channel report $TIMESTAMP"
    if ($LASTEXITCODE -ne 0) {
        Write-Host "[FAIL] Commit failed." -ForegroundColor Red
        Read-Host "Press Enter to exit"
        exit 1
    }
    Write-Host "[OK] Committed." -ForegroundColor Green
}

# 同步远程（rebase 模式）
git pull --rebase origin master
if ($LASTEXITCODE -ne 0) {
    git rebase --abort 2>$null
    Write-Host "[FAIL] pull --rebase failed. Resolve conflicts in $REPO manually." -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

# 推送
git push origin master
if ($LASTEXITCODE -ne 0) {
    Write-Host "[FAIL] Push failed. Check network or GitHub auth (Git Credential Manager)." -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host "[OK] Pushed successfully." -ForegroundColor Green
Write-Host ""
Write-Host "========================================"
Write-Host "  Done! Page updates in ~1-2 minutes."
Write-Host "  URL: https://lyylly2022.github.io/report-dashboard/sales-channel.html"
Write-Host "========================================"
Read-Host "Press Enter to close"