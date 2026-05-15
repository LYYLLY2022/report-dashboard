"""
Patches generate_report.py - JS table sections to use dynamic hist_months.
Uses function signatures as markers (no special chars).
"""

SCRIPT_PATH = r'C:\Users\liche\AppData\Roaming\WorkBuddy\User\globalStorage\tencent-cloud.coding-copilot\brain\b11f38441fcf41bfa1758005f67019af\generate_report.py'

with open(SCRIPT_PATH, 'r', encoding='utf-8') as f:
    src = f.read()

original = src

def replace_func(content, func_sig, end_sentinel, new_body):
    """Replace from func_sig to end_sentinel (exclusive) with new_body."""
    start = content.find(func_sig)
    if start == -1:
        print(f"  NOT FOUND: {func_sig[:60]!r}")
        return content
    end = content.find(end_sentinel, start)
    if end == -1:
        print(f"  END NOT FOUND for: {func_sig[:60]!r}")
        return content
    print(f"  OK: {func_sig[:40]!r} at {start}-{end}")
    return content[:start] + new_body + content[end:]


# ─────────────────────────────────────────────────────────────────────────────
# 1. initTablePlatformAvg
# ─────────────────────────────────────────────────────────────────────────────
print("Patching initTablePlatformAvg...")
src = replace_func(src,
    'function initTablePlatformAvg() {{',
    '\n// ── Table: Platform',
    '''\
function initTablePlatformAvg() {{
  const el = document.getElementById('table-platform-avg');
  if (!el) return;
  const D = RAW.platform_monthly_avg;
  const curMonthLabel = RAW.company_monthly_avg.cur_month_label;
  const histMonths = RAW.company_monthly_avg.hist_months;

  const rows = D.names.map((name, i) => {{
    const histAvgs = histMonths.map((h, hi) => (D.hist_avgs[hi] || [])[i] || 0);
    const prevAvg = histAvgs[0] || 0;
    const mom = prevAvg > 0 && D.cur_avg[i] > 0 ? ((D.cur_avg[i] - prevAvg) / prevAvg * 100).toFixed(1) : null;
    return {{ name, total: D.cur_total[i], curAvg: D.cur_avg[i], histAvgs, mom }};
  }});

  let html = `<table class="data-table ranking-table">
    <thead>
      <tr>
        <th style="width:60px;">排名</th>
        <th>平台（渠道）</th>
        <th style="text-align:right;">${{curMonthLabel}}销售额<br/><span style="font-weight:normal;font-size:12px;">(USD)</span></th>
        <th style="text-align:right;">${{curMonthLabel}}日均销售额<br/><span style="font-weight:normal;font-size:12px;">(USD/天)</span></th>
        ${{histMonths.map(h => `<th style="text-align:right;">${{h.label}}日均销售额<br/><span style="font-weight:normal;font-size:12px;">(USD/天)</span></th>`).join('')}}
        <th style="text-align:right;">日均销售额<br/>环比</th>
      </tr>
    </thead>
    <tbody>`;

  rows.forEach((row, idx) => {{
    const rank = idx + 1;
    var badgeStyle = '';
    if (rank === 1) badgeStyle = 'background:linear-gradient(135deg,#F59E0B,#FFA500);color:#1a1a2e;';
    else if (rank === 2) badgeStyle = 'background:linear-gradient(135deg,#C0C0C0,#A0A0A0);color:#1a1a2e;';
    else if (rank === 3) badgeStyle = 'background:linear-gradient(135deg,#CD7F32,#A0522D);color:#fff;';
    var rankBadge = rank <= 3
      ? '<span style="display:inline-block;width:28px;height:28px;line-height:28px;border-radius:50%;text-align:center;font-weight:700;font-size:14px;' + badgeStyle + '">' + rank + '</span>'
      : rank;
    const momHtml = row.mom === null
      ? '<span style="color:#9CA3AF;">–</span>'
      : parseFloat(row.mom) > 0
        ? `<span style="color:#F85149;">↑${{row.mom}}%</span>`
        : parseFloat(row.mom) < 0
          ? `<span style="color:#3FB950;">↓${{Math.abs(row.mom)}}%</span>`
          : `<span style="color:#9CA3AF;">→0%</span>`;
    const histTds = row.histAvgs.map(v => `<td style="text-align:right;">${{v > 0 ? fmt(v) : '<span style="color:#9CA3AF;">–</span>'}}</td>`).join('');
    html += `<tr>
      <td style="text-align:center;">${{rankBadge}}</td>
      <td style="font-weight:500;">${{row.name}}</td>
      <td class="num-positive" style="text-align:right;font-size:15px;font-weight:600;">${{fmt(row.total)}}</td>
      <td class="num-positive" style="text-align:right;">${{fmt(row.curAvg)}}</td>
      ${{histTds}}
      <td style="text-align:right;">${{momHtml}}</td>
    </tr>`;
  }});

  html += '</tbody></table>';
  el.innerHTML = html;
}}

''')


