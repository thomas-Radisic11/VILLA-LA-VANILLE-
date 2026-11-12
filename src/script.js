// Villa La Vanille — barre de navigation et galerie plein écran.
(function () {

  // Souligne la rubrique en cours dans la barre
  var links = Array.prototype.slice.call(document.querySelectorAll('.pill a'));
  function mark() {
    var y = window.scrollY + window.innerHeight * 0.35, on = null;
    links.forEach(function (a) { var s = document.querySelector(a.getAttribute('href')); if (s && s.offsetTop <= y) on = a; });
    links.forEach(function (a) { a.classList.toggle('on', a === on); });
  }
  window.addEventListener('scroll', mark, { passive: true });
  mark();

  // Galerie plein écran
  var lb = document.getElementById('lb');
  var lbImg = lb.querySelector('img');
  var count = lb.querySelector('.count');
  var items = [], cur = 0;
  function show(i) {
    cur = (i + items.length) % items.length;
    var im = items[cur].querySelector('img');
    lbImg.src = im.src; lbImg.alt = im.alt;
    count.textContent = (cur + 1) + ' / ' + items.length;
  }
  // Chaque groupe (galerie, ou photos d'une chambre) défile séparément
  document.querySelectorAll('.zoomg, .zoom').forEach(function (b) {
    b.addEventListener('click', function () {
      items = Array.prototype.slice.call(b.closest('[data-group]').querySelectorAll('.zoomg, .zoom'));
      show(items.indexOf(b));
      if (lb.showModal) lb.showModal();
    });
  });
  lb.querySelector('.prev').addEventListener('click', function () { show(cur - 1); });
  lb.querySelector('.next').addEventListener('click', function () { show(cur + 1); });
  lb.querySelector('.close').addEventListener('click', function () { lb.close(); });
  lb.addEventListener('click', function (e) { if (e.target === lb) lb.close(); });
  // Carrousels horizontaux (galerie, chambres) : flèches et compteur
  document.querySelectorAll('.carrousel').forEach(function (c) {
    var piste = c.querySelector('.piste');
    var slides = Array.prototype.slice.call(piste.querySelectorAll('.slide'));
    var compteur = c.querySelector('.compteur');
    var pad = function (n) { return (n < 10 ? '0' : '') + n; };
    var courant = function () {
      var x = piste.scrollLeft + 2, i = 0;
      slides.forEach(function (s, k) { if (s.offsetLeft - slides[0].offsetLeft <= x) i = k; });
      if (piste.scrollLeft + piste.clientWidth >= piste.scrollWidth - 4) i = slides.length - 1;
      return i;
    };
    var aller = function (i) {
      i = Math.max(0, Math.min(slides.length - 1, i));
      piste.scrollTo({ left: slides[i].offsetLeft - slides[0].offsetLeft, behavior: 'smooth' });
    };
    piste.addEventListener('scroll', function () { compteur.textContent = pad(courant() + 1) + ' / ' + pad(slides.length); }, { passive: true });
    c.querySelector('.c-prev').addEventListener('click', function () { aller(courant() - 1); });
    c.querySelector('.c-next').addEventListener('click', function () { aller(courant() + 1); });
  });

  document.addEventListener('keydown', function (e) {
    if (!lb.open) return;
    if (e.key === 'ArrowRight') show(cur + 1);
    if (e.key === 'ArrowLeft') show(cur - 1);
  });

})();
