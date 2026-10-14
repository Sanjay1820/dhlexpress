# DHLR Express redesign

## October 2026 editorial refresh

Homepage slider follow-up: all three photos now fill the entire banner width and height, with the headings, descriptions and buttons layered over a dark gradient. Mobile uses the same image-overlay layout with its own crop and spacing. Existing autoplay and controls remain in use.

About Us follow-up: at the user's request, the complete original introduction and all 16 original topics are retained word for word, with only whitespace and visual grouping changed. This includes Our Values, Passion, Honesty, Caring, Quality, Management, Accountability & Transparency, Supply Chain Management, Assistance, Analytical Approach, Importance, Methodology, Satisfaction, Delivering, Vision and Mission. `restore_about_content.py` extracts them from `.redesign-backup/about-us.html`, verifies every full description and the introduction, and writes `templates/about-content.html`. Dedicated responsive styling lives in `css/premium.css`; `apply_premium_design.py` retains the complete content during regeneration. Browser visual verification remains unavailable.

About Us text motion: `js/about-motion.js` animates headings and paragraphs once on entering the viewport, alternating left, bottom, right and top entrances with short stagger delays. Existing generic parent reveals skip the About content to avoid doubled movement. Smaller mobile offsets, reduced-motion preferences, printing and browsers without IntersectionObserver are handled. Simulated JavaScript checks passed for directions, viewport reveal, one-time observation and reduced-motion/fallback behavior; the original introduction and all 16 topics remain unchanged.

Services follow-up: 19 service pages now use the `services-modern` reading layout with a navigation sidebar, clear headings, image spacing and complete paragraph text. The Services overview retains its six directory cards and restores all five original detailed sections from the backup (Car Transportation, Warehousing and Storage, Logistics, Supply Chain and warehousing), including the original paragraph text. `format_service_pages.py` applies the layout and is called by the regeneration hook. The shared `js/about-motion.js` now applies the same four directional text entrances to services. Reduced-motion, no-observer and print fallbacks remain supported. Original service headings and paragraphs were compared against the backup; browser visual verification remains unavailable.

Service HD imagery: `service_images.py` maps each service to its existing branded high-resolution photograph. All 18 detail pages now have a relevant large image, including new lead photographs for packing, wooden packaging and export packing. The overview's five detailed sections also use HD photographs; its existing six HD directory images remain. Original product-reference images and all text are retained. The 23 large content photos were checked against actual JPEG dimensions (at least 1600 pixels wide) and file integrity. Responsive CSS controls their crop and height; generation retains the assignments.

Contact follow-up: `templates/contact-content.html` provides distinct phone/email/website channels, an existing HD support photograph, a WhatsApp link and six office cards. All original office wording, addresses, numbers and email addresses are preserved, with separate clickable email links. `format_contact_page.py` and the premium generation hook retain this layout. The original enquiry endpoint and all six input field names remain unchanged. Four-direction text motion now includes contact content. Content preservation, HTML nesting, local assets/links/anchors, form structure and stable regeneration checks pass. PHP mail delivery and rendered browser appearance have not been verified.

Network follow-up: `format_network_page.py` presents the existing strategic-solutions text and both original helplines, an HD network photograph, six featured destination cards and a complete directory of all 70 existing city/area pages. The original enquiry form and all six field names are retained. `js/network.js` filters the directory by city/area words and provides a result count, clear button and no-results state; destinations stay visible without JavaScript. The shared four-direction text effects include the network page. Checks pass for all destination links, content/helpline retention, form structure, HTML nesting, regeneration and simulated search interactions. Browser visual verification remains unavailable.

Homepage final polish: `polish_homepage.py` adds the homepage styling scope and a services scroll link. The full-width slideshow now has numbered dot controls, a glass caption, accent typography and an overlapping trust strip. Service cards, the company image, process section and quote panel have refined image crops, spacing, surfaces and hover details. All three slides, six service cards, original content and enquiry form are retained. Markup, local assets/links/anchors, CSS block balance and regeneration checks pass. Browser visual verification remains unavailable.

Homepage roadmap: the supplied screenshot's two-column timeline is adapted to the existing moving process. A left introduction and quote CTA sit alongside four numbered circles joined by a vertical line. Every original step title and description is retained. Desktop keeps the introduction alongside the steps; mobile stacks the two columns. Existing scroll reveals include the timeline and its introduction. HTML, content retention, CTA anchors and regeneration checks pass; browser visual verification remains unavailable.