# ─────────────────────────────────────────────────────────────────────────────
# 2. initRankingTable
# ─────────────────────────────────────────────────────────────────────────────
print("Patching initRankingTable...")
src = replace_func(src,
    'function initRankingTable() {{',
    '\n// ── Detail Table',
    '''\
function initRankingTable() {{
  const R = RAW.ranking;
  document.getElementById('ranking-cur-days').textContent = R.cur_month_days;
  document.getElementById('ranking-prev-days').textContent = R.prev_month_days;
  const curMonthLabel = R.cur_month + '月';
  const histMonths = RAW.company_monthly_avg.hist_months;

  const histThs = histMonths.map(h => `<th style="text-align:right;">${{h.label}}日均销售额<br/><span style="font-weight:normal;font-size:12px;">(USD/天)</span></th>`).join('');
  let html = `<table class="data-table ranking-table">
    <thead>
      <tr>
        <th style="width:60px;">排名</th>
        <th>运营人员</th>
        <th style="text-align:right;">${{curMonthLabel}}销售额<br/><span style="font-weight:normal;font-size:12px;">(USD)</span></th>
        <th style="text-align:right;">${{curMonthLabel}}日均销售额<br/><span style="font-weight:normal;font-size:12px;">(USD/天)</span></th>
        ${{histThs}}
        <th style="text-align:right;">日均销售额<br/>环比</th>
      </tr>
    </thead>
    <tbody>`;

  R.data.forEach(row => {{
    var badgeStyle = '';
    if (row.rank === 1) badgeStyle = 'background:linear-gradient(135deg,#F59E0B,#FFA500);color:#1a1a2e;';
    else if (row.rank === 2) badgeStyle = 'background:linear-gradient(135deg,#C0C0C0,#A0A0A0);color:#1a1a2e;';
    else if (row.rank === 3) badgeStyle = 'background:linear-gradient(135deg,#CD7F32,#A0522D);color:#fff;';
    var rankBadge = row.rank <= 3
      ? '<span style="display:inline-block;width:28px;height:28px;line-height:28px;border-radius:50%;text-align:center;font-weight:700;font-size:14px;' + badgeStyle + '">' + row.rank + '</span>'
      : row.rank;
    const momHtml = row.mom_change === null
      ? '<span style="color:#9CA3AF;">–</span>'
      : row.mom_change > 0
        ? `<span style="color:#F85149;">↑${{row.mom_change}}%</span>`
        : row.mom_change < 0
          ? `<span style="color:#3FB950;">↓${{Math.abs(row.mom_change)}}%</span>`
          : `<span style="color:#9CA3AF;">→0%</span>`;
    const histTds = (row.hist_avgs || []).map(v => `<td style="text-align:right;">${{v > 0 ? fmt(v) : '<span style="color:#9CA3AF;">–</span>'}}</td>`).join('');
    html += `<tr>
      <td style="text-align:center;">${{rankBadge}}</td>
      <td style="font-weight:500;">${{row.name}}</td>
      <td class="num-positive" style="text-align:right;font-size:15px;font-weight:600;">${{fmt(row.total)}}</td>
      <td class="num-positive" style="text-align:right;">${{fmt(row.cur_avg)}}</td>
      ${{histTds}}
      <td style="text-align:right;">${{momHtml}}</td>
    </tr>`;
  }});

  html += '</tbody></table>';
  document.getElementById('ranking-table-wrap').innerHTML = html;
}}

''')


