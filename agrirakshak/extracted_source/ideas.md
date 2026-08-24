# AgriRakshak Design Direction

## Three stylistic approaches

### Theme Name: Field Notes
Very light editorial agriculture interface with paper-like warmth, ink-green typography, and annotated field-guide details. The product feels calm, practical, and made for real decisions in the field.

**Probability:** 0.03

### Theme Name: Monsoon Signal
A deep green public-service system with restrained blue weather cues, high-contrast data cards, and map-room utility. The mood is dependable, operational, and built for officers monitoring crop health across districts.

**Probability:** 0.08

### Theme Name: Harvest Ledger
A warm earth-tone interface inspired by cooperative ledgers, seed packets, and government agricultural extension posters. The mood is familiar, rooted, and highly legible for first-time digital users.

**Probability:** 0.06

## Chosen approach: Field Notes

### Design Movement
Contemporary editorial information design blended with Indian agricultural field-guide ephemera. AgriRakshak should feel like a trusted extension officer's well-organized notebook translated into a clear digital service.

### Core Principles
1. **Clarity before cleverness.** Every screen answers what happened, what it means, and what to do next.
2. **Useful warmth.** Earth neutrals, crop greens, and paper surfaces create trust without looking rustic or decorative.
3. **Progressive disclosure.** Farmers see simple actions first; technical detail is available when it helps.
4. **Evidence in context.** Images, confidence, weather signals, and escalation paths stay close to the decision they support.

### Color Philosophy
The base is a warm rice-paper white with charcoal ink for comfortable reading. Deep neem green signals trust and action; tender leaf green marks positive progress; turmeric amber draws attention to caution; monsoon blue carries weather and informational states; brick red is reserved for high-risk disease severity. The palette is intentionally matte and low-saturation so that alerts remain meaningful.

### Layout Paradigm
Use an asymmetrical editorial composition: a calm top navigation, generous left-aligned content columns, and offset evidence panels that resemble clipped field notes. Farmer views emphasize one dominant next action and a short supporting rail. Officer views use a persistent left rail with a wider data canvas. Avoid uniformly centered SaaS cards.

### Signature Elements
- A small leaf-and-sun mark used as a recognizable visual stamp in the header, favicon, and empty states.
- Thin olive rules and numbered action markers that echo annotated agronomy notes.
- Soft paper grain, subtle corner labels, and terracotta side tabs for priority states.

### Interaction Philosophy
Interactions should feel reassuring and reversible. Buttons use plain-language verbs, file upload progress explains each stage, and uncertain predictions offer a clear route to an expert rather than forcing a false answer. Hover states are quiet; focus states are prominent and accessible. Toasts explain placeholders honestly.

### Animation
Use short, physically grounded transitions under 260ms. Cards enter with a slight upward settle and opacity shift; workflow steps reveal in a 45ms stagger; upload analysis uses a gently moving scan line and status dots. Avoid decorative loops. Respect `prefers-reduced-motion` and keep keyboard-triggered navigation instant.

### Typography System
Use **Fraunces** for display headings and editorial labels, with **DM Sans** for body copy, navigation, controls, and data. Fraunces is used sparingly for warmth and distinction; DM Sans carries readability at small sizes. Headings use tight leading and sentence case. Body text stays between 15px and 18px where guidance is important.

### Brand Essence
AgriRakshak is a calm, plain-language crop health companion for Indian farmers and agricultural officers, different because it connects AI detection with understandable action and human escalation.

**Personality:** grounded, protective, practical.

### Brand Voice
Headlines are direct and encouraging, never dramatic. CTAs describe the action rather than the technology. Microcopy is short, respectful, and avoids unnecessary English jargon.

Example headline: **See the signs early. Protect the season.**

Example CTA: **Scan a crop photo**

### Wordmark & Logo
The mark is a bold, text-free sprout formed from two offset leaf shapes around a small sun notch, suggesting both protection and diagnosis. The wordmark pairs a sturdy Fraunces treatment of “Agri” with a clean DM Sans treatment of “Rakshak”; the mark remains legible on its own at small sizes.

### Signature Brand Color
**Neem Ink — #164A35.** A deep, ownable green that feels agricultural and institutional without becoming corporate or generic. It anchors navigation, primary actions, and high-confidence states.

## Style Decisions

- Use the Field Notes direction consistently across landing, farmer, and officer experiences.
- Prefer asymmetrical editorial layouts over centered dashboard templates.
- Use generated assets only for the landing hero crop visual and the brand mark; use CSS, icons, and restrained illustration for the rest.
- Keep mock data visibly structured for later API replacement and never invent pesticide doses, customer reviews, or testimonials.

### Accepted review amendments

- Utility screens carry notebook cues through field-sample strips, annotated rules, privacy notes, and evidence-adjacent guidance.
- Farmer dashboards lead with one dominant field decision, while secondary signals remain supporting notes rather than equal-weight SaaS cards.
- Brand continuity persists through the sprout/sun mark, split Agri/Rakshak wordmark, and Neem Ink primary action color across public, farmer, and officer views.
