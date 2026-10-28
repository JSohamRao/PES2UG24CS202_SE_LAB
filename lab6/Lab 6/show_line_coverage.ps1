param([string]$Python = 'python')
$ErrorActionPreference = 'Stop'
Set-Location $PSScriptRoot
$Host.UI.RawUI.WindowTitle = 'Lab 6 - Code Coverage'
$py = $Python
Write-Host '$py -m coverage run --data-file=evidence/line/.coverage --source=movie_tickets -m pytest -q CodeCoverageTest_movie_tickets_application.py'
& $py -m coverage run --data-file=evidence/line/.coverage --source=movie_tickets -m pytest -q CodeCoverageTest_movie_tickets_application.py
if ($LASTEXITCODE -ne 0) { throw 'Tests failed' }
Write-Host '$py -m coverage report --data-file=evidence/line/.coverage -m --fail-under=90'
& $py -m coverage report --data-file=evidence/line/.coverage -m --fail-under=90
if ($LASTEXITCODE -ne 0) { throw 'Coverage target failed' }