# ─────────────────────────────────────────────────────────────────────────────
# 3. initGroup1ShopCompare
# ─────────────────────────────────────────────────────────────────────────────
print("Patching initGroup1ShopCompare...")
src = replace_func(src,
    'function initGroup1ShopCompare() {{',
    '\nfunction initGroupPlatformMonthly(',
    '''\
function initGroup1ShopCompare() {{
  const el = document.getElementById('table-g1-shop');
  if (!el) return;
  const curMonthLabel = RAW.company_monthly_avg.cur_month_label;
  const histMonths = RAW.company_monthly_avg.hist_months;
  const rows = RAW.g1_shop_compare;

  const histThs = histMonths.map(h => `<th style="text-align:right;">${{h.label}}日均销售额<br/><span style="font-weight:normal;font-size:12px;">(USD/天)</span></th>`).join('');
  let html = `<table class="data-table ranking-table">
    <thead>
      <tr>
        <th style="width:60px;">排名</th>
        <th>店铺</th>
        <th>渠道</th>
        <th style="text-align:right;">${{curMonthLabel}}日均销售额<br/><span style="font-weight:normal;font-size:12px;">(USD/天)</span></th>
        ${{histThs}}
        <th style="text-align:right;">日均销售额<br/>环比</th>
      </tr>
    </thead>
    <tbody>`;

  rows.forEach((row, idx) => {{
    const rank = idx + 1;
    var badgeStyle = '';
    if (rank === 1) badgeStyle = 'background:linear-gradient(135deg,#F59E0B,#FFA500);color:#1a1a2e;';
    else if (rank === 2) badgeStyle = 'background:linear-gradient(135deg,#C0C0C0,#A0A0A0);color:#1a1a2e;';
    else if (rank === 3) badgeStyle = 'background:linear-gradient(135deg,#CD7F32,#A0522D);color:#fff;';
    var rankBadge = rank <= 3
      ? '<span style="display:inline-block;width:28px;height:28px;line-height:28px;border-radius:50%;text-align:center;font-weight:700;font-size:14px;' + badgeStyle + '">' + rank + '</span>'
      : rank;
    const momHtml = row.mom === null
      ? '<span style="color:#9CA3AF;">–</span>'
      : parseFloat(row.mom) > 0
        ? `<span style="color:#F85149;">↑${{row.mom}}%</span>`
        : parseFloat(row.mom) < 0
          ? `<span style="color:#3FB950;">↓${{Math.abs(row.mom)}}%</span>`
          : `<span style="color:#9CA3AF;">→0%</span>`;
    const histTds = (row.hist_avgs || []).map(v => `<td style="text-align:right;">${{v > 0 ? fmt(v) : '<span style="color:#9CA3AF;">–</span>'}}</td>`).join('');
    html += `<tr>
      <td style="text-align:center;">${{rankBadge}}</td>
      <td style="font-weight:500;">${{row.name}}</td>
      <td>${{row.platform || '<span style="color:#9CA3AF;">–</span>'}}</td>
      <td class="num-positive" style="text-align:right;">${{fmt(row.cur_avg)}}</td>
      ${{histTds}}
      <td style="text-align:right;">${{momHtml}}</td>
    </tr>`;
  }});

  html += '</tbody></table>';
  el.innerHTML = html;

  const titleEl = document.getElementById('g1-shop-title');
  const prevLabel = histMonths.length > 0 ? histMonths[0].label : '';
  if (titleEl) titleEl.textContent = '一组运营 — 各店铺月度日均销售额对比（' + prevLabel + ' vs ' + curMonthLabel + '）';
}}

''')


