/* NORIKO — shared page behaviour.
   Every block guards for absent elements, so the same file serves the
   homepage (nav, reveal, JUZO, HoReCa filter, enquiry basket) and the
   Retail hub (nav, reveal, JUZO only). */
(function () {
  'use strict';

  /* Mobile nav */
  var toggle = document.querySelector('.nav-toggle');
  var nav = document.getElementById('primary-nav');
  if (toggle && nav) {
    toggle.addEventListener('click', function () {
      var open = nav.classList.toggle('is-open');
      toggle.setAttribute('aria-expanded', String(open));
    });
  }

  /* Entrance reveal — once, and skipped entirely under reduced motion.
     The hidden start state is opt-in via .js-reveal so that no-JS, an older
     browser, or an observer that never fires still shows all content. */
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var items = document.querySelectorAll('.reveal');
  if (!reduce && 'IntersectionObserver' in window && items.length) {
    document.documentElement.classList.add('js-reveal');
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry, i) {
        if (!entry.isIntersecting) return;
        var el = entry.target;
        setTimeout(function () { el.classList.add('is-in'); }, (i % 4) * 60);
        io.unobserve(el);
      });
    }, { rootMargin: '0px 0px -8% 0px', threshold: 0.08 });
    items.forEach(function (el) { io.observe(el); });

    /* Safety net: if anything is still hidden after 2s, reveal it. */
    setTimeout(function () {
      items.forEach(function (el) { el.classList.add('is-in'); });
    }, 2000);
  }

  /* JUZO flavour switcher — repaints the section and swaps the cup.
     Selection is exposed via aria-pressed and a checkmark, not colour alone. */
  /* Key off the class, not an id: the section is #juzo on the homepage
     and #drink on the Retail hub, where the nav needs that anchor. */
  var juzo = document.querySelector('.juzo');
  var flavourBtns = document.querySelectorAll('.flavours button');
  if (juzo && flavourBtns.length) {
    var paint = function (f) {
      juzo.style.setProperty('--juzo-active', 'var(--juzo-' + f + ')');
      juzo.style.setProperty('--juzo-active-ink', 'var(--juzo-' + f + '-ink)');
    };
    flavourBtns.forEach(function (btn) {
      btn.addEventListener('click', function () {
        var f = btn.getAttribute('data-flavour');
        flavourBtns.forEach(function (b) { b.setAttribute('aria-pressed', String(b === btn)); });
        paint(f);
        juzo.querySelectorAll('.juzo__cup').forEach(function (cup) {
          cup.classList.toggle('is-active', cup.getAttribute('data-cup') === f);
        });
      });
    });
    var initial = document.querySelector('.flavours button[aria-pressed="true"]');
    if (initial) paint(initial.getAttribute('data-flavour'));
  }

  /* ---- HoReCa category filter ----
     Sized for the full catalogue; the visible rows are a sample, so most
     categories are legitimately empty for now. */
  var filterBtns = document.querySelectorAll('.filters button');
  var specRows = document.querySelectorAll('.spec-row');
  var noneEl = document.getElementById('spec-none');
  var moreBtn = document.getElementById('spec-more');
  var PREVIEW = 10;          /* the homepage previews; the full catalogue is long */
  var expanded = false;
  var activeCat = 'all';

  function applyRows() {
    var matching = [], shown = 0;
    specRows.forEach(function (row) {
      var match = activeCat === 'all' || row.getAttribute('data-cat') === activeCat;
      if (match) matching.push(row);
      row.hidden = true;
    });
    matching.forEach(function (row, i) {
      var visible = expanded || i < PREVIEW;
      row.hidden = !visible;
      if (visible) shown++;
    });
    if (noneEl) noneEl.hidden = matching.length !== 0;
    if (moreBtn) {
      var hiddenCount = matching.length - shown;
      if (matching.length <= PREVIEW) {
        moreBtn.hidden = true;
      } else {
        moreBtn.hidden = false;
        moreBtn.setAttribute('aria-expanded', String(expanded));
        moreBtn.textContent = expanded
          ? 'Show fewer products'
          : 'Show all ' + matching.length + ' products';
      }
    }
  }

  filterBtns.forEach(function (btn) {
    btn.addEventListener('click', function () {
      activeCat = btn.getAttribute('data-cat');
      expanded = false;
      filterBtns.forEach(function (b) { b.setAttribute('aria-pressed', String(b === btn)); });
      applyRows();
    });
  });
  if (moreBtn) {
    moreBtn.addEventListener('click', function () { expanded = !expanded; applyRows(); });
  }
  if (specRows.length) applyRows();

  /* ---- HoReCa enquiry basket ----
     Browse → add → review → details → submit. Never displays a price. */
  var basket = [];
  var listEl = document.getElementById('enquiry-list');
  var emptyEl = document.getElementById('enquiry-empty');
  var countEl = document.getElementById('enquiry-count');
  var formEl = document.getElementById('enquiry-form');
  var addBtns = document.querySelectorAll('.spec-row__cta');

  function syncButtons() {
    addBtns.forEach(function (b) {
      var inBasket = basket.some(function (i) { return i.name === b.getAttribute('data-name'); });
      b.setAttribute('aria-pressed', String(inBasket));
      b.textContent = inBasket ? 'Added ✓' : 'Add to enquiry';
    });
  }

  function render() {
    if (!listEl) return;
    listEl.innerHTML = '';
    basket.forEach(function (item, idx) {
      var li = document.createElement('li');
      var label = document.createElement('span');
      label.innerHTML = '<strong>' + item.name + '</strong> <span class="num">· ' + item.size + '</span>';
      var rm = document.createElement('button');
      rm.type = 'button';
      rm.className = 'enquiry__remove';
      rm.textContent = 'Remove';
      rm.setAttribute('aria-label', 'Remove ' + item.name + ' from enquiry');
      rm.addEventListener('click', function () {
        basket.splice(idx, 1);
        render();
        syncButtons();
      });
      li.appendChild(label);
      li.appendChild(rm);
      listEl.appendChild(li);
    });
    var n = basket.length;
    listEl.hidden = n === 0;
    if (emptyEl) emptyEl.hidden = n !== 0;
    if (countEl) countEl.textContent = n === 0 ? 'No items yet' : n + (n === 1 ? ' item' : ' items');
  }

  addBtns.forEach(function (btn) {
    btn.addEventListener('click', function () {
      var name = btn.getAttribute('data-name');
      var i = basket.findIndex(function (it) { return it.name === name; });
      if (i > -1) basket.splice(i, 1);
      else basket.push({ name: name, size: btn.getAttribute('data-size') });
      render();
      syncButtons();
    });
  });

  if (formEl) {
    formEl.addEventListener('submit', function (e) {
      e.preventDefault();
      if (basket.length === 0) {
        if (countEl) countEl.textContent = 'Add at least one product first';
        return;
      }
      /* Prototype only — no backend is wired up yet. */
      if (countEl) countEl.textContent = 'Prototype: submission not yet connected';
    });
  }

  render();
})();
