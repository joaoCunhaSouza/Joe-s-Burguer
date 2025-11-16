<#
deploy_render.ps1

Automates local migration/collectstatic and pushes to origin branch so Render (if connected to the repo)
will run its build and deploy. Use this only if your local repo has the correct remote (origin)
and you are comfortable committing generated migration files.

Usage (PowerShell):
  .\scripts\deploy_render.ps1 -Branch main

Options:
  -Branch  Branch to push (default: main)

This script will:
  - run `python manage.py makemigrations` (may create migration files)
  - run `python manage.py migrate`
  - run `python manage.py collectstatic --noinput`
  - if there are file changes (for example new migration files), stage and commit them
    with a standard message and push to the configured remote branch.

Make sure your virtualenv is activated if you rely on a local interpreter.
#>

param(
  [string]$Branch = 'main'
)

function Run-Command($cmd) {
  Write-Host "-> $cmd" -ForegroundColor Cyan
  $proc = Start-Process -FilePath pwsh -ArgumentList "-NoProfile -Command $cmd" -NoNewWindow -Wait -PassThru -RedirectStandardError stderr.txt -RedirectStandardOutput stdout.txt
  $out = Get-Content stdout.txt -ErrorAction SilentlyContinue
  $err = Get-Content stderr.txt -ErrorAction SilentlyContinue
  if ($out) { Write-Host $out }
  if ($err) { Write-Host $err -ForegroundColor Red }
  Remove-Item stdout.txt, stderr.txt -ErrorAction SilentlyContinue
  return $proc.ExitCode
}

Write-Host "Starting local deploy helper (branch: $Branch)" -ForegroundColor Green

# 1) makemigrations
if (Run-Command "python manage.py makemigrations") {
  Write-Host "makemigrations finished" -ForegroundColor Green
} else {
  Write-Host "makemigrations returned non-zero exit code" -ForegroundColor Yellow
}

# 2) migrate
if (Run-Command "python manage.py migrate --noinput") {
  Write-Host "migrate finished" -ForegroundColor Green
} else {
  Write-Host "migrate returned non-zero exit code" -ForegroundColor Yellow
}

# 3) collectstatic
if (Run-Command "python manage.py collectstatic --noinput") {
  Write-Host "collectstatic finished" -ForegroundColor Green
} else {
  Write-Host "collectstatic returned non-zero exit code" -ForegroundColor Yellow
}

# 4) git add/commit if changes
$status = git status --porcelain
if ($status) {
  Write-Host "Detected git changes, committing them..." -ForegroundColor Yellow
  git add -A
  $msg = "chore: deploy - add migrations/static changes"
  git commit -m $msg
  if ($LASTEXITCODE -ne 0) {
    Write-Host "git commit failed or nothing to commit" -ForegroundColor Yellow
  }
} else {
  Write-Host "No git changes detected." -ForegroundColor Green
}

# 5) push
Write-Host "Pushing to origin/$Branch..." -ForegroundColor Cyan
git push origin $Branch
if ($LASTEXITCODE -eq 0) {
  Write-Host "Push complete. If your repo is connected to Render, deploy will be triggered." -ForegroundColor Green
} else {
  Write-Host "git push failed. Check remote configuration and credentials." -ForegroundColor Red
}

Write-Host "Done." -ForegroundColor Green
