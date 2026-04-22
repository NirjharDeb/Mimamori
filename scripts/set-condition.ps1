param(
    [Parameter(Mandatory = $true)]
    [ValidateSet("baseline", "light", "strong")]
    [string]$Condition
)

$repoRoot = Split-Path -Parent $PSScriptRoot
$sourceMap = @{
    baseline = Join-Path $repoRoot "study/conditions/baseline.mdc"
    light    = Join-Path $repoRoot "study/conditions/light-control-card.mdc"
    strong   = Join-Path $repoRoot "study/conditions/structured-review-card.mdc"
}

$source = $sourceMap[$Condition]
$targetDir = Join-Path $repoRoot ".cursor/rules"
$target = Join-Path $targetDir "control-card-active.mdc"

if (-not (Test-Path $source)) {
    throw "Condition file not found: $source"
}

New-Item -ItemType Directory -Force -Path $targetDir | Out-Null
Copy-Item -Path $source -Destination $target -Force

Write-Host "Activated condition: $Condition"
Write-Host "Active rule: $target"
