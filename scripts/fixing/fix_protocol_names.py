#!/usr/bin/env python3
"""
Fix protocol naming: axionax protocol -> axionax protocol
"""
import os
import re
from pathlib import Path

WORKSPACE_ROOT = Path(r"D:\Desktop\axionaxius01")
EXTENSIONS = [".md", ".ts", ".tsx", ".html", ".json", ".toml", ".rs", ".go", ".py", ".sh", ".yml", ".yaml"]
EXCLUDE_DIRS = {"node_modules", ".git", "dist", "build", "target", "out", ".next", "__pycache__"}

def should_process(file_path):
    """Check if file should be processed"""
    return (
        file_path.suffix in EXTENSIONS and
        not any(exclude in file_path.parts for exclude in EXCLUDE_DIRS)
    )

def fix_protocol_name(content):
    """Replace protocol names"""
    replacements = [
        (r"axionax protocol", "axionax protocol"),
        (r"axionax protocol", "axionax protocol"),
        (r"axionax protocol", "axionax protocol"),
    ]
    
    modified = False
    for old, new in replacements:
        if old in content:
            content = content.replace(old, new)
            modified = True
    
    return content, modified

def main():
    print("🔍 Scanning workspace...")
    
    total_files = 0
    modified_files = 0
    
    for file_path in WORKSPACE_ROOT.rglob("*"):
        if not file_path.is_file() or not should_process(file_path):
            continue
        
        total_files += 1
        
        try:
            # Read file
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()
            
            # Fix names
            new_content, modified = fix_protocol_name(content)
            
            if modified:
                # Write back
                with open(file_path, "w", encoding="utf-8", newline="") as f:
                    f.write(new_content)
                
                print(f"✅ Fixed: {file_path.relative_to(WORKSPACE_ROOT)}")
                modified_files += 1
        
        except Exception as e:
            print(f"⚠️  Error processing {file_path.name}: {e}")
    
    print(f"\n✨ Done!")
    print(f"📊 Scanned: {total_files} files")
    print(f"📝 Modified: {modified_files} files")

if __name__ == "__main__":
    main()
