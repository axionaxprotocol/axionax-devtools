#!/usr/bin/env python3
"""
Fix dependencies to use file: protocol instead of workspace:
"""

import json
from pathlib import Path

def fix_dependency_to_file_protocol(file_path, sdk_path):
    """Change @axionax/sdk to use file: protocol"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        if 'dependencies' in data and '@axionax/sdk' in data['dependencies']:
            data['dependencies']['@axionax/sdk'] = sdk_path
            print(f"✅ Updated {file_path.name}: @axionax/sdk -> {sdk_path}")
        
        with open(file_path, 'w', encoding='utf-8', newline='\n') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
            f.write('\n')
        
        return True
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def update_root_package_json():
    """Update root package.json for npm workspaces"""
    root_package = Path('package.json')
    
    package_json = {
        "name": "axionax-monorepo",
        "version": "1.0.0",
        "private": True,
        "workspaces": [
            "axionax-sdk-ts",
            "axionax-web",
            "axionax-marketplace"
        ],
        "scripts": {
            "install-all": "npm install",
            "build:sdk": "cd axionax-sdk-ts && npm run build",
            "build:web": "cd axionax-web && npm run build",
            "build:marketplace": "cd axionax-marketplace && npm run build",
            "build-all": "npm run build:sdk && npm run build:web && npm run build:marketplace",
            "dev:web": "cd axionax-web && npm run dev",
            "dev:marketplace": "cd axionax-marketplace && npm run dev"
        },
        "devDependencies": {
            "typescript": "^5.4.0"
        }
    }
    
    with open(root_package, 'w', encoding='utf-8', newline='\n') as f:
        json.dump(package_json, f, indent=2, ensure_ascii=False)
        f.write('\n')
    
    print("✅ Updated root package.json")

def main():
    print("🔧 Fixing npm workspace dependencies")
    print("=" * 80)
    print()
    
    # Fix axionax-web
    web_package = Path('axionax-web/package.json')
    if web_package.exists():
        fix_dependency_to_file_protocol(web_package, 'file:../axionax-sdk-ts')
    
    # Fix axionax-marketplace
    marketplace_package = Path('axionax-marketplace/package.json')
    if marketplace_package.exists():
        fix_dependency_to_file_protocol(marketplace_package, 'file:../axionax-sdk-ts')
    
    # Update root package.json
    update_root_package_json()
    
    print()
    print("✅ All dependencies fixed!")
    print()
    print("📋 Next steps:")
    print("  1. npm install (this will install all workspaces)")
    print("  2. npm run build:sdk (build SDK first)")
    print("  3. npm run build-all (build everything)")
    print()

if __name__ == "__main__":
    main()
