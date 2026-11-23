/**
 * THE DAILY CHRONICLE - Sunday, 22 November 2026 World News Edition
 * Copies the generated front-page entry.png to the target output directory
 * (MAKEFUN_OUTPUT_DIR or /output), with an existence guard.
 */

import { copyFileSync, existsSync } from 'node:fs';
import { join } from 'node:path';

const srcPath = new URL('./entry.png', import.meta.url);
const destDir = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';
const destPath = join(destDir, 'entry.png');

if (!existsSync(srcPath)) {
  console.error(`Error: entry.png not found at ${srcPath.pathname}`);
  process.exit(1);
}

copyFileSync(srcPath, destPath);
console.log(`Successfully copied entry.png to ${destPath}`);