# ─────────────────────────────────────────────────────────────────────────────
# 4. initGroupPlatformMonthly
# ─────────────────────────────────────────────────────────────────────────────
print("Patching initGroupPlatformMonthly...")
src = replace_func(src,
    'function initGroupPlatformMonthly(dataKey, tableId, titleId, groupLabel) {{',
    '\nfunction initGroupPlatformPie(',
    '''\
function initGroupPlatformMonthly(dataKey, tableId, titleId, groupLabel) {{
  const el = document.getElementById(tableId);
  if (!el) return;
  const curMonthLabel = RAW.company_monthly_avg.cur_month_label;
  const histMonths = RAW.company_monthly_avg.hist_months;
  const rows = RAW[dataKey];

  const histThs = histMonths.map(h => `<th style="text-align:right;">${{h.label}}日均销售额<br/><span style="font-weight:normal;font-size:12px;">(USD/天)</span></th>`).join('');
  let html = `<table class="data-table ranking-table">
    <thead>
      <tr>
        <th style="width:60px;">排名</th>
        <th>平台（渠道）</th>
        <th style="text-align:right;">${{curMonthLabel}}销售额<br/><span style="font-weight:normal;font-size:12px;">(USD)</span></th>
        <th style="text-align:right;">${{curMonthLabel}}日均销售额<br/><span style="font-weight:normal;font-size:12px;">(USD/天)</span></th>
        ${{histThs}}
        <th style="text-align:right;">日均销售额<br/>环比</th>
      </tr>
    </thead>
    <tbody>`;

  rows.forEach((row, idx) => {{
    const rank = idx + 1;
    var badgeStyle = '';
    if (rank === 1) badgeStyle = 'background:linear-gradient(135deg,#F59E0B,#FFA500);color:#1a1a2e;';
    else if (rank === 2) badgeStyle = 'background:linear-gradient(135deg,#C0C0C0,#A0A0A0);color:#1a1a2e;';
    else if (rank === 3) badgeStyle = 'background:linear-gradient(135deg,#CD7F32,#A0522D);color:#fff;';
    var rankBadge = rank <= 3
      ? '<span style="display:inline-block;width:28px;height:28px;line-height:28px;border-radius:50%;text-align:center;font-weight:700;font-size:14px;' + badgeStyle + '">' + rank + '</span>'
      : rank;
    const momHtml = row.mom === null
      ? '<span style="color:#9CA3AF;">–</span>'
      : parseFloat(row.mom) > 0
        ? `<span style="color:#F85149;">↑${{row.mom}}%</span>`
        : parseFloat(row.mom) < 0
          ? `<span style="color:#3FB950;">↓${{Math.abs(row.mom)}}%</span>`
          : `<span style="color:#9CA3AF;">→0%</span>`;
    const histTds = (row.hist_avgs || []).map(v => `<td style="text-align:right;">${{v > 0 ? fmt(v) : '<span style="color:#9CA3AF;">–</span>'}}</td>`).join('');
    html += `<tr>
      <td style="text-align:center;">${{rankBadge}}</td>
      <td style="font-weight:500;">${{row.name}}</td>
      <td class="num-positive" style="text-align:right;font-size:15px;font-weight:600;">${{fmt(row.cur_total)}}</td>
      <td class="num-positive" style="text-align:right;">${{fmt(row.cur_avg)}}</td>
      ${{histTds}}
      <td style="text-align:right;">${{momHtml}}</td>
    </tr>`;
  }});

  html += '</tbody></table>';
  el.innerHTML = html;

  const titleEl = document.getElementById(titleId);
  const prevLabel = histMonths.length > 0 ? histMonths[0].label : '';
  if (titleEl) titleEl.textContent = groupLabel + ' — 各渠道月度日均销售额对比（' + prevLabel + ' vs ' + curMonthLabel + '）';
}}

''')


