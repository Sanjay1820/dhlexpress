import os
import shutil

BASE_DIR = r"c:\Users\Krunal\Desktop\DHLREXPRESS 13-10-2026\secound design\html"
DIST_DIR = os.path.join(BASE_DIR, "dist")

print("Building complete site into dist/...")

if os.path.exists(DIST_DIR):
    shutil.rmtree(DIST_DIR)

os.makedirs(DIST_DIR, exist_ok=True)

skip_dirs = {'node_modules', '.git', 'dist', 'scripts', '.system_generated', 'scratch', '__pycache__'}
skip_file_exts = {'.py', '.pyc'}

copied_count = 0

for root, dirs, files in os.walk(BASE_DIR):
    dirs[:] = [d for d in dirs if d not in skip_dirs]
    rel_dir = os.path.relpath(root, BASE_DIR)
    dest_dir = os.path.normpath(os.path.join(DIST_DIR, rel_dir)) if rel_dir != '.' else DIST_DIR
    os.makedirs(dest_dir, exist_ok=True)

    for f in files:
        if any(f.endswith(ext) for ext in skip_file_exts):
            continue
        src_file = os.path.join(root, f)
        dest_file = os.path.join(dest_dir, f)
        shutil.copy2(src_file, dest_file)
        copied_count += 1

print(f"Build complete! Copied {copied_count} files to dist/.")
