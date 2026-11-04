// Copies src/ into dist/, stamping the build time into index.html.
import { mkdir, readFile, writeFile, copyFile } from 'node:fs/promises';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const root = join(dirname(fileURLToPath(import.meta.url)), '..');
const src = join(root, 'src');
const dist = join(root, 'dist');

await mkdir(dist, { recursive: true });
const html = await readFile(join(src, 'index.html'), 'utf8');
await writeFile(join(dist, 'index.html'), html.replace('{{BUILD_TIME}}', new Date().toISOString()));
await copyFile(join(src, 'format.mjs'), join(dist, 'format.mjs'));
console.log('Built web/dist');