# ─────────────────────────────────────────────────────────────────────────────
# 5. initGroupShopCompare
# ─────────────────────────────────────────────────────────────────────────────
print("Patching initGroupShopCompare...")
src = replace_func(src,
    'function initGroupShopCompare(shopKey, tableId, titleId, groupLabel) {{',
    '\nfunction initGroupCharts(',
    '''\
function initGroupShopCompare(shopKey, tableId, titleId, groupLabel) {{
  const el = document.getElementById(tableId);
  if (!el) return;
  const curMonthLabel = RAW.company_monthly_avg.cur_month_label;
  const histMonths = RAW.company_monthly_avg.hist_months;
  const rows = RAW[shopKey];

  const histThs = histMonths.map(h => `<th style="text-align:right;">${{h.label}}日均销售额<br/><span style="font-weight:normal;font-size:12px;">(USD/天)</span></th>`).join('');
  let html = `<table class="data-table ranking-table">
    <thead>
      <tr>
        <th style="width:60px;">排名</th>
        <th>店铺</th>
        <th>渠道</th>
        <th style="text-align:right;">${{curMonthLabel}}日均销售额<br/><span style="font-weight:normal;font-size:12px;">(USD/天)</span></th>
        ${{histThs}}
        <th style="text-align:right;">日均销售额<br/>环比</th>
      </tr>
    </thead>
    <tbody>`;

  rows.forEach((row, idx) => {{
    const rank = idx + 1;
    var badgeStyle = '';
    if (rank === 1) badgeStyle = 'background:linear-gradient(135deg,#F59E0B,#FFA500);color:#1a1a2e;';
    else if (rank === 2) badgeStyle = 'background:linear-gradient(135deg,#C0C0C0,#A0A0A0);color:#1a1a2e;';
    else if (rank === 3) badgeStyle = 'background:linear-gradient(135deg,#CD7F32,#A0522D);color:#fff;';
    var rankBadge = rank <= 3
      ? '<span style="display:inline-block;width:28px;height:28px;line-height:28px;border-radius:50%;text-align:center;font-weight:700;font-size:14px;' + badgeStyle + '">' + rank + '</span>'
      : rank;
    const momHtml = row.mom === null
      ? '<span style="color:#9CA3AF;">–</span>'
      : parseFloat(row.mom) > 0
        ? `<span style="color:#F85149;">↑${{row.mom}}%</span>`
        : parseFloat(row.mom) < 0
          ? `<span style="color:#3FB950;">↓${{Math.abs(row.mom)}}%</span>`
          : `<span style="color:#9CA3AF;">→0%</span>`;
    const histTds = (row.hist_avgs || []).map(v => `<td style="text-align:right;">${{v > 0 ? fmt(v) : '<span style="color:#9CA3AF;">–</span>'}}</td>`).join('');
    html += `<tr>
      <td style="text-align:center;">${{rankBadge}}</td>
      <td style="font-weight:500;">${{row.name}}</td>
      <td>${{row.platform || '<span style="color:#9CA3AF;">–</span>'}}</td>
      <td class="num-positive" style="text-align:right;">${{fmt(row.cur_avg)}}</td>
      ${{histTds}}
      <td style="text-align:right;">${{momHtml}}</td>
    </tr>`;
  }});

  html += '</tbody></table>';
  el.innerHTML = html;

  const titleEl = document.getElementById(titleId);
  const prevLabel = histMonths.length > 0 ? histMonths[0].label : '';
  if (titleEl) titleEl.textContent = groupLabel + ' — 各店铺月度日均销售额对比（' + prevLabel + ' vs ' + curMonthLabel + '）';
}}

''')


