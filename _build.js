/**
 * _build.js — 一键构建：Excel → data.json → HTML → 加密
 * 由 1_构建报表.bat 调用，避免 bat 文件中文编码问题
 */
const { execSync } = require('child_process');
const fs = require('fs');
const path = require('path');

const BASE = 'D:/CLAUDE CODE/可视化分析/库存管理';
const REPO = 'D:/CLAUDE CODE/report-dashboard';

function run(label, cmd, cwd) {
  console.log('\n============================================');
  console.log('  ' + label);
  console.log('============================================');
  try {
    execSync(cmd, { cwd: cwd || BASE, stdio: 'inherit' });
  } catch (e) {
    console.error('\n[ERROR] ' + label + ' failed. Exit code: ' + e.status);
    process.exit(1);
  }
}

// Step 1: Excel -> data.json
run('Step 1/4  gendata.js  (Excel -> data.json)',
    'node "' + BASE + '/gendata.js"');

// Step 2: data.json -> HTML
run('Step 2/4  build.js  (data.json -> HTML)',
    'node "' + BASE + '/build.js"');

// Step 3: Copy to report-dashboard
console.log('\n============================================');
console.log('  Step 3/4  Copy to report-dashboard');
console.log('============================================');
const src = path.join(BASE, '万邑通库存管理.html');
const dst = path.join(REPO, '万邑通库存管理.html');
try {
  fs.copyFileSync(src, dst);
  console.log('  OK: copied to ' + dst);
} catch (e) {
  console.error('[ERROR] Copy failed: ' + e.message);
  process.exit(1);
}

// Step 4: Encrypt all pages
run('Step 4/4  encrypt.js  (AES encrypt all)',
    'node "' + BASE + '/encrypt.js"');

console.log('\n============================================');
console.log('  Build complete! Run 2_Push_GitHub.bat next.');
console.log('============================================\n');
