// Villa La Vanille — bandeau cookies et balise Google (Analytics + Google Ads).
// La balise n'est chargée qu'après l'accord du visiteur (exigence CNIL).
(function () {
  var ID = 'G-8RVVVXJ4HN';
  var KEY = 'vlv-cookies';
  function lire() { try { return localStorage.getItem(KEY); } catch (e) { return null; } }
  function ecrire(v) { try { localStorage.setItem(KEY, v); } catch (e) {} }
  function charger() {
    if (window.__vlvGa) return;
    window.__vlvGa = true;
    var s = document.createElement('script');
    s.async = true;
    s.src = 'https://www.googletagmanager.com/gtag/js?id=' + ID;
    document.head.appendChild(s);
    window.dataLayer = window.dataLayer || [];
    window.gtag = function () { dataLayer.push(arguments); };
    gtag('js', new Date());
    gtag('config', ID);
    var ev = document.body && document.body.getAttribute('data-event');
    if (ev) gtag('event', ev);
  }
  // Carte Google Maps du pied de page : chargée après accord ou sur clic
  function carte() {
    document.querySelectorAll('.carte-f').forEach(function (c) {
      if (c.querySelector('iframe')) return;
      var f = document.createElement('iframe');
      f.src = c.getAttribute('data-src'); f.loading = 'lazy'; f.title = 'Google Maps';
      f.referrerPolicy = 'no-referrer-when-downgrade';
      c.innerHTML = ''; c.appendChild(f);
    });
  }
  var choix = lire();
  if (choix === 'oui') { charger(); }

  function bandeau() {
    if (choix === 'oui') carte();
    document.querySelectorAll('.carte-btn').forEach(function (bt) { bt.addEventListener('click', carte); });
    var b = document.getElementById('cookies');
    if (!b) return;
    if (!choix) b.hidden = false;
    b.querySelector('.c-ok').addEventListener('click', function () { ecrire('oui'); b.hidden = true; charger(); carte(); });
    b.querySelector('.c-non').addEventListener('click', function () { ecrire('non'); b.hidden = true; });
    var g = document.getElementById('gerer-cookies');
    if (g) g.addEventListener('click', function (e) { e.preventDefault(); b.hidden = false; });
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', bandeau); else bandeau();
})();
