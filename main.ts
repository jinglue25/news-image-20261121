import { copyFile, mkdir, stat } from 'node:fs/promises';
import { resolve } from 'node:path';

const source = new URL('./entry.png', import.meta.url);
const outputDir = resolve(process.env.MAKEFUN_OUTPUT_DIR || '/output');

try {
  const sourceInfo = await stat(source);
  if (!sourceInfo.isFile()) {
    throw new Error('entry.png must be a regular file');
  }
  await mkdir(outputDir, { recursive: true });
  await copyFile(source, resolve(outputDir, 'entry.png'));
  console.log(`Copied entry.png to ${outputDir}`);
} catch (error) {
  console.error(`Unable to copy entry.png: ${error.message}`);
  process.exitCode = 1;
}
