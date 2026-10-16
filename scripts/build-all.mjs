import { readFile, writeFile, mkdir, copyFile, readdir, stat, rm } from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const output = path.join(root, 'dist');

console.log('Building full site for Vercel deployment...');

// Recreate dist directory
await rm(output, { recursive: true, force: true });
await mkdir(output, { recursive: true });

async function copyRecursive(srcDir, destDir) {
  await mkdir(destDir, { recursive: true });
  const entries = await readdir(srcDir, { withFileTypes: true });

  for (const entry of entries) {
    const srcPath = path.join(srcDir, entry.name);
    const destPath = path.join(destDir, entry.name);

    if (entry.isDirectory()) {
      // Skip node_modules, .git, dist, scripts, scratch
      if (['node_modules', '.git', 'dist', 'scripts', '.system_generated', 'scratch'].includes(entry.name)) {
        continue;
      }
      await copyRecursive(srcPath, destPath);
    } else if (entry.isFile()) {
      // Skip development scripts or temp files
      if (entry.name.endsWith('.py') || entry.name === 'package-lock.json' || entry.name === 'fast_unused_images.py') {
        continue;
      }
      await copyFile(srcPath, destPath);
    }
  }
}

await copyRecursive(root, output);

console.log('Successfully built entire website into dist/ folder!');
