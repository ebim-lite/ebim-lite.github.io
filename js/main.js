// Shared navbar + footer injection, mobile menu, scroll reveal.
(function () {
  const page = document.body.dataset.page || '';

  const links = [
    ['index.html', 'Home', 'home'],
    ['competition.html', 'Competition', 'competition'],
    ['resources.html', 'Learning & Compute', 'resources'],
    ['faq.html', 'FAQ', 'faq'],
  ];

  const nav = document.getElementById('site-nav');
  if (nav) {
    nav.innerHTML = `
      <div class="container">
        <a class="nav-logo" href="index.html">EBiM<span>-Lite</span> 2026</a>
        <button class="nav-toggle" aria-label="Toggle menu" aria-expanded="false">☰</button>
        <ul class="nav-links">
          ${links.map(([href, label, key]) =>
            `<li><a href="${href}"${key === page ? ' class="active"' : ''}>${label}</a></li>`).join('')}
          <li><a class="nav-cta" href="index.html#register">Register</a></li>
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
            <p style="margin-top:12px">Embodied Bimanual Manipulation Competition — Dual SO-101 adaptation.
            Simulation → Cross-Site Validation → Real-World Evaluation.</p>
          </div>
          <div>
            <h4>Pages</h4>
            <ul>
              <li><a href="index.html">Home</a></li>
              <li><a href="competition.html">Competition</a></li>
              <li><a href="resources.html">Learning &amp; Compute</a></li>
              <li><a href="faq.html">FAQ</a></li>
            </ul>
          </div>
          <div>
            <h4>Tracks</h4>
            <ul>
              <li><a href="competition.html#track1">Cable Routing</a></li>
              <li><a href="competition.html#track2">Thermal Pad Pick-and-Place</a></li>
              <li><a href="competition.html#track3">Service Robot Challenge</a></li>
            </ul>
          </div>
          <div>
            <h4>Participate</h4>
            <ul>
              <li><a href="index.html#register">Register</a></li>
              <li><a href="index.html#dates">Important Dates</a></li>
              <li><a href="index.html#contact">Contact</a></li>
            </ul>
          </div>
        </div>
        <div class="bottom">
          <span>© 2026 EBiM-Lite Organizing Committee</span>
          <span>Final at GTC Taipei · May 2027</span>
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