Restored homepage sections: `restore_home_sections.py` reads the original homepage backup and restores all six complete customer reviews (names, roles, associated images and full text), all 15 original client logos, and the strategic-solutions/24x7 helpline banner with both original phone numbers and representative image. Reviews and logos have responsive horizontal carousels controlled by `js/home-carousels.js`; complete content is available by scrolling without JavaScript. No review text is truncated. Both sections and the helpline precede the existing enquiry form. Original content/assets, HTML nesting, links/anchors, retained homepage sections and stable regeneration pass checks; simulated carousel tests cover next/previous, counts, disabled end controls and reduced motion. Browser visual verification remains unavailable.

Carousel autoplay follow-up: reviews advance every 3 seconds; logos every 1.8 seconds (updated to the user's faster timing preference). Both loop back to the beginning and have manual arrows plus pause/play. Hover, keyboard focus and a hidden browser tab suspend the timer; reduced-motion preferences disable autoplay by default. Simulated checks pass for timers, wraparound, manual navigation, pause/resume, hover/focus and visibility/motion changes. Complete original review and logo content is retained.

Welcome content follow-up: `restore_home_welcome.py` restores the original full Welcome introduction and Quality & Professional Services heading/description immediately after the slider's trust strip. The welcome heading sits alongside readable paragraphs; the quality text has its own contrasting panel. No original wording is shortened. The shared four-direction text effects now include these headings and paragraphs. Original-text retention, placement, HTML/links/anchors and stable regeneration checks pass; rendered browser appearance remains unverified.

Review center-focus follow-up: the reviews now use a looping coverflow presentation. The centered card remains full size with a stronger border/shadow; neighbours scale down, tilt in perspective and sit slightly lower. Runtime copies before and after the six original cards allow seamless loop normalization after scrolling stops; copies are inert and hidden from assistive technology. The original review text is untouched. Three-second autoplay, manual arrows, keyboard navigation, pause/hover/focus handling and reduced-motion support remain. Simulated checks pass for center sizing, next/previous wrap, normalization, autoplay and accessible copies; browser visual verification remains unavailable.

All 94 pages load `css/premium.css` after the existing stylesheet. The new visual system uses warm ivory, deep blue-green and the existing red brand accent, Segoe UI headings, Georgia italic highlights, rounded buttons, detailed service cards and refined inner-page banners. The homepage now has a split photographic hero, a moving services ribbon, numbered sections, a dark process section, a light enquiry panel and a large typographic footer. Existing images, navigation destinations and PHP form fields are retained.

`apply_premium_design.py` applies the composition changes to existing pages and is also called by `redesign_site.py`, so regeneration retains the new design. The reference homepage at `https://talentmanagementsystem.in/` was inspected through its HTML; its multiline headings, emphasis, numbered content and motion styling informed the adaptation. Browser access was unavailable, so rendered desktop/mobile appearance has not been visually verified. Local link, image, anchor and form-target audits passed for all 94 pages; both existing JavaScript controllers passed syntax validation. PHP mail delivery was not exercised. Changes remain local.

94 existing HTML pages now use the shared responsive red, navy and white design based on the existing DHLR Express logo. Start with `index.html`.

Features: a three-slide home banner, generated photography, alternating text entrances, image zoom, four directional card color sweeps, responsive navigation, quote forms, city links and WhatsApp contact. Slider supports dots, previous/next, pause, arrow keys and reduced-motion preferences. Existing PHP enquiry endpoint and field names are preserved.

Original HTML is preserved in `.redesign-backup/`. Shared styling is in `css/redesign.css`, interactions in `js/redesign.js`. `redesign_site.py` regenerates the HTML from the preserved originals; edit it when changing shared page markup. `redesign-report.json` lists the updated pages.

All 94 pages passed a local audit of linked files, images, fragment targets and form actions. Home, CSS, JavaScript, both generated JPEGs, contact and a service page returned HTTP 200. Browser automation was unavailable, so rendered desktop/mobile layout and interactive behavior have not been verified in a browser. PHP email delivery requires the existing PHP-enabled host and mail configuration and has not been tested here.

## AI images

Generated with the built-in imagegen tool. Original PNGs and optimized JPEGs are included under `img/redesign/`.

`img/redesign/logistics-hero.jpg` / `logistics-hero.png`

Prompt: “Use case: ads-marketing. Create a photorealistic premium wide landscape website hero photograph for an Indian packing, moving and logistics company. Modern red cargo truck parked at a clean contemporary warehouse loading bay, two Indian professional movers wearing navy uniforms carrying neatly sealed cardboard moving boxes on the right half. Authentic high-end commercial photography, golden morning sunlight, crisp realistic materials, restrained red and deep navy accents. Wide cinematic 16:9 composition, truck and workers on right, left third clean dark navy warehouse shadow for readable white HTML headline overlay. No lettering, no words, no logos, no watermarks. Save the generated image for use in current website project.”

`img/redesign/home-hero.jpg` / `home-hero.png`

Prompt: “Use case: ads-marketing. Premium photorealistic commercial photo for an Indian home relocation website hero. Two professional Indian movers in clean deep navy polo shirts carefully wrapping furniture and stacking sealed cardboard boxes in a beautiful bright modern Indian apartment. Main action on the right two-thirds, clean subdued shadowed space on left for white HTML heading. Warm natural daylight, realistic skin and furniture texture, subtle red moving equipment accents. Wide landscape 16:9, understated trustworthy premium editorial photography. No logos, no text, no watermarks.”

Changes are local to this workspace and have not been deployed.

## Topic-specific title banners

All 93 inner-page title banners now use images related to the page topic. There are 27 AI image themes: 25 newly generated images plus the two existing generated home/logistics images. Each primary service page has its own subject, including team, customer support, vehicle transport, office/corporate relocation, industrial machinery, fine art, packing, timber crates, export freight, commercial moving, containers, supply chain, oversized cargo, international relocation, domestic moving, dispatch network and completed delivery. City pages use related metropolitan, coastal, residential or Bangalore apartment moving scenes.

Banner desktop/mobile padding and headline sizing are unchanged. Each theme has its own crop position, with a navy overlay for title contrast. Assets are saved as both original PNG and optimized JPEG in `img/redesign/`. Generated images use the built-in imagegen tool. Full prompts and source provenance are recorded in `banner-generation.json`; assignments for each page are in `page-banner-map.json`.

Run `python set_page_banners.py` to reapply the banner assignments without rebuilding page content. `redesign_site.py` also preserves these topic assignments on regeneration.

## Logos on AI imagery

26 AI photos containing moving cartons, wooden crates or transport vehicles now have DHLR Express branding based on the original `img/resources/transtar logo.jpg`. The built-in imagegen edit tool applied perspective-aware packaging prints and vehicle decals. The home slider and applicable inner-page banners use these edited versions.

Edited originals and optimized JPEGs are saved as `img/redesign/<topic>-branded.png` and `img/redesign/<topic>-branded.jpg`. Earlier unbranded assets are retained. `branded-image-generation.json` records the editing prompts, logo reference, generated sources and final asset paths. The contact-support photo contains no boxes or trucks and retains its original image.

`set_page_banners.py` and `redesign_site.py` prefer branded files automatically. Image sheets `img/redesign/branded-preview-1.jpg` through `branded-preview-4.jpg` show the edited assets for review.

## Distinct home slides and autoplay

The home slider now has three different images: branded truck relocation, branded home packing, and the new business-logistics distribution-centre photo. The final new photo is saved as `img/redesign/business-logistics-hero-branded.png` and its optimized `business-logistics-hero-branded.jpg`. It was refined using the original logo reference. `business-hero-generation.json` records the built-in imagegen prompts and final paths.

The slider has one controller in `js/hero-slider.js`: a fresh five-second timer after each transition or manual navigation, looping through all three slides. Pointer hover does not stop autoplay. Pause/play, dots, previous/next, keyboard arrows, background-tab suspension and reduced-motion preferences are supported. All three photos load eagerly. The old slider controller was removed from `js/redesign.js` to avoid multiple timers.

Autoplay, wraparound, manual controls, timer reset, hover continuity, hidden-tab handling and reduced-motion behaviour passed a JavaScript runtime check with simulated DOM and timers. Live browser verification remains unavailable.
