// Shared navbar + footer injection (EN / 繁中), mobile menu, scroll reveal.
(function () {
  const page = document.body.dataset.page || '';
  const isZh = (document.documentElement.lang || '').toLowerCase().startsWith('zh');
  const file = location.pathname.split('/').pop() || 'index.html';
  const enHref = isZh ? '../' + file : file;
  const zhHref = isZh ? file : 'zh-tw/' + file;

  const T = isZh ? {
    home: '首頁', competition: '競賽內容', resources: '學習與算力', faq: '常見問題', register: '報名',
    tagline: '具身雙臂操作競賽：雙 SO-101 版本。模擬 → 跨站驗證 → 實機評測。',
    pages: '頁面', tracks: '賽道', participate: '參加',
    t1: '線纜佈線', t2: '導熱墊取放', t3: '服務機器人挑戰',
    dates: '重要日期', contact: '聯絡我們',
    copy: '© 2026 EBiM-Lite 籌備委員會', final: '決賽 · GTC Taipei · 2027 年 5 月',
  } : {
    home: 'Home', competition: 'Competition', resources: 'Learning & Compute', faq: 'FAQ', register: 'Register',
    tagline: 'Embodied Bimanual Manipulation Competition — Dual SO-101 adaptation. Simulation → Cross-Site Validation → Real-World Evaluation.',
    pages: 'Pages', tracks: 'Tracks', participate: 'Participate',
    t1: 'Cable Routing', t2: 'Thermal Pad Pick-and-Place', t3: 'Service Robot Challenge',
    dates: 'Important Dates', contact: 'Contact',
    copy: '© 2026 EBiM-Lite Organizing Committee', final: 'Final at GTC Taipei · May 2027',
  };

  const links = [
    ['index.html', T.home, 'home'],
    ['competition.html', T.competition, 'competition'],
    ['resources.html', T.resources, 'resources'],
    ['faq.html', T.faq, 'faq'],
  ];

  const nav = document.getElementById('site-nav');
  if (nav) {
    nav.innerHTML = `
      <div class="container">
        <a class="nav-logo" href="index.html">EBiM<span>-Lite</span> 2026</a>
        <button class="nav-toggle" aria-label="Menu" aria-expanded="false">☰</button>
        <ul class="nav-links">
          ${links.map(([href, label, key]) =>
            `<li><a href="${href}"${key === page ? ' class="active"' : ''}>${label}</a></li>`).join('')}
          <li><a class="nav-cta" href="index.html#register">${T.register}</a></li>
          <li class="lang-switch">
            <a href="${enHref}" hreflang="en"${isZh ? '' : ' class="cur"'}>EN</a>
            <a href="${zhHref}" hreflang="zh-Hant"${isZh ? ' class="cur"' : ''}>繁中</a>
          </li>
        </ul>
      </div>`;
    const toggle = nav.querySelector('.nav-toggle');
    const list = nav.querySelector('.nav-links');
    toggle.addEventListener('click', () => {
      const open = list.classList.toggle('open');
      toggle.setAttribute('aria-expanded', open);
    });
    list.addEventListener('click', (e) => { if (e.target.tagName === 'A') list.classList.remove('open'); });
  }

  const footer = document.getElementById('site-footer');
  if (footer) {
    footer.innerHTML = `
      <div class="container">
        <div class="cols">
          <div>
            <a class="nav-logo" href="index.html">EBiM<span>-Lite</span> 2026</a>
            <p style="margin-top:12px">${T.tagline}</p>
          </div>
          <div>
            <h4>${T.pages}</h4>
            <ul>${links.map(([href, label]) => `<li><a href="${href}">${label}</a></li>`).join('')}</ul>
          </div>
          <div>
            <h4>${T.tracks}</h4>
            <ul>
              <li><a href="competition.html#track1">${T.t1}</a></li>
              <li><a href="competition.html#track2">${T.t2}</a></li>
              <li><a href="competition.html#track3">${T.t3}</a></li>
            </ul>
          </div>
          <div>
            <h4>${T.participate}</h4>
            <ul>
              <li><a href="index.html#register">${T.register}</a></li>
              <li><a href="index.html#dates">${T.dates}</a></li>
              <li><a href="index.html#contact">${T.contact}</a></li>
            </ul>
          </div>
        </div>
        <div class="bottom">
          <span>${T.copy}</span>
          <span>${T.final}</span>
        </div>
      </div>`;
  }

  // Scroll reveal
  const els = document.querySelectorAll('.reveal');
  if ('IntersectionObserver' in window) {
    const io = new IntersectionObserver((entries) => {
      entries.forEach((en) => { if (en.isIntersecting) { en.target.classList.add('in'); io.unobserve(en.target); } });
    }, { threshold: 0.12 });
    els.forEach((el) => io.observe(el));
  } else {
    els.forEach((el) => el.classList.add('in'));
  }
})();