# ─────────────────────────────────────────────────────────────────────────────
# 6. initGroupCharts - replace entire function (avg table uses hist_avgs)
# ─────────────────────────────────────────────────────────────────────────────
print("Patching initGroupCharts...")
src = replace_func(src,
    'function initGroupCharts(groupIdx, avgTableId, pieKey, pieChartId, pieTitleId, shopKey, shopTableId, shopTitleId, groupLabel) {{',
    '\nfunction initGroupDailyTrend(',
    '''\
function initGroupCharts(groupIdx, avgTableId, pieKey, pieChartId, pieTitleId, shopKey, shopTableId, shopTitleId, groupLabel) {{
  const gNames = RAW.group_names;
  const gName = gNames[groupIdx];
  if (!gName || !RAW.group_op_stats[gName]) return;
  const gData = RAW.group_op_stats[gName];

  // ── 月度日均销售额对比表格 ──
  const avgTableEl = document.getElementById(avgTableId);
  if (avgTableEl) {{
    const curMonthLabel = RAW.company_monthly_avg.cur_month_label;
    const histMonths = RAW.company_monthly_avg.hist_months;

    // Build lookup map for each historical month: name -> avg value
    const histAvgMaps = (gData.hist_avgs || []).map(h => {{
      const m = {{}};
      (h.names || []).forEach((n, i) => {{ m[n] = h.values[i]; }});
      return m;
    }});

    const curNames = gData.avg.names;
    const curAvgValues = gData.avg.values;
    const totalMap = {{}};
    gData.rank.names.forEach((n, i) => {{ totalMap[n] = gData.rank.values[i]; }});

    const rows = curNames.map((name, i) => {{
      const histAvgs = histAvgMaps.map(m => m[name] || 0);
      const prevAvg = histAvgs[0] || 0;
      const mom = prevAvg > 0 && curAvgValues[i] > 0 ? ((curAvgValues[i] - prevAvg) / prevAvg * 100).toFixed(1) : null;
      return {{ name, total: totalMap[name] || 0, curAvg: curAvgValues[i], histAvgs, mom }};
    }}).sort((a, b) => b.curAvg - a.curAvg);

    const histThs = histMonths.map(h => `<th style="text-align:right;">${{h.label}}日均销售额<br/><span style="font-weight:normal;font-size:12px;">(USD/天)</span></th>`).join('');
    let html = `<table class="data-table ranking-table">
      <thead>
        <tr>
          <th style="width:60px;">排名</th>
          <th>运营人员</th>
          <th style="text-align:right;">${{curMonthLabel}}销售额<br/><span style="font-weight:normal;font-size:12px;">(USD)</span></th>
          <th style="text-align:right;">${{curMonthLabel}}日均销售额<br/><span style="font-weight:normal;font-size:12px;">(USD/天)</span></th>
          ${{histThs}}
          <th style="text-align:right;">日均销售额<br/>环比</th>
        </tr>
      </thead>
      <tbody>`;

    rows.forEach((row, idx) => {{
      const rank = idx + 1;
      var badgeStyle = '';
      if (rank === 1) badgeStyle = 'background:linear-gradient(135deg,#F59E0B,#FFA500);color:#1a1a2e;';
      else if (rank === 2) badgeStyle = 'background:linear-gradient(135deg,#C0C0C0,#A0A0A0);color:#1a1a2e;';
      else if (rank === 3) badgeStyle = 'background:linear-gradient(135deg,#CD7F32,#A0522D);color:#fff;';
      var rankBadge = rank <= 3
        ? '<span style="display:inline-block;width:28px;height:28px;line-height:28px;border-radius:50%;text-align:center;font-weight:700;font-size:14px;' + badgeStyle + '">' + rank + '</span>'
        : rank;
      const momHtml = row.mom === null
        ? '<span style="color:#9CA3AF;">—</span>'
        : parseFloat(row.mom) > 0
          ? `<span style="color:#F85149;">▲ ${{row.mom}}%</span>`
          : parseFloat(row.mom) < 0
            ? `<span style="color:#3FB950;">▼ ${{Math.abs(row.mom)}}%</span>`
            : `<span style="color:#9CA3AF;">— 0%</span>`;
      const histTds = row.histAvgs.map(v => `<td style="text-align:right;">${{v > 0 ? fmt(v) : '<span style="color:#9CA3AF;">—</span>'}}</td>`).join('');
      html += `<tr>
        <td style="text-align:center;">${{rankBadge}}</td>
        <td style="font-weight:500;">${{row.name}}</td>
        <td class="num-positive" style="text-align:right;font-size:15px;font-weight:600;">${{fmt(row.total)}}</td>
        <td class="num-positive" style="text-align:right;">${{fmt(row.curAvg)}}</td>
        ${{histTds}}
        <td style="text-align:right;">${{momHtml}}</td>
      </tr>`;
    }});
    html += '</tbody></table>';
    avgTableEl.innerHTML = html;
  }}

  initGroupPlatformPie(groupIdx, pieKey, pieChartId, pieTitleId, groupLabel);
  initGroupShopCompare(shopKey, shopTableId, shopTitleId, groupLabel);
}}

''')


# ─────────────────────────────────────────────────────────────────────────────
# Write
# ─────────────────────────────────────────────────────────────────────────────
if src == original:
    print("\nWARNING: No changes made!")
else:
    with open(SCRIPT_PATH, 'w', encoding='utf-8') as f:
        f.write(src)
    print(f"\nDone. Written: {SCRIPT_PATH}")
