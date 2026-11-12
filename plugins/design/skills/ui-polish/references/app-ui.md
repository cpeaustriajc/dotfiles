# App UI rules

For dashboards, admin, settings and other dense screens. A row names the rule it breaks.

Sources for type, number, radius, shadow and image details: Vercel's Web Interface Guidelines
(https://vercel.com/design/guidelines); Jakub Krehel, "Details that make interfaces feel better"
(https://jakub.kr/writing/details-that-make-interfaces-feel-better); Josh Comeau, "Designing
Beautiful Shadows in CSS" (https://www.joshwcomeau.com/css/designing-shadows/);
`Dammyjay93/interface-design` (https://github.com/Dammyjay93/interface-design).

Our choices:
- One 4- or 8-point grid; flag off-grid values such as 14px (grep the CSS for them).
- One depth strategy per product, borders or shadows, not both on one surface.
- Density decided up front as a named control height (32px dense, 40px roomy), applied everywhere.
- Colour signals state; grey carries structure.
