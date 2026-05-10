<#
.SYNOPSIS
  MedXAI — PowerShell equivalent of the project Makefile.

.DESCRIPTION
  Mirrors every Makefile target so Windows contributors do not need WSL
  or `make`. All real work shells out to `uv run …` so behaviour matches
  CI and the POSIX Makefile exactly.

.EXAMPLE
  ./make.ps1 setup
  ./make.ps1 lint
  ./make.ps1 test
#>

[CmdletBinding()]
param(
    [Parameter(Position = 0)]
    [string]$Target = "help"
)

$ErrorActionPreference = "Stop"
$uv = if ($env:UV) { $env:UV } else { "uv" }

function Invoke-UV {
    param([string[]]$Args)
    & $uv @Args
    if ($LASTEXITCODE -ne 0) {
        throw "uv $($Args -join ' ') failed with exit code $LASTEXITCODE"
    }
}

function Show-Help {
    Write-Host "MedXAI — make.ps1 targets:`n"
    @(
        @{ Name = "setup";              Desc = "One-time setup: sync deps + install pre-commit hooks." }
        @{ Name = "lock";               Desc = "Refresh uv.lock without installing." }
        @{ Name = "sync";               Desc = "Install / update the env from uv.lock." }
        @{ Name = "precommit-install";  Desc = "Install pre-commit hooks." }
        @{ Name = "lint";               Desc = "Ruff lint + format check." }
        @{ Name = "format";             Desc = "Apply ruff fixes + formatting." }
        @{ Name = "type";               Desc = "Mypy strict on src/." }
        @{ Name = "test";               Desc = "Run pytest suite (parallel, coverage on)." }
        @{ Name = "cov";                Desc = "Run pytest with HTML coverage report." }
        @{ Name = "train";              Desc = "(Phase 2+) Run a training experiment." }
        @{ Name = "eval";               Desc = "(Phase 2+) Evaluate a trained model." }
        @{ Name = "app";                Desc = "(Phase 2+) Launch the Streamlit demo." }
        @{ Name = "api";                Desc = "(Phase 7) Launch the FastAPI backend." }
        @{ Name = "docs";               Desc = "(Phase 0+) Build MkDocs site locally." }
        @{ Name = "docs-serve";         Desc = "(Phase 0+) Serve MkDocs site at http://127.0.0.1:8000." }
        @{ Name = "paper";              Desc = "(Phase 8) Build the IEEE paper PDF." }
        @{ Name = "clean";              Desc = "Remove caches and build artefacts." }
    ) | ForEach-Object {
        Write-Host ("  {0,-18} {1}" -f $_.Name, $_.Desc)
    }
}

switch ($Target.ToLower()) {
    "help"               { Show-Help }
    "setup" {
        Invoke-UV @("sync", "--all-extras")
        Invoke-UV @("run", "pre-commit", "install")
    }
    "lock"               { Invoke-UV @("lock") }
    "sync"               { Invoke-UV @("sync", "--all-extras") }
    "precommit-install"  { Invoke-UV @("run", "pre-commit", "install") }
    "lint" {
        Invoke-UV @("run", "ruff", "check", ".")
        Invoke-UV @("run", "ruff", "format", "--check", ".")
    }
    "format" {
        Invoke-UV @("run", "ruff", "check", ".", "--fix")
        Invoke-UV @("run", "ruff", "format", ".")
    }
    "type"               { Invoke-UV @("run", "mypy", "src/medxai") }
    "test"               { Invoke-UV @("run", "pytest", "-n", "auto") }
    "cov"                { Invoke-UV @("run", "pytest", "-n", "auto", "--cov-report=html") }
    "train"              { Write-Host "[Phase 2+] training pipeline not yet implemented — see docs/PLAN.md" }
    "eval"               { Write-Host "[Phase 2+] evaluation pipeline not yet implemented — see docs/PLAN.md" }
    "app"                { Write-Host "[Phase 2+] Streamlit app not yet implemented — see docs/PLAN.md" }
    "api"                { Write-Host "[Phase 7] FastAPI backend not yet implemented — see docs/PLAN.md" }
    "docs"               { Invoke-UV @("run", "mkdocs", "build", "--strict") }
    "docs-serve"         { Invoke-UV @("run", "mkdocs", "serve") }
    "paper"              { Write-Host "[Phase 8] paper build (LaTeX) not yet implemented — see docs/PLAN.md" }
    "clean" {
        @(".ruff_cache", ".mypy_cache", ".pytest_cache", ".coverage",
          "htmlcov", "coverage.xml", "site", "dist", "build") |
            ForEach-Object {
                if (Test-Path $_) { Remove-Item -Recurse -Force $_ }
            }
        Get-ChildItem -Path . -Recurse -Force -Directory -Filter "__pycache__" |
            ForEach-Object { Remove-Item -Recurse -Force $_.FullName }
    }
    default {
        Write-Host "Unknown target: $Target`n" -ForegroundColor Red
        Show-Help
        exit 1
    }
}
