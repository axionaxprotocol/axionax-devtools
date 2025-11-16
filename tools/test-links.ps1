# =====================================================
# Axionax Link Validation Script
# Tests all inter-repository links and documentation
# =====================================================

param(
    [switch]$Verbose,
    [switch]$FixLinks,
    [string]$Output = "link-test-results.txt"
)

$ErrorActionPreference = "Continue"
$TotalLinks = 0
$BrokenLinks = 0
$FixedLinks = 0
$Warnings = 0

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "  Axionax Link Validation Script v1.0" -ForegroundColor Cyan
Write-Host "========================================`n" -ForegroundColor Cyan

$startTime = Get-Date

# =====================================================
# Repository Structure Validation
# =====================================================

Write-Host "`n[1] Testing Repository Structure..." -ForegroundColor Yellow

$repos = @(
    "axionax-core",
    "axionax-deploy", 
    "axionax-devtools",
    "axionax-docs",
    "axionax-marketplace",
    "axionax-sdk-ts",
    "axionax-web",
    "axionax-phase1",
    "axionaxprotocol",
    "issue-manager"
)

foreach ($repo in $repos) {
    $path = Join-Path $PSScriptRoot $repo
    $TotalLinks++
    
    if (Test-Path $path) {
        Write-Host "  [OK] Found: $repo" -ForegroundColor Green
        
        # Check for git repository
        $gitPath = Join-Path $path ".git"
        if (Test-Path $gitPath) {
            Write-Host "       Git initialized" -ForegroundColor Gray
        } else {
            Write-Host "       [WARN] Not a git repository" -ForegroundColor Yellow
            $Warnings++
        }
        
        # Check for README
        $readmePath = Join-Path $path "README.md"
        if (Test-Path $readmePath) {
            Write-Host "       README.md found" -ForegroundColor Gray
        } else {
            Write-Host "       [WARN] README.md missing" -ForegroundColor Yellow
            $Warnings++
        }
    } else {
        Write-Host "  [FAIL] Missing: $repo" -ForegroundColor Red
        $BrokenLinks++
    }
}

# =====================================================
# Markdown Link Validation
# =====================================================

Write-Host "`n[2] Testing Cross-Repository Links..." -ForegroundColor Yellow

$repoFolders = Get-ChildItem $PSScriptRoot -Directory | Where-Object { 
    $_.Name -match '^axionax-' -or $_.Name -eq 'issue-manager' -or $_.Name -eq 'axionaxprotocol'
}

foreach ($repo in $repoFolders) {
    Write-Host "  Checking: $($repo.Name)" -ForegroundColor Cyan
    
    # Find all markdown files
    $mdFiles = Get-ChildItem -Path $repo.FullName -Filter "*.md" -Recurse -ErrorAction SilentlyContinue
    
    foreach ($mdFile in $mdFiles) {
        $content = Get-Content $mdFile.FullName -Raw -ErrorAction SilentlyContinue
        if (-not $content) { continue }
        
        # Simple regex to find markdown links
        $pattern = '\[([^\]]+)\]\(([^\)]+)\)'
        $matches = Select-String -InputObject $content -Pattern $pattern -AllMatches
        
        if ($matches.Matches) {
            foreach ($match in $matches.Matches) {
                $linkText = $match.Groups[1].Value
                $linkPath = $match.Groups[2].Value
                $TotalLinks++
                
                # Skip external URLs
                if ($linkPath -match '^https?://') {
                    continue
                }
                
                # Skip anchors
                if ($linkPath -match '^#') {
                    continue
                }
                
                # Resolve relative path
                $baseDir = Split-Path $mdFile.FullName -Parent
                $resolvedPath = Join-Path $baseDir $linkPath
                
                try {
                    $resolvedPath = [System.IO.Path]::GetFullPath($resolvedPath)
                } catch {
                    continue
                }
                
                # Check if target exists
                if (-not (Test-Path $resolvedPath)) {
                    Write-Host "    [BROKEN] $linkText -> $linkPath" -ForegroundColor Red
                    Write-Host "             In: $($mdFile.Name)" -ForegroundColor Gray
                    $BrokenLinks++
                }
            }
        }
    }
}

# =====================================================
# Documentation Consistency Check
# =====================================================

Write-Host "`n[3] Testing Documentation Consistency..." -ForegroundColor Yellow

$repos = Get-ChildItem $PSScriptRoot -Directory | Where-Object { 
    $_.Name -match '^axionax-'
}

foreach ($repo in $repos) {
    $readmePath = Join-Path $repo.FullName "README.md"
    
    if (Test-Path $readmePath) {
        $content = Get-Content $readmePath -Raw
        
        # Check for inconsistent branding
        $axionaxCount = ([regex]::Matches($content, '\bAxionAX\b')).Count
        $axionaxCapCount = ([regex]::Matches($content, '\bAxionax\b')).Count
        
        if ($axionaxCount -gt 0 -or $axionaxCapCount -gt 0) {
            Write-Host "  [WARN] Inconsistent branding in $($repo.Name)" -ForegroundColor Yellow
            Write-Host "         AxionAX: $axionaxCount, Axionax: $axionaxCapCount" -ForegroundColor Gray
            $Warnings++
        } else {
            Write-Host "  [OK] $($repo.Name) branding consistent" -ForegroundColor Green
        }
    }
}

# =====================================================
# Website Link Testing
# =====================================================

Write-Host "`n[4] Testing Website Links..." -ForegroundColor Yellow

