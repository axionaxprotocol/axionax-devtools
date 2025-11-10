# Automated Fix Script for axionax Repositories (Windows PowerShell)
# Generated: 2025-11-07

Write-Host "🔧 Starting automated fixes..." -ForegroundColor Cyan
Write-Host ""

# 1. Fix UTF-8 BOM issues in package.json files
Write-Host "📝 Fixing: UTF-8 BOM issues in JSON files" -ForegroundColor Yellow
Write-Host ""

$repos = @('axionax-marketplace', 'axionax-deploy')
foreach ($repo in $repos) {
    $packageJsonPath = Join-Path $repo "package.json"
    if (Test-Path $packageJsonPath) {
        Write-Host "  Fixing UTF-8 BOM in $repo/package.json..." -ForegroundColor Gray
        
        # Read file without BOM and write back
        $content = Get-Content $packageJsonPath -Raw -Encoding UTF8
        $utf8NoBom = New-Object System.Text.UTF8Encoding $false
        [System.IO.File]::WriteAllText($packageJsonPath, $content, $utf8NoBom)
        
        Write-Host "  ✅ Fixed BOM in $repo/package.json" -ForegroundColor Green
    }
}

Write-Host ""

# 2. Install Node.js dependencies
Write-Host "📝 Fixing: Installing Node.js dependencies" -ForegroundColor Yellow
Write-Host ""

$nodeRepos = @('axionax-web', 'axionax-sdk-ts', 'axionax-marketplace')
foreach ($repo in $nodeRepos) {
    $packageJsonPath = Join-Path $repo "package.json"
    if ((Test-Path $repo) -and (Test-Path $packageJsonPath)) {
        Write-Host "  Installing dependencies for $repo..." -ForegroundColor Gray
        Push-Location $repo
        
        try {
            npm install
            Write-Host "  ✅ Dependencies installed for $repo" -ForegroundColor Green
        }
        catch {
            Write-Host "  ⚠️  Error installing dependencies for $repo : $_" -ForegroundColor Red
        }
        
        Pop-Location
    }
}

Write-Host ""

# 3. Check Cargo.toml structure in axionax-core
Write-Host "📝 Checking: Cargo.toml structure" -ForegroundColor Yellow
Write-Host ""

$cargoPath = "axionax-core\Cargo.toml"
if (Test-Path $cargoPath) {
    $cargoContent = Get-Content $cargoPath -Raw
    
    if ($cargoContent -notmatch '\[package\]') {
        Write-Host "  ⚠️  axionax-core/Cargo.toml appears to be a workspace root" -ForegroundColor Yellow
        Write-Host "     This is normal if it's configured as a workspace." -ForegroundColor Gray
        Write-Host "     Check for [workspace] section instead." -ForegroundColor Gray
    }
    else {
        Write-Host "  ✅ Cargo.toml has proper [package] section" -ForegroundColor Green
    }
}

Write-Host ""

# 4. Verify git status
Write-Host "📝 Checking: Git repository status" -ForegroundColor Yellow
Write-Host ""

$allRepos = @('axionax-core', 'axionax-web', 'axionax-sdk-ts', 'axionax-marketplace', 
              'axionax-docs', 'axionax-deploy', 'axionax-devtools')

foreach ($repo in $allRepos) {
    if (Test-Path "$repo\.git") {
        Push-Location $repo
        
        $branch = git rev-parse --abbrev-ref HEAD 2>$null
        $status = git status --porcelain 2>$null
        
        if ($status) {
            Write-Host "  ⚠️  $repo has uncommitted changes on branch: $branch" -ForegroundColor Yellow
        }
        else {
            Write-Host "  ✅ $repo is clean on branch: $branch" -ForegroundColor Green
        }
        
        Pop-Location
    }
}

Write-Host ""
Write-Host "=" -NoNewline -ForegroundColor Cyan
Write-Host "=" * 79 -ForegroundColor Cyan

Write-Host ""
Write-Host "✅ Automated fixes completed!" -ForegroundColor Green
Write-Host ""
Write-Host "📋 Next Steps:" -ForegroundColor Cyan
Write-Host "  1. Review the changes made" -ForegroundColor Gray
Write-Host "  2. Run: python test_repo_integration.py" -ForegroundColor Gray
Write-Host "  3. Check INTEGRATION_TEST_REPORT.txt for results" -ForegroundColor Gray
Write-Host ""
