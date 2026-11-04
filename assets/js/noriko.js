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
    function closeNav(returnFocus) {
      if (!nav.classList.contains('is-open')) return;
      nav.classList.remove('is-open');
      toggle.setAttribute('aria-expanded', 'false');
      document.body.classList.remove('nav-open');
      if (returnFocus) toggle.focus();
    }

    toggle.addEventListener('click', function () {
      var open = nav.classList.toggle('is-open');
      toggle.setAttribute('aria-expanded', String(open));
      document.body.classList.toggle('nav-open', open);
    });

    nav.addEventListener('click', function (event) {
      if (event.target.closest('a')) closeNav(false);
    });

    document.addEventListener('click', function (event) {
      if (nav.classList.contains('is-open') && !nav.contains(event.target) && !toggle.contains(event.target)) {
        closeNav(false);
      }
    });

    document.addEventListener('keydown', function (event) {
      if (event.key === 'Escape') closeNav(true);
    });

    window.addEventListener('resize', function () {
      if (window.innerWidth > 900) closeNav(false);
    });
  }

  /* Entrance reveal — once, and skipped entirely under reduced motion.
     The hidden start state is opt-in via .js-reveal so that no-JS, an older
     browser, or an observer that never fires still shows all content. */
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* Use real plated-food photography where supplied. Remaining snacks fall
     back to a crop of the food illustration printed on their own pack. */
  var snackDishImages = {
    'big-latiao.webp': 'assets/img/snack-dishes/latiao.webp',
    'mini-latiao.webp': 'assets/img/snack-dishes/latiao.webp',
    'kiss-burn.webp': 'assets/img/snack-dishes/kiss-burn.webp',
    'konjac-hot.webp': 'assets/img/snack-dishes/konjac.webp',
    'konjac-sour.webp': 'assets/img/snack-dishes/konjac.webp'
  };
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
    if (!snackFoodFocus[file] && !snackDishImages[file]) return;
    var food = snackDishImages[file] ? document.createElement('img') : pack.cloneNode(false);
    if (snackDishImages[file]) food.src = snackDishImages[file];
    food.className = 'snack-card__food';
    food.alt = '';
    food.setAttribute('aria-hidden', 'true');
    if (snackFoodFocus[file]) food.style.setProperty('--food-focus', snackFoodFocus[file]);
    food.loading = 'lazy';
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

  /* ---- Featured Cook pack: tap to swap pack and dish (touch has no hover) ---- */
  document.querySelectorAll('.cook-feature__media').forEach(function (media) {
    media.addEventListener('click', function () {
      media.closest('.cook-feature').classList.toggle('is-dish');
    });
  });

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
    var contactParams = new URLSearchParams(window.location.search);
    var requestedInterest = contactParams.get('interest');
    var requestedProduct = contactParams.get('product');
    if (requestedInterest) {
      Array.prototype.forEach.call(contactForm.querySelectorAll('[name="interest"] option'), function (option) {
        option.selected = option.value.toLowerCase() === requestedInterest.toLowerCase();
      });
    }
    if (requestedProduct) {
      var messageField = contactForm.querySelector('[name="message"]');
      if (messageField && !messageField.value) {
        messageField.value = 'I am interested in ' + requestedProduct + '. Please share availability, suitable pack formats and pricing.';
      }
    }
    contactForm.addEventListener('change', function (e) {
      var help = document.getElementById('interest-help');
      if (help && e.target.name === 'interest' && contactForm.querySelector('input[name="interest"]:checked')) help.hidden = true;
    });
    contactForm.addEventListener('submit', function (e) {
      e.preventDefault();
      if (!contactForm.checkValidity()) {
        contactForm.reportValidity();
        return;
      }
      /* "Interested in" is a set of checkboxes; at least one is required,
         and the choices are sent to Formspree as one readable line. */
      var interests = Array.prototype.map.call(
        contactForm.querySelectorAll('input[name="interest"]:checked'),
        function (box) { return box.value; }
      );
      var interestHelp = document.getElementById('interest-help');
      if (interestHelp) interestHelp.hidden = interests.length > 0;
      if (interests.length === 0) {
        var firstBox = contactForm.querySelector('input[name="interest"]');
        if (firstBox) firstBox.focus();
        return;
      }
      var data = new FormData(contactForm);
      data.delete('interest');
      data.append('interest', interests.join(', '));
      submitToFormspree(contactForm, data, contactStatus, 'Thank you. Your enquiry has been sent to the NORIKO India team.').then(function (sent) {
        if (sent) contactForm.reset();
      });
    });
  }

  /* ---- Visitor recipe suggestions ---- */
  var recipeSuggestionForm = document.getElementById('recipe-suggestion-form');
  var recipeSuggestionStatus = document.getElementById('recipe-suggestion-status');
  if (recipeSuggestionForm) {
    recipeSuggestionForm.addEventListener('submit', function (e) {
      e.preventDefault();
      if (!recipeSuggestionForm.checkValidity()) {
        recipeSuggestionForm.reportValidity();
        return;
      }
      var data = new FormData(recipeSuggestionForm);
      submitToFormspree(recipeSuggestionForm, data, recipeSuggestionStatus, 'Thank you. Your recipe suggestion has been sent to the NORIKO team.').then(function (sent) {
        if (sent) recipeSuggestionForm.reset();
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

  /* ---- Connect product detail pages to recipes that use them ---- */
  var recipeLibrary = {
    bamboo: ['bamboo-water-chestnut-stir-fry.html', 'Bamboo & Water Chestnut Stir-Fry', 'bamboo-shoot-stir-fry-final.webp'],
    blackFungus: ['black-fungus-cucumber-salad.html', 'Black Fungus Cucumber Salad', 'black-fungus-salad-final.webp'],
    crispyRice: ['crispy-sushi-rice-bites.html', 'Crispy Sushi Rice Bites', 'crispy-sushi-rice-bites-final.webp'],
    paneer: ['gochujang-honey-paneer.html', 'Gochujang Honey Paneer', 'gochujang-honey-paneer-final.webp'],
    ramen: ['gochujang-ramen.html', 'Gochujang Ramen', 'spicy-ramen-eggs-final.webp'],
    kimchiRice: ['kimchi-fried-rice.html', 'Kimchi Fried Rice', 'kimchi-fried-rice-final.webp'],
    mangoRice: ['mango-sticky-rice.html', 'Mango Sticky Rice', 'mango-sticky-rice-final.webp'],
    udon: ['sesame-shiitake-udon.html', 'Sesame Shiitake Udon', 'miso-butter-udon-final.webp'],
    soba: ['sesame-soba-salad.html', 'Sesame Soba Salad', 'sesame-soba-salad-final.webp'],
    shiitakeNoodles: ['shiitake-chilli-garlic-noodles.html', 'Shiitake Chilli Garlic Noodles', 'shiitake-chilli-garlic-noodles-final.webp']
  };
  var productRecipeMap = {
    'canned-bamboo-shoots.html': ['bamboo'],
    'canned-water-chestnuts.html': ['bamboo'],
    'dried-black-fungus.html': ['blackFungus'],
    'sushi-rice.html': ['crispyRice'],
    'sushi-vinegar.html': ['crispyRice'],
    'noriko-sushi-vinegar-500ml.html': ['crispyRice'],
    'mayonnaise.html': ['crispyRice'],
    'gochujang.html': ['crispyRice', 'paneer', 'ramen'],
    'nori-sheet-10.html': ['crispyRice', 'ramen', 'kimchiRice'],
    'nori-sheet-50.html': ['crispyRice', 'ramen', 'kimchiRice'],
    'rice-vinegar.html': ['bamboo', 'blackFungus', 'crispyRice', 'paneer', 'udon', 'soba', 'shiitakeNoodles'],
    'rice-vinegar-1-8l.html': ['bamboo', 'blackFungus', 'crispyRice', 'paneer', 'udon', 'soba', 'shiitakeNoodles'],
    'sesame-oil.html': ['bamboo', 'blackFungus', 'paneer', 'ramen', 'kimchiRice', 'udon', 'soba', 'shiitakeNoodles'],
    'ramen-noodles.html': ['ramen'],
    'kimchi-sauce.html': ['kimchiRice'],
    'glutinous-rice.html': ['mangoRice'],
    'udon-noodles.html': ['udon'],
    'soba-noodles.html': ['soba'],
    'dried-shiitake-mushroom.html': ['udon', 'shiitakeNoodles']
  };
  var productPageName = window.location.pathname.split('/').pop();
  var linkedRecipeKeys = productRecipeMap[productPageName];
  var productInfo = document.querySelector('.pdp__info');
  if (linkedRecipeKeys && productInfo && !productInfo.querySelector('.pdp-recipes')) {
    var recipeBlock = document.createElement('aside');
    recipeBlock.className = 'pdp-recipes';
    recipeBlock.setAttribute('aria-label', 'Recipes using this product');
    recipeBlock.innerHTML = '<p class="eyebrow">Cook with this product</p><div class="pdp-recipes__list">' + linkedRecipeKeys.map(function (key) {
      var recipe = recipeLibrary[key];
      return '<a class="pdp-recipe-link" href="../recipes/' + recipe[0] + '"><img src="../assets/img/recipes/' + recipe[2] + '" alt="" width="160" height="100" loading="lazy"><span><strong>' + recipe[1] + '</strong><small>View recipe <b aria-hidden="true">→</b></small></span></a>';
    }).join('') + '</div>';
    var enquiryActions = productInfo.querySelector('.pdp__actions');
    if (enquiryActions) enquiryActions.insertAdjacentElement('afterend', recipeBlock);
    else productInfo.appendChild(recipeBlock);
  }

  /* ---- Floating "Chat on WhatsApp" button, on every page ----
     Opens the helpline on WhatsApp with a message that names the page,
     so a product page arrives as "I'm interested in Gochujang". */
  var WHATSAPP_NUMBER = '918928227122';
  function whatsappLink(message) {
    return 'https://wa.me/' + WHATSAPP_NUMBER + '?text=' + encodeURIComponent(message);
  }
  var pageName = document.title.split(' — ')[0].replace(/ Recipe$/, '');
  var waMessage = 'Hi NORIKO, ';
  if (/\/products\//.test(location.pathname)) waMessage += "I'm interested in " + pageName + '.';
  else if (/\/recipes\//.test(location.pathname)) waMessage += 'I saw the ' + pageName + ' recipe and have a question.';
  else waMessage += 'I have an enquiry.';

  var waButton = document.createElement('a');
  waButton.className = 'wa-float';
  waButton.href = whatsappLink(waMessage);
  waButton.target = '_blank';
  waButton.rel = 'noopener';
  waButton.setAttribute('aria-label', 'Chat with NORIKO on WhatsApp');
  waButton.innerHTML = '<svg viewBox="0 0 32 32" width="26" height="26" aria-hidden="true"><path fill="currentColor" d="M16.02 3C8.84 3 3 8.82 3 15.98c0 2.3.6 4.53 1.75 6.5L3 29l6.7-1.74a13 13 0 0 0 6.32 1.62h.01C23.2 28.88 29 23.06 29 15.9 29 8.75 23.19 3 16.02 3zm0 23.7h-.01a10.8 10.8 0 0 1-5.5-1.5l-.4-.24-3.97 1.03 1.06-3.86-.26-.4a10.7 10.7 0 0 1-1.65-5.75c0-5.95 4.85-10.8 10.83-10.8a10.8 10.8 0 0 1 10.8 10.82c0 5.95-4.86 10.7-10.9 10.7zm5.93-8.03c-.33-.16-1.93-.95-2.23-1.06-.3-.11-.52-.16-.73.16-.22.33-.84 1.06-1.03 1.27-.19.22-.38.24-.71.08-.33-.16-1.38-.51-2.62-1.62-.97-.86-1.62-1.93-1.81-2.25-.19-.33-.02-.5.14-.67.15-.14.33-.38.49-.57.16-.19.22-.33.33-.54.11-.22.05-.41-.03-.57-.08-.16-.73-1.76-1-2.41-.27-.63-.53-.55-.73-.56h-.62c-.22 0-.57.08-.87.41-.3.33-1.14 1.11-1.14 2.71s1.17 3.15 1.33 3.36c.16.22 2.3 3.5 5.56 4.9.78.34 1.39.54 1.86.69.78.25 1.49.21 2.05.13.63-.09 1.93-.79 2.2-1.55.27-.76.27-1.41.19-1.55-.08-.14-.3-.22-.62-.38z"/></svg><span>Chat on WhatsApp</span>';
  document.body.appendChild(waButton);

  /* Retail "Where to buy": ask on WhatsApp with the question pre-written */
  var whereWa = document.getElementById('where-whatsapp');
  if (whereWa) whereWa.href = whatsappLink('Hi NORIKO, where can I buy your products near me? My city is: ');

  render();
})();