$webPath = Join-Path $PSScriptRoot "axionax-web"

if (Test-Path $webPath) {
    Write-Host "  [OK] Website repository found" -ForegroundColor Green
    
    # Check public/index.html
    $indexPath = Join-Path $webPath "public\index.html"
    if (Test-Path $indexPath) {
        $content = Get-Content $indexPath -Raw
        
        # Count GitHub links
        $githubLinks = ([regex]::Matches($content, 'github\.com/axionaxprotocol')).Count
        Write-Host "       Found $githubLinks GitHub repository links" -ForegroundColor Gray
        
        # Check for branding
        $axionaxCount = ([regex]::Matches($content, '\bAxionAX\b')).Count
        if ($axionaxCount -gt 0) {
            Write-Host "       [WARN] Found $axionaxCount instances of 'AxionAX' (should be 'axionax')" -ForegroundColor Yellow
            $Warnings++
        } else {
            Write-Host "       Branding consistent (axionax)" -ForegroundColor Gray
        }
    }
} else {
    Write-Host "  [FAIL] Website repository not found" -ForegroundColor Red
    $BrokenLinks++
}

# =====================================================
# Network Configuration Check
# =====================================================

Write-Host "`n[5] Testing Network Configuration..." -ForegroundColor Yellow

$expectedChainIDs = @{
    "Testnet" = "86137"
    "Mainnet" = "86150"
}

$repos = Get-ChildItem $PSScriptRoot -Directory
$foundChainIDs = @{}

foreach ($repo in $repos) {
    $mdFiles = Get-ChildItem -Path $repo.FullName -Filter "*.md" -Recurse -ErrorAction SilentlyContinue
    
    foreach ($mdFile in $mdFiles) {
        $content = Get-Content $mdFile.FullName -Raw -ErrorAction SilentlyContinue
        if (-not $content) { continue }
        
        # Look for Chain ID mentions
        if ($content -match 'Chain ID[:\s]+(\d+)') {
            $chainId = $Matches[1]
            if (-not $foundChainIDs.ContainsKey($chainId)) {
                $foundChainIDs[$chainId] = 0
            }
            $foundChainIDs[$chainId]++
        }
    }
}

foreach ($network in $expectedChainIDs.Keys) {
    $expected = $expectedChainIDs[$network]
    
    if ($foundChainIDs.ContainsKey($expected)) {
        Write-Host "  [OK] $network Chain ID $expected found ($($foundChainIDs[$expected]) mentions)" -ForegroundColor Green
    } else {
        Write-Host "  [WARN] $network Chain ID $expected not found" -ForegroundColor Yellow
        $Warnings++
    }
}

# Check for incorrect Chain IDs
foreach ($chainId in $foundChainIDs.Keys) {
    if ($chainId -notin $expectedChainIDs.Values) {
        Write-Host "  [FAIL] Unexpected Chain ID: $chainId" -ForegroundColor Red
        $BrokenLinks++
    }
}

# =====================================================
# Version Check
# =====================================================

Write-Host "`n[6] Checking Version Information..." -ForegroundColor Yellow

# Check package.json files
$packageFiles = Get-ChildItem $PSScriptRoot -Recurse -Filter "package.json" -ErrorAction SilentlyContinue | Select-Object -First 10

foreach ($pkgFile in $packageFiles) {
    try {
        $json = Get-Content $pkgFile.FullName -Raw | ConvertFrom-Json
        if ($json.version) {
            $repoName = (Split-Path (Split-Path $pkgFile.FullName -Parent) -Leaf)
            Write-Host "  $repoName`: v$($json.version)" -ForegroundColor Gray
        }
    } catch {
        # Skip invalid JSON
    }
}

# =====================================================
# Results Summary
# =====================================================

$endTime = Get-Date
$duration = ($endTime - $startTime).TotalSeconds

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "  Test Results Summary" -ForegroundColor Cyan
Write-Host "========================================`n" -ForegroundColor Cyan

Write-Host "Total Links Tested:  $TotalLinks" -ForegroundColor White
Write-Host "Broken Links:        " -NoNewline
if ($BrokenLinks -eq 0) {
    Write-Host "$BrokenLinks" -ForegroundColor Green
} else {
    Write-Host "$BrokenLinks" -ForegroundColor Red
}

Write-Host "Warnings:            " -NoNewline
if ($Warnings -eq 0) {
    Write-Host "$Warnings" -ForegroundColor Green
} else {
    Write-Host "$Warnings" -ForegroundColor Yellow
}

Write-Host "`nExecution Time:      $([math]::Round($duration, 2)) seconds" -ForegroundColor Cyan

# Save results to file
$results = @"
Axionax Link Validation Results
Generated: $(Get-Date -Format "yyyy-MM-dd HH:mm:ss")
Duration: $([math]::Round($duration, 2)) seconds

Summary:
- Total Links Tested: $TotalLinks
- Broken Links: $BrokenLinks
- Warnings: $Warnings

Status: $(if ($BrokenLinks -eq 0) { "PASSED" } else { "FAILED" })
"@

$results | Out-File $Output -Encoding UTF8
Write-Host "`nResults saved to: $Output" -ForegroundColor Cyan

# Exit code
if ($BrokenLinks -gt 0) {
    Write-Host "`n[FAILED] Tests failed with $BrokenLinks broken links`n" -ForegroundColor Red
    exit 1
} else {
    Write-Host "`n[SUCCESS] All tests passed!`n" -ForegroundColor Green
    exit 0
}
