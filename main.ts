// gta6-clipper-01 entrypoint (Node 22, standard library only).
//
// The entry itself is the YouTube clip; this program's one job is to hand
// the gate the clip's address. VIDEO.json sits beside this file in the
// repository and holds {"url": "..."} naming the published video. The
// program checks that file is present and well formed, then copies it
// into the output directory, where the house reads the address and pulls
// the video's details and views from YouTube.
//
// Run it the way the grader does:
//   mkdir -p out && MAKEFUN_BOT_DIR=. MAKEFUN_OUTPUT_DIR=out node main.ts
// MAKEFUN_BOT_DIR stands in for the mounted repository (/bot) and
// MAKEFUN_OUTPUT_DIR for the results directory (/output).

import { copyFileSync, mkdirSync, readFileSync } from 'node:fs';
import { join } from 'node:path';

const repoDir = process.env.MAKEFUN_BOT_DIR ?? '/bot';
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';
const videoFile = join(repoDir, 'VIDEO.json');

// Fail here with a clear message rather than at the gate: VIDEO.json must
// exist and its "url" must be a non-empty string.
let parsed: unknown;
try {
  parsed = JSON.parse(readFileSync(videoFile, 'utf8'));
} catch (err) {
  console.error(`VIDEO.json unreadable at ${videoFile}: ${(err as Error).message}`);
  process.exit(1);
}
const url = (parsed as { url?: unknown } | null)?.url;
if (typeof url !== 'string' || url.length === 0) {
  console.error('VIDEO.json must be a JSON object with a non-empty "url" string.');
  process.exit(1);
}

mkdirSync(outDir, { recursive: true });
copyFileSync(videoFile, join(outDir, 'VIDEO.json'));
console.log(`clip entry handed over: ${url}`);
