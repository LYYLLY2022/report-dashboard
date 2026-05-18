/**
 * protect.js
 * 推送前保护检查：对使用 overlay 注入方式的报告重新注入密码。
 * 由各推送 bat 在 git add 之前调用：node protect.js
 */
'use strict';
const fs   = require('fs');
const path = require('path');

const REPO = path.join(__dirname);

// ── 密码遮罩（与 inject_pwd.ps1 / push_to_github.js 保持完全一致）─────────
const PWD_OVERLAY = `<style id="pwd-overlay-style">
#pwd-overlay{position:fixed;inset:0;z-index:99999;background:#0f0a1a;display:flex;align-items:center;justify-content:center;}
#pwd-overlay .pwdbox{background:rgba(30,20,50,.9);border:1px solid rgba(167,139,250,.35);border-radius:20px;padding:2.5rem 2rem;width:360px;max-width:90%;display:flex;flex-direction:column;gap:1.2rem;animation:pwdpop .2s ease;}
@keyframes pwdpop{from{transform:scale(.94);opacity:0}to{transform:scale(1);opacity:1}}
#pwd-overlay .pwdlock{font-size:2.8rem;text-align:center;}
#pwd-overlay .pwdtitle{text-align:center;}
#pwd-overlay .pwdtitle h2{font-size:1.2rem;font-weight:700;background:linear-gradient(135deg,#a78bfa,#60a5fa);-webkit-background-clip:text;-webkit-text-fill-color:transparent;margin-bottom:.3rem;}
#pwd-overlay .pwdtitle p{font-size:.82rem;color:#94a3b8;}
#pwd-overlay input[type=password]{width:100%;padding:11px 14px;background:rgba(255,255,255,.06);border:1px solid rgba(167,139,250,.3);border-radius:10px;color:#e2e8f0;font-size:15px;letter-spacing:2px;outline:none;transition:border-color .15s;}
#pwd-overlay input[type=password]:focus{border-color:#a78bfa;}
#pwd-overlay .pwdbtn{width:100%;padding:11px;border-radius:10px;border:none;background:linear-gradient(135deg,#7c3aed,#2563eb);color:#fff;font-size:15px;font-weight:600;cursor:pointer;transition:opacity .15s;}
#pwd-overlay .pwdbtn:hover{opacity:.88;}
#pwd-overlay .pwderr{font-size:12px;color:#f87171;text-align:center;min-height:16px;}
</style>
<div id="pwd-overlay">
  <div class="pwdbox">
    <div class="pwdlock">&#x1F510;</div>
    <div class="pwdtitle">
      <h2>&#25253;&#34920;&#20013;&#24515;</h2>
      <p>&#27492;&#39029;&#38754;&#24050;&#21152;&#23494;&#65292;&#35831;&#36755;&#20837;&#35775;&#38382;&#23494;&#30721;</p>
    </div>
    <input type="password" id="pwd-input" placeholder="&#35831;&#36755;&#20837;&#23494;&#30721;" autofocus onkeydown="if(event.key==='Enter')pwdCheck()">
    <div class="pwderr" id="pwd-err"></div>
    <button class="pwdbtn" onclick="pwdCheck()">&#30830;&#35748;</button>
  </div>
</div>
<script>
(function(){var K='__hst_auth';function h(s){var a=0;for(var i=0;i<s.length;i++){a=((a<<5)-a)+s.charCodeAt(i);a|=0;}return a;}var PH=h('sy18929531199');if(Number(sessionStorage.getItem(K))===PH){document.getElementById('pwd-overlay').remove();}window.pwdCheck=function(){var v=document.getElementById('pwd-input').value;if(h(v)===PH){sessionStorage.setItem(K,PH);document.getElementById('pwd-overlay').remove();}else{document.getElementById('pwd-err').textContent='密码错误，请重试';document.getElementById('pwd-input').select();}};})();
</script>`;

// ── 使用 overlay 注入方式的文件清单 ─────────────────────────────────────────
// AES 加密文件（index.html / sales-channel.html / new-product.html / 万邑通库存管理.html）
// 由各自的构建脚本和 encrypt.js 管理，此处不处理。
const OVERLAY_FILES = [
  '全品销售与退款报告.html',
];

function injectPassword(html) {
  // 移除已有遮罩，再重新注入（幂等）
  html = html.replace(/<style id="pwd-overlay-style">[\s\S]*?<\/script>/g, '');
  html = html.replace(/(<body[^>]*>)/, '$1\n' + PWD_OVERLAY);
  return html;
}

function isAesEncrypted(html) {
  // AES 解密壳特征：含 PBKDF2
  return html.includes('PBKDF2');
}

let ok = 0, skipped = 0, missing = 0;

OVERLAY_FILES.forEach(filename => {
  const filePath = path.join(REPO, filename);
  if (!fs.existsSync(filePath)) {
    console.log(`  [SKIP] not found: ${filename}`);
    missing++;
    return;
  }
  const html = fs.readFileSync(filePath, 'utf8');
  if (isAesEncrypted(html)) {
    console.log(`  [SKIP] AES-encrypted (not overlay-managed): ${filename}`);
    skipped++;
    return;
  }
  const protected_ = injectPassword(html);
  fs.writeFileSync(filePath, protected_, 'utf8');
  console.log(`  [OK]   password overlay applied: ${filename}`);
  ok++;
});

console.log(`\n  protect.js done — applied: ${ok}, skipped: ${skipped}, missing: ${missing}`);
