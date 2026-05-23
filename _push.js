/**
 * _push.js — 一键推送到 GitHub Pages
 * 由 2_推送GitHub.bat 调用，避免 bat 文件中文编码问题
 */
const { execSync } = require('child_process');

const REPO = 'D:/CLAUDE CODE/report-dashboard';
const URL  = 'https://lyylly2022.github.io/report-dashboard/home.html';

function run(label, cmd, allowFail) {
  console.log('\n============================================');
  console.log('  ' + label);
  console.log('============================================');
  try {
    execSync(cmd, { cwd: REPO, stdio: 'inherit' });
    return true;
  } catch (e) {
    if (allowFail) {
      console.log('  (skipped — nothing to do)');
      return false;
    }
    console.error('\n[ERROR] ' + label + ' failed.');
    process.exit(1);
  }
}

// Step 1: Pull latest
run('Step 1/3  git pull --rebase', 'git pull --rebase --autostash');

// Step 2: Commit with timestamp
const now = new Date();
const pad = n => String(n).padStart(2, '0');
const msg = 'update reports ' +
  now.getFullYear() + '-' + pad(now.getMonth()+1) + '-' + pad(now.getDate()) +
  ' ' + pad(now.getHours()) + ':' + pad(now.getMinutes());

run('Step 2/3  git add + commit', 'git add .', false);
run('         committing: ' + msg, 'git commit -m "' + msg + '"', true);

// Step 3: Push
run('Step 3/3  git push', 'git push');

console.log('\n============================================');
console.log('  Done! Pages update in ~30 sec.');
console.log('  ' + URL);
console.log('============================================\n');
