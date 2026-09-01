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

  /* Crop the food illustration from each snack's own front packshot. */
  var snackFoodFocus = {
    'fish-spicy.webp': '50% 68%',
    'fish-mala.webp': '50% 68%',
    'fish-pepper.webp': '50% 68%',
    'fish-sweet-sour.webp': '50% 68%',
    'squid-spicy.webp': '50% 68%',
    'fermented-tofu.webp': '50% 68%',
    'lotus-root.webp': '50% 67%',
    'tofu-block-spicy.webp': '50% 66%',
    'tofu-curd-skewer-spicy.webp': '50% 61%',
    'braised-tofu-stick-spicy.webp': '50% 60%',
    'big-latiao.webp': '50% 70%',
    'mini-latiao.webp': '50% 62%',
    'kiss-burn.webp': '50% 67%',
    'konjac-hot.webp': '50% 69%',
    'konjac-sour.webp': '50% 69%'
  };
  document.querySelectorAll('.snack-card__media > img').forEach(function (pack) {
    var cleanSrc = pack.getAttribute('src').split('?')[0];
    var file = cleanSrc.substring(cleanSrc.lastIndexOf('/') + 1);
    if (!snackFoodFocus[file]) return;
    var food = pack.cloneNode(false);
    food.className = 'snack-card__food';
    food.alt = '';
    food.setAttribute('aria-hidden', 'true');
    food.style.setProperty('--food-focus', snackFoodFocus[file]);
    pack.parentNode.appendChild(food);
  });

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
  var enquiryStatus = document.getElementById('enquiry-form-status');
  var addBtns = document.querySelectorAll('.spec-row__cta');

  function submitToFormspree(form, data, statusEl, successMessage) {
    var submitButton = form.querySelector('[type="submit"]');
    var originalLabel = submitButton ? submitButton.textContent : '';
    if (submitButton) {
      submitButton.disabled = true;
      submitButton.textContent = 'Sending…';
    }
    if (statusEl) statusEl.textContent = 'Sending your enquiry…';

    return fetch(form.action, {
      method: 'POST',
      body: data,
      headers: { Accept: 'application/json' }
    }).then(function (response) {
      if (!response.ok) throw new Error('Form submission failed');
      if (statusEl) statusEl.textContent = successMessage;
      return true;
    }).catch(function () {
      if (statusEl) statusEl.textContent = 'We could not send your enquiry. Please try again or email info@aepl.biz.';
      return false;
    }).finally(function () {
      if (submitButton) {
        submitButton.disabled = false;
        submitButton.textContent = originalLabel;
      }
    });
  }

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
      if (!formEl.checkValidity()) {
        formEl.reportValidity();
        return;
      }
      if (basket.length === 0) {
        if (countEl) countEl.textContent = 'Add at least one product first';
        return;
      }
      var data = new FormData(formEl);
      data.append('products', basket.map(function (item) {
        return item.name + ' · ' + item.size;
      }).join('\n'));
      submitToFormspree(formEl, data, enquiryStatus, 'Thank you. Your product enquiry has been sent.').then(function (sent) {
        if (!sent) return;
        formEl.reset();
        basket = [];
        render();
        syncButtons();
      });
    });
  }

  /* ---- General contact form ---- */
  var contactForm = document.getElementById('contact-form');
  var contactStatus = document.getElementById('contact-form-status');
  if (contactForm) {
    contactForm.addEventListener('submit', function (e) {
      e.preventDefault();
      if (!contactForm.checkValidity()) {
        contactForm.reportValidity();
        return;
      }
      var data = new FormData(contactForm);
      submitToFormspree(contactForm, data, contactStatus, 'Thank you. Your enquiry has been sent to the NORIKO India team.').then(function (sent) {
        if (sent) contactForm.reset();
      });
    });
  }

  var catalogueForm = document.getElementById('catalogue-request-form');
  var catalogueStatus = document.getElementById('catalogue-request-status');
  if (catalogueForm) {
    catalogueForm.addEventListener('submit', function (e) {
      e.preventDefault();
      if (!catalogueForm.checkValidity()) {
        catalogueForm.reportValidity();
        return;
      }
      var submitButton = catalogueForm.querySelector('[type="submit"]');
      var originalLabel = submitButton.textContent;
      submitButton.disabled = true;
      submitButton.textContent = 'Sending…';
      if (catalogueStatus) catalogueStatus.textContent = 'Preparing your catalogue email…';

      var formData = new FormData(catalogueForm);
      fetch(catalogueForm.action, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', Accept: 'application/json' },
        body: JSON.stringify({ email: formData.get('email'), website: formData.get('website') })
      }).then(function (response) {
        return response.json().catch(function () { return {}; }).then(function (body) {
          if (!response.ok) throw new Error(body.error || 'Delivery failed');
          return body;
        });
      }).then(function () {
        catalogueForm.reset();
        if (catalogueStatus) catalogueStatus.textContent = 'Sent. Please check your inbox for the catalogue attachment.';
      }).catch(function (error) {
        if (catalogueStatus) catalogueStatus.textContent = error.message || 'We could not send the catalogue. Please try again.';
      }).finally(function () {
        submitButton.disabled = false;
        submitButton.textContent = originalLabel;
      });
    });
  }

  render();
})();
