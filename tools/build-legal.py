"""Build privacy.html and terms.html using the site header/footer from about.html.

Run after editing the text below, then run tools/add-share-tags.py:

    python tools/build-legal.py && python tools/add-share-tags.py
"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
UPDATED = "4 November 2026"
CONTACT = ('<a href="mailto:info@aepl.biz">info@aepl.biz</a> or '
           '<a href="tel:+918928227122">+91 89282 27122</a>')

PRIVACY = f"""
<p class="legal__meta">Last updated {UPDATED}</p>
<p>This policy explains what personal information NORIKO collects through noriko.in, why we collect it, and your choices. NORIKO is a brand of Ashokasha Exim Pvt. Ltd. ("we", "us"), based in Thane West 400604, Maharashtra, India.</p>

<h2>What we collect</h2>
<ul>
<li><strong>Enquiry and contact forms.</strong> Name, company or firm name, email address, phone number, the products or ranges you are interested in, and your message.</li>
<li><strong>Catalogue request.</strong> Your business email address, so we can send you the HoReCa catalogue link.</li>
<li><strong>WhatsApp.</strong> If you tap a WhatsApp button, WhatsApp opens with a message already written. We only receive what you choose to send.</li>
<li><strong>Website usage.</strong> With Google Analytics 4 we see anonymous visit data such as pages viewed, device type, approximate location and which buttons are tapped. It does not tell us who you are.</li>
</ul>

<h2>Why we use it</h2>
<ul>
<li>To reply to your enquiry, send pricing and availability, and send the catalogue you asked for.</li>
<li>To understand which pages and products are useful, and to improve the website.</li>
</ul>
<p>We do not sell your information. We do not send marketing messages unless you ask us to.</p>

<h2>Who handles it for us</h2>
<ul>
<li><strong>Formspree</strong> receives the enquiry and contact forms and passes them to us by email and WhatsApp alert.</li>
<li><strong>Resend</strong> delivers the catalogue email.</li>
<li><strong>Netlify</strong> hosts the website.</li>
<li><strong>Google</strong> provides Analytics and Search Console.</li>
<li><strong>WhatsApp (Meta)</strong> carries the messages you send us on WhatsApp.</li>
</ul>
<p>These providers may process information outside India. We only share with them what is needed to run the service.</p>

<h2>Cookies</h2>
<p>Google Analytics uses cookies or similar technologies to count visits. You can block or delete cookies in your browser settings, or install Google's opt-out add-on. The site works without them.</p>

<h2>How long we keep it</h2>
<p>We keep enquiry details for as long as needed to deal with your request and for our ordinary business records, and then delete them. Ask us if you want yours removed sooner.</p>

<h2>Your choices</h2>
<p>You can ask us to show you the personal information we hold about you, correct it, or delete it, and you can withdraw consent to us contacting you. Write to {CONTACT}. We will respond within a reasonable time.</p>

<h2>Children</h2>
<p>This website is meant for adults and for business buyers. We do not knowingly collect information from children.</p>

<h2>Changes</h2>
<p>We may update this policy. The date above shows when it last changed.</p>

<h2>Grievance officer</h2>
<p>If you have a concern about how your information is handled, write to our Grievance Officer, Ms. Asawari Gujar, Ashokasha Exim Pvt. Ltd., Thane West 400604, Maharashtra, India, at {CONTACT}. We will acknowledge your complaint and respond within a reasonable time.</p>

<h2>Contact</h2>
<p>Ashokasha Exim Pvt. Ltd., Thane West 400604, Maharashtra, India. {CONTACT}.</p>
"""

TERMS = f"""
<p class="legal__meta">Last updated {UPDATED}</p>
<p>These terms apply when you use noriko.in. NORIKO is a brand of Ashokasha Exim Pvt. Ltd. ("we", "us"). By using the website you agree to them.</p>

<h2>About the website</h2>
<p>The website shows our products, recipes and ways to contact us. It is not an online shop. You cannot buy or pay for products on it.</p>

<h2>Product information</h2>
<p>We take care that product names, pack sizes, ingredients and allergen details are accurate and match the pack. Always read the label on the product you hold, because packs and recipes can change. Photos and serving suggestions are illustrations. Recipes are suggestions, not nutritional or medical advice.</p>

<h2>Prices and availability</h2>
<p>Trade prices are not published on the website. Pricing, availability, minimum orders and delivery are confirmed by our team when you enquire, and apply only once we confirm them in writing. Retail prices (MRP) shown on some pages are indicative and may change.</p>

<h2>Enquiries</h2>
<p>Sending an enquiry, catalogue request or WhatsApp message does not create an order or a contract. A contract exists only when we accept your order in writing.</p>

<h2>Brands and imported products</h2>
<p>NORIKO, JUZO and the NORIKO logo belong to Ashokasha Exim Pvt. Ltd. Other brand names shown on the website belong to their owners. Where we show another brand's product, we are the authorised importer and distributor in India, as stated on that product page.</p>

<h2>Our content</h2>
<p>The text, photographs, illustrations and design of this website belong to us or are used with permission. You may share a page link or quote a short extract with credit to NORIKO. Please ask before you copy more or use it commercially.</p>

<h2>Using the website</h2>
<p>Please do not misuse the website, try to break or overload it, or send us false or harmful content through the forms.</p>

<h2>Links</h2>
<p>Links to other websites, such as Instagram and WhatsApp, are provided for convenience. We are not responsible for their content or practices.</p>

<h2>Liability</h2>
<p>We provide the website "as is" and try to keep it accurate and available, but we cannot promise it will always be error-free or uninterrupted. To the extent the law allows, we are not liable for loss arising from using the website. Nothing in these terms limits any right you have under law that cannot be limited.</p>

<h2>Privacy</h2>
<p>How we handle your information is explained in our <a href="privacy.html">Privacy Policy</a>.</p>

<h2>Governing law</h2>
<p>These terms are governed by the laws of India. Courts at Thane, Maharashtra, have jurisdiction over any dispute.</p>

<h2>Contact</h2>
<p>Ashokasha Exim Pvt. Ltd., Thane West 400604, Maharashtra, India. {CONTACT}. FSSAI Lic. No. 10021011000329.</p>
"""

PAGES = {
    "privacy.html": ("Privacy Policy", "How NORIKO collects, uses and protects the information you send through noriko.in.", PRIVACY),
    "terms.html": ("Terms of Use", "The terms for using the NORIKO website, noriko.in.", TERMS),
}


def main():
    about = (ROOT / "about.html").read_text(encoding="utf-8")
    head = about[: about.index("<main")]
    footer = about[about.index("</main>") + len("</main>"):]
    head = head.replace(' aria-current="page"', "")
    for name, (title, desc, body) in PAGES.items():
        h = re.sub(r"<title>.*?</title>", f"<title>{title} — NORIKO</title>", head, flags=re.S)
        h = re.sub(r'<meta name="description" content="[^"]*">', f'<meta name="description" content="{desc}">', h)
        main_html = f"""<main id="main">
  <nav class="crumbs container" aria-label="Breadcrumb">
    <ol>
      <li><a href="index.html">Home</a></li>
      <li aria-hidden="true"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"><path d="M9 6l6 6-6 6"/></svg></li>
      <li><span aria-current="page">{title}</span></li>
    </ol>
  </nav>
  <section class="section legal">
    <div class="container legal__body">
      <hr class="rule">
      <h1>{title}</h1>{body}
    </div>
  </section>
</main>"""
        (ROOT / name).write_text(h + main_html + footer, encoding="utf-8")
        print("wrote", name)


if __name__ == "__main__":
    main()
