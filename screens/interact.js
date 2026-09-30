/* Brand Beacon mockups: shared interactions. Each page sets <body data-page="...">.
   Data here is the same sample/live data the mockups already show. */
(function () {
  var Y = '#FFC72C', YT = '#1A1300', MUTED = '#5E5A52';
  var page = document.body.getAttribute('data-page');
  var live = window.self === window.top || /[?&]live=1/.test(location.search);

  // ---------- toast ----------
  var toastEl;
  function toast(msg) {
    if (!toastEl) {
      toastEl = document.createElement('div');
      toastEl.setAttribute('role', 'status');
      toastEl.style.cssText = 'position:fixed;left:50%;bottom:28px;transform:translateX(-50%) translateY(20px);z-index:100;background:#0B0B0B;color:#fff;font:600 14px Figtree,system-ui,sans-serif;padding:11px 18px;border-radius:999px;box-shadow:0 8px 24px rgba(0,0,0,.2);opacity:0;transition:all .2s;pointer-events:none;max-width:80vw;text-align:center;';
      document.body.appendChild(toastEl);
    }
    toastEl.textContent = msg;
    toastEl.style.opacity = 1; toastEl.style.transform = 'translateX(-50%) translateY(0)';
    clearTimeout(toastEl._t);
    toastEl._t = setTimeout(function () { toastEl.style.opacity = 0; toastEl.style.transform = 'translateX(-50%) translateY(20px)'; }, 2200);
  }
  window.bbToast = toast;

  // ---------- pill groups: [data-pills] ----------
  function setPill(btn) {
    var g = btn.closest('[data-pills]'); if (!g) return;
    [].forEach.call(g.querySelectorAll('button'), function (b) {
      var on = b === btn;
      b.style.background = on ? Y : 'transparent';
      b.style.color = on ? YT : MUTED;
      b.setAttribute('aria-pressed', on ? 'true' : 'false');
    });
  }
  document.addEventListener('click', function (e) {
    var b = e.target.closest('[data-pills] button');
    if (b) { setPill(b); var g = b.closest('[data-pills]'); g.dispatchEvent(new CustomEvent('pill', { detail: b.textContent.trim(), bubbles: true })); }
  });

  // ---------- bookmarks: [aria-label=Save] ----------
  var BOOK_ON = '<svg width="17" height="17" viewBox="0 0 24 24" fill="currentColor" stroke="currentColor" stroke-width="1.8" stroke-linejoin="round" aria-hidden="true"><path d="M7 4h10v16l-5-3.5L7 20z"></path></svg>';
  document.addEventListener('click', function (e) {
    var a = e.target.closest('[aria-label="Save"]'); if (!a) return;
    e.preventDefault();
    if (!a._off) a._off = a.innerHTML;
    var on = a.getAttribute('data-saved') !== '1';
    a.setAttribute('data-saved', on ? '1' : '0');
    a.innerHTML = on ? BOOK_ON : a._off;
    a.style.background = on ? '#FFF6D6' : '';
    a.style.color = on ? '#6B4B00' : '';
    a.style.borderColor = on ? '#F5DD92' : '';
    toast(on ? 'Saved to Library' : 'Removed from Library');
  });

  // ---------- share + analysis open the live share flow ----------
  document.addEventListener('click', function (e) {
    var s = e.target.closest('[aria-label="Share"]');
    if (s) { e.preventDefault(); window.open('share-flow.html#share', '_blank'); return; }
    var v = e.target.closest('[data-view-analysis], a[href="share-this-video.html"]');
    if (v) { e.preventDefault(); window.open('share-flow.html', '_blank'); }
  });

  // ---------- analyze: spinner, then View analysis; uses one breakdown ----------
  function bumpMeter() {
    var used = document.querySelector('[data-meter-used]'), bar = document.querySelector('[data-meter-bar]');
    if (!used) return;
    var n = +used.textContent + 1; used.textContent = n;
    if (bar) bar.style.width = n + '%';
  }
  document.addEventListener('click', function (e) {
    var b = e.target.closest('button'); if (!b || !/^\s*Analyze video/.test(b.textContent) || b._busy) return;
    b._busy = true;
    var h = b.innerHTML;
    b.innerHTML = '<span style="width:14px;height:14px;border-radius:50%;border:2px solid rgba(0,0,0,.25);border-top-color:#1A1300;display:inline-block;animation:bbspin .7s linear infinite;"></span>Analyzing';
    setTimeout(function () {
      b.innerHTML = h.replace('Analyze video', 'View analysis');
      b.style.background = '#fff'; b.style.border = '1px solid ' + Y; b.style.boxShadow = 'none';
      b.setAttribute('data-view-analysis', '1');
      b._busy = false; bumpMeter(); toast('Analysis ready. 1 breakdown used.');
    }, 1300);
  });
  var st = document.createElement('style');
  st.textContent = '@keyframes bbspin{to{transform:rotate(360deg)}}';
  document.head.appendChild(st);

  // ---------- links that lead to pages outside the mockup ----------
  document.addEventListener('click', function (e) {
    var a = e.target.closest('a[href="#"]');
    if (!a || e.defaultPrevented || a.hasAttribute('data-handled')) return;
    e.preventDefault();
    var t = a.textContent.trim();
    toast(t ? '“' + t + '” opens its own page, not part of this mockup' : 'Not part of this mockup');
  });

  // ---------- dropdown menu helper ----------
  function menu(anchor, options, current, onPick) {
    closeMenus();
    var r = anchor.getBoundingClientRect();
    var m = document.createElement('div');
    m.className = 'bbmenu';
    m.style.cssText = 'position:fixed;z-index:90;left:' + r.left + 'px;top:' + (r.bottom + 6) + 'px;min-width:' + r.width + 'px;background:#fff;border:1px solid #ECE9E1;border-radius:14px;box-shadow:0 12px 32px rgba(23,21,15,.16);padding:6px;font:600 13.5px Figtree,system-ui,sans-serif;';
    options.forEach(function (o) {
      var i = document.createElement('button');
      i.textContent = o;
      i.style.cssText = 'display:block;width:100%;text-align:left;border:0;background:' + (o === current ? '#FFF6D6' : 'transparent') + ';padding:9px 12px;border-radius:9px;font:inherit;cursor:pointer;color:#0B0B0B;';
      i.onmouseenter = function () { if (o !== current) i.style.background = '#F5F4F0'; };
      i.onmouseleave = function () { if (o !== current) i.style.background = 'transparent'; };
      i.onclick = function (ev) { ev.stopPropagation(); closeMenus(); onPick(o); };
      m.appendChild(i);
    });
    document.body.appendChild(m);
    setTimeout(function () { document.addEventListener('click', closeMenus, { once: true }); }, 0);
  }
  function closeMenus() { [].forEach.call(document.querySelectorAll('.bbmenu'), function (m) { m.remove(); }); }
  window.bbMenu = menu;

  // ---------- run a search (feed + slim bar) ----------
  function runSearch(q) {
    q = (q || '').trim();
    if (!q) { toast('Type a brand or a product first'); return; }
    toast('Searching “' + q + '”. It lands in Your searches.');
    var list = document.querySelector('[data-your-searches]');
    if (list && !list.querySelector('[data-q="' + q + '"]')) {
      var row = document.createElement('div');
      row.className = 'row'; row.setAttribute('data-q', q);
      row.style.cssText = 'gap:10px;margin-top:10px;';
      row.innerHTML = '<span class="av" style="width:30px;height:30px;font-size:11px;">' + q.slice(0, 2).toUpperCase() + '</span><div style="display:flex;flex-direction:column;line-height:1.3;"><b style="font-size:14px;">' + q + '</b><span style="font-size:12px;color:#6B675F;">Searching now, about 1 minute</span></div>';
      list.appendChild(row);
    }
  }
  document.addEventListener('click', function (e) {
    var chip = e.target.closest('[data-try]');
    if (chip) {
      e.preventDefault();
      var q = chip.getAttribute('data-try');
      [].forEach.call(document.querySelectorAll('input[aria-label="Search a brand or product"]'), function (i) { i.value = q; });
      var big = document.querySelector('#bigsearch input'); if (big) big.focus();
      toast('“' + q + '” is in the search box. Press Find breakouts.');
      return;
    }
    var fb = e.target.closest('button');
    if (fb && /Find breakouts/.test(fb.textContent)) {
      var inp = fb.parentNode.querySelector('input'); runSearch(inp && inp.value);
    }
  });
  document.addEventListener('keydown', function (e) {
    if (e.key === 'Enter' && e.target.matches('input[aria-label="Search a brand or product"]')) runSearch(e.target.value);
    if (e.key === 'Escape') { closeMenus(); var p = document.querySelector('[data-export-panel]'); if (p && p.getAttribute('data-open') === '1') toggleExport(false); }
  });

  // ---------- export panel (readout) ----------
  function toggleExport(open) {
    var p = document.querySelector('[data-export-panel]'), dim = document.querySelector('[data-export-dim]'), btn = document.querySelector('[data-export-btn]');
    if (!p) return;
    p.style.display = open ? 'flex' : 'none'; if (dim) dim.style.display = open ? 'block' : 'none';
    p.setAttribute('data-open', open ? '1' : '0');
    if (btn) { btn.style.background = open ? '#0B0B0B' : '#fff'; btn.style.color = open ? '#fff' : '#0B0B0B'; btn.style.borderColor = open ? '#0B0B0B' : ''; btn.setAttribute('aria-expanded', open ? 'true' : 'false'); }
  }
  window.bbToggleExport = toggleExport;
  document.addEventListener('click', function (e) {
    if (e.target.closest('[data-export-btn]')) { e.stopPropagation(); var p = document.querySelector('[data-export-panel]'); toggleExport(p.getAttribute('data-open') !== '1'); return; }
    var p2 = document.querySelector('[data-export-panel]');
    if (p2 && p2.getAttribute('data-open') === '1' && !e.target.closest('[data-export-panel]') && !e.target.closest('.bbmenu')) toggleExport(false);
  });
  var EXPORT_ROWS = [
    ['@cyr1n32', 'https://www.tiktok.com/@cyr1n32', 'https://www.tiktok.com/@cyr1n32/video/', '8.6K', '8.9M', '1.6K'],
    ['@_ellapalmer_', 'https://www.tiktok.com/@_ellapalmer_', 'https://www.tiktok.com/@_ellapalmer_/video/', '7.1K', '19.7M', '3.8K'],
    ['@em_ireland', 'https://www.tiktok.com/@em_ireland', 'https://www.tiktok.com/@em_ireland/video/', '6.2K', '4.8M', '905'],
    ['@justemma529', 'https://www.tiktok.com/@justemma529', 'https://www.tiktok.com/@justemma529/video/', '5.9K', '4M', '891'],
    ['@jordannsagee', 'https://www.tiktok.com/@jordannsagee', 'https://www.tiktok.com/@jordannsagee/video/', '4.2K', '3.1M', '772']
  ];
  var HEAD = ['Creator', 'Profile URL', 'Best breakout URL', 'Breakout Score', 'Views', 'Followers'];
  document.addEventListener('click', function (e) {
    var b = e.target.closest('[data-export-copy]');
    if (b) {
      var tsv = [HEAD].concat(EXPORT_ROWS).map(function (r) { return r.join('\t'); }).join('\n');
      try { navigator.clipboard.writeText(tsv); } catch (err) {}
      b.lastChild.textContent = 'Copied'; setTimeout(function () { b.lastChild.textContent = 'Copy list'; }, 1800);
      toast('Copied. Paste it into a sheet.');
      return;
    }
    var d = e.target.closest('[data-export-csv]');
    if (d) {
      var csv = [HEAD].concat(EXPORT_ROWS).map(function (r) { return r.map(function (c) { return '"' + c + '"'; }).join(','); }).join('\n');
      var url = URL.createObjectURL(new Blob([csv], { type: 'text/csv' }));
      var a = document.createElement('a'); a.href = url; a.download = 'rhode-skin-creators.csv'; document.body.appendChild(a); a.click(); a.remove();
      setTimeout(function () { URL.revokeObjectURL(url); }, 1000);
      toast('rhode-skin-creators.csv downloaded (sample rows)');
    }
  });

  // ---------- page-specific ----------
  var P = {};

  P.feed = function () {
    var root = document.getElementById('root');
    if (!root) return;
    if (live) { root.style.height = 'auto'; root.style.minHeight = '100vh'; }
    // infinite scroll: repeat the plain cards a few times, then say so
    var col = document.querySelector('[data-feed]'), peek = document.querySelector('[data-feed-peek]');
    if (!col || !live || !('IntersectionObserver' in window)) return;
    var pool = [].slice.call(col.querySelectorAll('article')).map(function (a) { return a.outerHTML; });
    var batches = 0, end = document.createElement('p');
    end.style.cssText = 'text-align:center;margin:8px 0 24px;font-size:13px;color:#6B675F;';
    end.textContent = 'Loading more breakouts…';
    col.appendChild(end);
    if (peek) peek.style.display = 'none';
    new IntersectionObserver(function (en) {
      if (!en[0].isIntersecting) return;
      if (batches >= 3) { end.textContent = 'You are all caught up. New breakouts land after the next refresh, Sep 25.'; return; }
      batches++;
      pool.slice(0, 3).forEach(function (h) {
        var t = document.createElement('div'); t.innerHTML = h;
        var a = t.firstChild; var strip = a.querySelector('[data-activity]'); if (strip) strip.remove();
        a.style.opacity = 0; a.style.transition = 'opacity .3s'; col.insertBefore(a, end);
        requestAnimationFrame(function () { a.style.opacity = 1; });
      });
      pool.push(pool.shift()); pool.push(pool.shift()); pool.push(pool.shift());
    }, { rootMargin: '300px' }).observe(end);
  };

  P.readout = function () {
    var root = document.getElementById('root');
    if (live && root && !document.body.hasAttribute('data-fixed')) { root.style.height = 'auto'; }
    // analytics measure tabs
    var tabs = document.querySelector('[data-measure-tabs]');
    if (tabs) tabs.addEventListener('pill', function (e) {
      var m = e.detail.toLowerCase();
      [].forEach.call(document.querySelectorAll('[data-measure]'), function (el) { el.style.display = el.getAttribute('data-measure') === m ? '' : 'none'; });
    });
    // refresh + sort menus
    var grid = document.querySelector('[data-grid]');
    [].forEach.call(document.querySelectorAll('[data-dd]'), function (chip) {
      chip.addEventListener('click', function (e) {
        e.stopPropagation();
        var kind = chip.getAttribute('data-dd'), val = chip.querySelector('b');
        var opts = kind === 'sort' ? ['Breakout Score', 'Views', 'Newest'] : ['This refresh, Sep 18', 'Last refresh, Sep 11', 'All runs'];
        menu(chip, opts, val.textContent, function (o) {
          val.textContent = o;
          if (kind === 'sort' && grid) {
            var key = { 'Breakout Score': 'score', 'Views': 'views', 'Newest': 'date' }[o];
            var cards = [].slice.call(grid.children);
            cards.sort(function (a, b) { return (+b.getAttribute('data-' + key)) - (+a.getAttribute('data-' + key)); });
            cards.forEach(function (c) { grid.appendChild(c); });
            toast('Sorted by ' + o.toLowerCase());
          } else toast('Showing ' + o.toLowerCase() + '. Same sample videos in this mockup.');
        });
      });
    });
    // show all
    var more = document.querySelector('[data-show-more]'), extra = document.querySelector('[data-extra-cards]');
    if (more && extra && grid) more.addEventListener('click', function () {
      if (extra.children.length) {
        while (extra.children.length) grid.appendChild(extra.children[0]);
        more.textContent = 'Showing 5 of 55 · The rest load as you scroll';
        more.style.pointerEvents = 'none'; more.style.borderColor = 'transparent'; more.style.background = 'transparent'; more.style.color = '#6B675F';
        if (root && !live) root.style.height = (root.offsetHeight + 740) + 'px';
      }
    });
    if (document.body.getAttribute('data-open-export') === '1') toggleExport(true);
  };

  P.admin = function () {
    var root = document.querySelector('.app');
    // range pills swap the momentum chart and the date line
    var rg = document.querySelector('[data-range]');
    if (rg) rg.addEventListener('pill', function (e) {
      var r = e.detail, map = { '1D': '1', '3D': '3', '7D': '7', '30D': '30' };
      var key = map[r] || '30';
      [].forEach.call(document.querySelectorAll('[data-days]'), function (el) { el.style.display = el.getAttribute('data-days') === key ? '' : 'none'; });
      var label = { '1': 'Sep 18, 2026', '3': 'Sep 16 to Sep 18, 2026', '7': 'Sep 12 to Sep 18, 2026', '30': 'Aug 20 to Sep 18, 2026' }[key];
      var d = document.querySelector('[data-range-label]'); if (d) d.textContent = label;
      toast(map[r] ? 'Range: ' + label : 'This snapshot only holds 30 days, so ' + r + ' shows the last 30');
    });
    // series toggles
    [].forEach.call(document.querySelectorAll('[data-series-toggle]'), function (b) {
      b.addEventListener('click', function () {
        var s = b.getAttribute('data-series-toggle'), off = b.getAttribute('data-off') !== '1';
        b.setAttribute('data-off', off ? '1' : '0');
        b.style.opacity = off ? .45 : 1; b.style.textDecoration = off ? 'line-through' : 'none';
        [].forEach.call(document.querySelectorAll('[data-series="' + s + '"]'), function (el) { el.style.display = off ? 'none' : ''; });
      });
    });
    // activity filters
    var af = document.querySelector('[data-activity-filter]');
    if (af) af.addEventListener('pill', function (e) {
      var f = e.detail, shown = 0;
      [].forEach.call(document.querySelectorAll('[data-type]'), function (li) {
        var ok = f === 'All' || li.getAttribute('data-type') === f; li.style.display = ok ? '' : 'none'; if (ok) shown++;
      });
      var empty = document.querySelector('[data-activity-empty]'); if (empty) empty.style.display = shown ? 'none' : 'block';
    });
    // refresh data
    var rf = document.querySelector('[data-refresh]');
    if (rf) rf.addEventListener('click', function () {
      var ic = rf.querySelector('svg'); if (ic) { ic.style.transition = 'transform .8s'; ic.style.transform = 'rotate(360deg)'; setTimeout(function () { ic.style.transition = 'none'; ic.style.transform = 'none'; }, 850); }
      var l = document.querySelector('[data-snapshot]'); setTimeout(function () { if (l) l.textContent = 'Refreshed just now'; toast('Data refreshed'); }, 850);
    });
    // team switch
    [].forEach.call(document.querySelectorAll('.switch'), function (sw) {
      sw.style.cursor = 'pointer';
      sw.addEventListener('click', function () {
        var k = sw.querySelector('.sw'), on = sw.getAttribute('data-on') !== '1';
        sw.setAttribute('data-on', on ? '1' : '0');
        k.style.background = on ? '#0B0B0B' : '';
        k.style.setProperty('--x', on ? '14px' : '0');
        k.classList.toggle('on', on);
        toast(on ? 'Team and comped accounts included' : 'Team and comped accounts left out');
      });
    });
  };

  if (P[page]) P[page]();
})();
