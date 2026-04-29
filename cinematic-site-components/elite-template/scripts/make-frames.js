/**
 * make-frames.js
 * 
 * Utility to extract frames from a video file for the ScrollVideoBackground component.
 * Requires ffmpeg to be installed.
 * 
 * Usage: node scripts/make-frames.js <video-path> <output-dir>
 */

import { execSync } from 'child_process';
import path from 'path';
import fs from 'fs';

const videoPath = process.argv[2];
const outputDir = process.argv[3] || './public/bg-frames';

if (!videoPath) {
  console.error('Usage: node scripts/make-frames.js <video-path> [output-dir]');
  process.exit(1);
}

if (!fs.existsSync(outputDir)) {
  fs.mkdirSync(outputDir, { recursive: true });
}

console.log(`Extracting frames from ${videoPath} to ${outputDir}...`);

try {
  // Extract 30 frames evenly distributed across the video
  // We use -vf "select=..." to get exactly N frames
  const frameCount = 30;
  execSync(`ffmpeg -i "${videoPath}" -vf "select='not(mod(n,max(1,floor(trunc(v_total_duration*r)/${frameCount}))))',setpts=N/FRAME_RATE/TB" -vframes ${frameCount} "${path.join(outputDir, 'frame-%04d.jpg')}"`);
  console.log('Done!');
} catch (error) {
  console.error('Error extracting frames:', error.message);
}
