#!/usr/bin/env pwsh
<#
.SYNOPSIS
    AxionAx Testnet Readiness Checker - PowerShell Wrapper

.DESCRIPTION
    Comprehensive pre-launch validation for AxionAx Protocol testnet deployment.
    Checks infrastructure, security, performance, documentation, and deployment readiness.

.EXAMPLE
    .\check-testnet-readiness.ps1

.EXAMPLE
    .\check-testnet-readiness.ps1 -Verbose

.NOTES
    Version: 1.0.0
    Author: AxionAx Protocol Team
    Last Updated: November 15, 2025
#>

param(
    [switch]$Verbose,
    [switch]$QuickCheck,
    [switch]$GenerateReport
)

# Set error action preference
$ErrorActionPreference = "Stop"

# Colors
function Write-ColorOutput {
    param(
        [string]$Message,
        [string]$Color = "White"
    )
    
    $colorMap = @{
        "Red" = "Red"
        "Green" = "Green"
        "Yellow" = "Yellow"
        "Cyan" = "Cyan"
        "Blue" = "Blue"
        "Magenta" = "Magenta"
        "White" = "White"
    }
    
    Write-Host $Message -ForegroundColor $colorMap[$Color]
}

# Banner
Write-Host ""
Write-ColorOutput "======================================================================" "Cyan"
Write-ColorOutput "  AXIONAX TESTNET READINESS CHECKER" "Cyan"
Write-ColorOutput "======================================================================" "Cyan"
Write-Host ""

# Check Python installation
Write-ColorOutput "Checking prerequisites..." "Yellow"

try {
    $pythonVersion = & python --version 2>&1
    Write-ColorOutput "  ✅ Python: $pythonVersion" "Green"
} catch {
    Write-ColorOutput "  ❌ Python not found. Please install Python 3.8+." "Red"
    exit 1
}

# Locate checker script
$checkerScript = Join-Path $PSScriptRoot "scripts/testing/testnet_readiness_checker.py"

if (-not (Test-Path $checkerScript)) {
    Write-ColorOutput "  ❌ Readiness checker script not found at: $checkerScript" "Red"
    exit 1
}

Write-ColorOutput "  ✅ Checker script found" "Green"
Write-Host ""

# Run the checker
Write-ColorOutput "Running comprehensive testnet readiness checks..." "Yellow"
Write-Host ""

try {
    # Change to workspace root
    Push-Location $PSScriptRoot
    
    # Run Python checker
    $exitCode = 0
    if ($Verbose) {
        python $checkerScript -v
        $exitCode = $LASTEXITCODE
    } else {
        python $checkerScript
        $exitCode = $LASTEXITCODE
    }
    
    Pop-Location
    
    # Check for report
    $reportPath = Join-Path $PSScriptRoot "TESTNET_READINESS_REPORT.json"
    
    if (Test-Path $reportPath) {
        Write-Host ""
        Write-ColorOutput "Detailed JSON report generated: TESTNET_READINESS_REPORT.json" "Cyan"
        
        # Parse and display key metrics
        $report = Get-Content $reportPath -Raw | ConvertFrom-Json
        
        Write-Host ""
        Write-ColorOutput "======================================================================" "Cyan"
        Write-ColorOutput "  KEY METRICS" "Cyan"
        Write-ColorOutput "======================================================================" "Cyan"
        Write-Host ""
        
        $overallStatus = if ($report.overall_passed) { "✅ READY" } else { "❌ NOT READY" }
        $statusColor = if ($report.overall_passed) { "Green" } else { "Red" }
        
        Write-ColorOutput "  Overall Status: $overallStatus" $statusColor
        Write-ColorOutput "  Overall Score:  $($report.overall_score)/100" "Yellow"
        Write-Host ""
        
        # Count by category
        $categories = @{}
        foreach ($result in $report.results) {
            if (-not $categories.ContainsKey($result.category)) {
                $categories[$result.category] = @{
                    total = 0
                    passed = 0
                    failed = 0
                }
            }
            $categories[$result.category].total++
            if ($result.passed) {
                $categories[$result.category].passed++
            } else {
                $categories[$result.category].failed++
            }
        }
        
        Write-ColorOutput "  Category Breakdown:" "White"
        foreach ($cat in $categories.Keys | Sort-Object) {
            $stats = $categories[$cat]
            $passRate = [math]::Round(($stats.passed / $stats.total) * 100, 1)
            $color = if ($passRate -ge 75) { "Green" } elseif ($passRate -ge 50) { "Yellow" } else { "Red" }
            
            $catTitle = (Get-Culture).TextInfo.ToTitleCase($cat)
            Write-ColorOutput "    $($catTitle.PadRight(20)): $($stats.passed)/$($stats.total) passed ($passRate%)" $color
        }
        
        # Critical issues
        $criticalIssues = $report.results | Where-Object { $_.critical -and -not $_.passed }
        if ($criticalIssues) {
            Write-Host ""
            Write-ColorOutput "  🚨 CRITICAL ISSUES (Must Fix):" "Red"
            foreach ($issue in $criticalIssues) {
                Write-ColorOutput "    • $($issue.name): $($issue.message)" "Red"
            }
        }
        
        Write-Host ""
        Write-ColorOutput "======================================================================" "Cyan"
        Write-Host ""
    }
    
    # Final recommendations
    if ($exitCode -eq 0) {
        Write-ColorOutput "🎉 TESTNET LAUNCH APPROVED!" "Green"
        Write-ColorOutput "   System passed all critical checks and is ready for deployment." "Green"
        Write-Host ""
        Write-ColorOutput "Next Steps:" "Yellow"
        Write-ColorOutput "  1. Schedule deployment window" "White"
        Write-ColorOutput "  2. Notify validators and community" "White"
        Write-ColorOutput "  3. Prepare rollback procedures" "White"
        Write-ColorOutput "  4. Monitor system health during launch" "White"
    } else {
        Write-ColorOutput "⚠️  TESTNET NOT READY" "Red"
        Write-ColorOutput "   Please address the issues above before proceeding with launch." "Yellow"
        Write-Host ""
        Write-ColorOutput "Recommended Actions:" "Yellow"
        Write-ColorOutput "  1. Fix all critical security issues" "White"
        Write-ColorOutput "  2. Complete missing documentation" "White"
        Write-ColorOutput "  3. Run security audit" "White"
        Write-ColorOutput "  4. Re-run this checker after fixes" "White"
    }
    
    Write-Host ""
    
    exit $exitCode
    
} catch {
    Write-ColorOutput "Error running readiness checker: $_" "Red"
    Pop-Location
    exit 1
}
