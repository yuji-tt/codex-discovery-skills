# Run from any directory after installing GitHub CLI and authenticating as yuji-tt.
$ErrorActionPreference = 'Stop'
Set-Location (Split-Path $PSScriptRoot -Parent)
function Invoke-Checked {
    param([string]$Program, [string[]]$Arguments)
    & $Program @Arguments
    if ($LASTEXITCODE -ne 0) { throw "$Program failed with exit code $LASTEXITCODE" }
}
if (-not (Get-Command gh -ErrorAction SilentlyContinue)) {
    throw 'GitHub CLI is missing. Install it, run gh auth login, then rerun this script.'
}
Invoke-Checked gh @('auth', 'status')
$login = & gh api user --jq .login
if ($LASTEXITCODE -ne 0 -or $login -ne 'yuji-tt') { throw 'The active GitHub account must be yuji-tt.' }
Invoke-Checked python @('scripts/validate.py')
Invoke-Checked python @('-m', 'unittest', 'discover', '-s', 'tests')
$dirty = & git status --porcelain
if ($LASTEXITCODE -ne 0 -or $dirty) { throw 'Commit the validated final state before publishing.' }
$branch = & git branch --show-current
if ($LASTEXITCODE -ne 0 -or $branch -ne 'main') { throw 'Expected branch main.' }
$description = 'Human-inspired research and problem-solving skills for Codex: question objectives, deepen hypotheses, transfer structures across domains, and iterate through falsifiable experiments.'
$origin = & git remote get-url origin 2>$null
if ($LASTEXITCODE -ne 0) {
    # Creation fails safely if the name is already taken; inspect ownership before retrying.
    Invoke-Checked gh @('repo', 'create', 'yuji-tt/codex-discovery-skills', '--public', '--description', $description, '--source', '.', '--remote', 'origin')
} elseif ($origin -notin @('https://github.com/yuji-tt/codex-discovery-skills.git', 'git@github.com:yuji-tt/codex-discovery-skills.git')) {
    throw "Unexpected origin: $origin"
}
Invoke-Checked git @('push', '-u', 'origin', 'main')
Invoke-Checked git @('fetch', 'origin', 'main')
$local = & git rev-parse HEAD
$remote = & git rev-parse origin/main
if ($local -ne $remote) { throw 'Remote commit does not match local HEAD.' }
$visibility = & gh repo view yuji-tt/codex-discovery-skills --json visibility --jq .visibility
if ($LASTEXITCODE -ne 0 -or $visibility -ne 'PUBLIC') { throw 'Public visibility not verified.' }
Invoke-Checked gh @('api', 'repos/yuji-tt/codex-discovery-skills/git/trees/main?recursive=1', '--jq', '.tree[].path')
Write-Output "Verified public repository at https://github.com/yuji-tt/codex-discovery-skills; commit $local"
Write-Output 'After CI passes, optionally run: gh release create v0.1.0 --target main --title v0.1.0 --notes "Initial four discovery skills, worked examples, evaluation harness, and validation."'
