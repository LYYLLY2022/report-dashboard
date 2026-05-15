param([string]$file, [string]$titleCode)
# All text is pure ASCII: Chinese words use HTML entities or JS \uXXXX escapes
# so this script works correctly regardless of PowerShell 5.1 file encoding on GBK systems.

if ($titleCode -eq 'new-product') {
    $title = '&#26032;&#21697;&#39318;&#21333;&#20998;&#26512;'
} elseif ($titleCode -eq 'sales-channel') {
    $title = '&#38750;&#20122;&#28192;&#36947;&#19994;&#32489;&#25253;&#21578;'
} else {
    $title = '&#20840;&#21697;&#38144;&#21806;&#20014;&#36864;&#27438;&#25253;&#21578;'
}
$subtitle = '&#27492;&#39029;&#38754;&#24050;&#21152;&#23494;&#65292;&#35831;&#36755;&#20837;&#35775;&#38382;&#23494;&#30721;'
$ph       = '&#35831;&#36755;&#20837;&#23494;&#30721;'
$btn      = '&#30830;&#35748;'

$overlay = @"
<style id="pwd-overlay-style">
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
    <div class="pwdtitle"><h2>$title</h2><p>$subtitle</p></div>
    <input type="password" id="pwd-input" placeholder="$ph" autofocus onkeydown="if(event.key==='Enter')pwdCheck()">
    <div class="pwderr" id="pwd-err"></div>
    <button class="pwdbtn" onclick="pwdCheck()">$btn</button>
  </div>
</div>
<script>
(function(){var K='__hst_auth';function h(s){var a=0;for(var i=0;i<s.length;i++){a=((a<<5)-a)+s.charCodeAt(i);a|=0;}return a;}var PH=h('sy18929531199');if(Number(sessionStorage.getItem(K))===PH){document.getElementById('pwd-overlay').remove();}window.pwdCheck=function(){var v=document.getElementById('pwd-input').value;if(h(v)===PH){sessionStorage.setItem(K,PH);document.getElementById('pwd-overlay').remove();}else{document.getElementById('pwd-err').textContent='\u5bc6\u7801\u9519\u8bef\uff0c\u8bf7\u91cd\u8bd5';document.getElementById('pwd-input').select();}};})();
</script>
"@

$content = [System.IO.File]::ReadAllText($file, [System.Text.Encoding]::UTF8)

# Remove any existing (possibly garbled) overlay block
$content = $content -replace '(?s)<style id="pwd-overlay-style">.*?</script>', ''

# Insert after <body> tag
$newContent = $content -replace '(<body[^>]*>)', "`$1`n$overlay"
[System.IO.File]::WriteAllText($file, $newContent, [System.Text.Encoding]::UTF8)
Write-Host "OK: $file"
