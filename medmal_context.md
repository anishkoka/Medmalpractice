# Project Context: PA Medical Malpractice Analysis & National Climate Map

## What this project is

A body of work on the medical malpractice liability environment, anchored by:
1. A panel briefing and addendum prepared for a CME panel on PA medical malpractice and tort reform (April 2026)
2. A Substack post on PA medmal tort reform building on the panel themes
3. A national medical malpractice climate map and recurring-update dashboard, scoring all 51 jurisdictions on a 0–75 composite using NAIC primary-source insurer financials

The author is **Anish Koka, MD** — cardiologist in Philadelphia, writes at AnishKokaMD.Substack.com, X @anish_koka, co-hosts The Doctor's Lounge podcast. Analytical style: rigorous, skeptical, scrutinizes COI and weak evidence. Pushes back on overconfident claims and partisan framing.

## Knowledge files in this project

- `medmal_panel_briefing.md` — main moderator's briefing (panelist bios, opening remarks, question roadmap by agenda block, key facts to surface)
- `medmal_panel_addendum.md` — four deep-dive sections: Hagans v. HUP analysis, "shock the conscience" doctrine, problems with damage caps in PA, Certificate of Merit reform options
- `substack_post.md` — Substack draft on PA medmal climate (Hagans hook → tort reform history → 2023 venue change → reserves & nuclear verdicts → defense costs → emotional toll → state comparisons → reform options framing)
- `map_data.json` — dashboard-ready scoring data, 51 states × 15-year history (2010–2024)
- `naic_medmal_data.json` — raw NAIC parse, 765 state-year records
- `parse_naic.py` — annual update script (parses NAIC PDF → produces both JSONs)
- `malpractice_climate_map.html` and `dashboard.html` — rendered outputs

---

## Methodology — the climate map scoring

Every state scored 0–75 on three primary-source components:

| Component | Range | Source |
|---|---|---|
| Cap structure | 0–35 | State statutes and state supreme court rulings, verified Apr 2026 (see `medmal_cap_citations.md` for full per-state citations) |
| NAIC premium burden per physician | 0–25 | NAIC Countrywide Summary of Medical Professional Liability Insurance ÷ AAMC State Physician Workforce |
| ATRA litigation environment | 0–15 | ATRA Judicial Hellholes 2025–26 + Watch List |

**Cap-score buckets (per state):**
- 0 = Strong cap (≤$500K noneconomic) OR PCF state limiting physician personal exposure
- 10 = Moderate cap ($500K–$1M noneconomic)
- 20 = Weak/partial cap (>$1M total cap, OR cap only on subset of noneconomic)
- 30 = No cap (struck unconstitutional or never enacted)
- 35 = Constitutional bar to enacting caps (legislature cannot restore without amendment)

**NAIC premium-burden buckets (per active physician, direct premium written):**
- < $5,500 = 0 pts
- < $7,500 = 5 pts
- < $10,000 = 10 pts
- < $13,000 = 15 pts
- < $16,000 = 20 pts
- ≥ $16,000 = 25 pts

**Rating buckets:**
- 0–25 = green (favorable)
- 26–45 = yellow (mixed)
- 46+ = red (hostile)

**Why this methodology over alternatives:** Earlier iterations relied on AMA-published OB/GYN manual premiums (only 8 jurisdictions had primary-source data; 42 states had inferred values). The NAIC integration replaced inferred values with measured values for all 51 jurisdictions. NAIC publishes annually as the Countrywide Summary of Medical Professional Liability Insurance.

## Data vintages

- **NAIC**: through calendar year 2024, published 2025 (current as of project creation)
- **AAMC physician counts**: 2023 State Physician Workforce Data Report
- **ATRA Judicial Hellholes**: 2025–2026 Report
- **NCSL cap registry**: ongoing, manually verified

The dashboard's vintage labels are dynamic — they read off the data, so the next NAIC vintage just slots in via `parse_naic.py` without code changes.

## Annual update workflow

1. NAIC publishes the new Countrywide Summary PDF (typically ~18 months after year-end)
2. Download from the NAIC Soutron library (record 25359). Note: Soutron blocks bots, so this is a manual download.
3. `pip install pdfplumber && python3 parse_naic.py path/to/NEW_VINTAGE.pdf`
4. Regenerated `map_data.json` is automatically picked up by `dashboard.html`. The static map is regenerated from the same data.
5. Update `PHYSICIAN_COUNTS` constant in `parse_naic.py` annually from the latest AAMC report.
6. Update `STATE_INPUTS` in `parse_naic.py` annually if any state's cap structure or ATRA designation changes.

## Top-line findings (2024 vintage, April 2026 cap refresh)

- PA: $21,684/MD, 97.5% loss ratio, score 70/75 (red) — constitutional bar to caps
- NY: $23,628/MD, 77.0% loss ratio, score 70/75 (red) — no cap statute
- IL: $16,642/MD, 65.2% loss ratio, score 65/75 (red) — cap struck (LeBron, 2010)
- WY, KY: 60/75 (red) — both have constitutional bars
- CT: $19,723/MD, **132.4% loss ratio** (insurers paying $1.32 per $1 collected), score 55/75 (red)
- TX: $8,504/MD, 44.2% loss ratio, score 15/75 (green) — Prop 12 reform validated
- CA: $9,397/MD, 62.9% loss ratio, score 25/75 (green) — MICRA/AB 35
- WI: $6,871/MD, 58.3% loss ratio, score 5/75 (green) — strong cap + IPFCF backstop

Distribution: 21 green / 12 yellow / 18 red. The April 2026 cap-data refresh moved Kansas from green to red (cap was wrongly classified as "restored" — actually struck in *Hilburn v. Enerpipe*, 2019), and corrected several other state classifications. The PA story is unchanged.

## Key cap-data corrections (April 2026 rebuild)

The cap structure data was rebuilt against authoritative sources in April 2026. Most significant:
- **Kansas**: was green, now red (cap was wrongly described as "restored"; *Hilburn v. Enerpipe* struck it in 2019, has not been restored)
- **Hawaii**: was yellow, now green (HRS § 663-8.7 imposes $375K p&s cap; previously listed as "no cap")
- **Wyoming**: was yellow, now red (constitutional bar under WY Const Art 10 § 4)
- **Tennessee**: aggregator-published $1.5M was wrong; actual cap is $750K/$1M catastrophic per Tenn Code § 29-39-102
- **Utah**: $450K (was $524K)
- **Florida, Illinois, New Hampshire, Washington**: caps struck (not constitutional bars; reclassified 35→30)
- **Arkansas, Kentucky**: constitutional bars (reclassified 30→35)

Full per-state citations in `medmal_cap_citations.md`.

---

## Key legal/historical facts (PA-specific)

- **MCARE Act 2002**: PA's tort reform package, established Certificate of Merit and (via PA Sup Ct rule) venue restriction to county where care was rendered
- **Pa.R.C.P. 1006(a.1) repeal**: PA Supreme Court Order August 25, 2022, effective January 1, 2023. Now any county where any defendant "regularly conducts business" is proper venue. Philadelphia filings 275 (2022) → 544 (2023). 41% of 2023 PA filings arose from care delivered outside Philadelphia.
- **Hagans v. HUP**: $182.7M jury verdict April 2023 → $207.6M with Rule 238 delay damages → Superior Court affirmed July 10, 2025 → reargument denied September 15, 2025. **Largest med-mal verdict in PA history.** Now on allocatur to PA Supreme Court. Six-issue Superior Court opinion authored by Judge Maria McLaughlin.
- **Jefferson Einstein verdict**: $108.6M Philadelphia jury, March 19–20, 2026, birth injury case (forceps, 2018), 68-year life expectancy projection
- **North-Central PA Trial Lawyers v. Weaver (2003)**: Venue is procedural, reserved to PA Supreme Court — blocks legislative venue restoration
- **PA Constitution Article III §18**: Permits damage caps only for workplace injuries. Blocks legislative caps on med-mal noneconomic damages without constitutional amendment.
- **AMA April 2026 report**: 7th consecutive year of premium increases. PA flagged with 53% of premiums rising 10%+ in 2025. Five states (PA, KY, FL, IL, NY) had 10%+ increases in both 2024 and 2025.

## Editorial guardrails (for Substack work)

These were deliberately decided through iteration. A fresh chat should respect these unless Anish revisits explicitly:

- **No firm names** — earlier drafts named Kline & Specter and Saltz Mongeluzzi; both were removed. Don't reintroduce.
- **No judicial-election or merit-selection framing** — was tried, removed after pushback. Anish was wary of partisan framing and the empirical claim that bench composition drives outcomes wasn't well supported. Replaced with "What Physicians Can Actually Do" — engagement with PAMED/PASHRM/PCCJR and public voice.
- **No MCARE Section 515 reform subsection** — removed.
- **No claim about elevated risk for women physicians** — removed.
- **System-level framing preferred over partisan/protective** — Anish wants tractable reform discussion, not "doctors vs. trial lawyers."
- **ARR over NNT, scrutinize COI, push back on weak evidence** — Anish's analytical brand. Don't paper over methodology limits.
- **Crisis resources without specific methods**: Physician Support Line 1-888-409-0141 referenced in the post. No method-specific content.

## Panelists referenced in the briefing

- **Lisa Ramthun, MSN, RN, CPHRM, DFASHRM, CPHQ** — Enterprise VP Risk and Claims, Jefferson Health
- **Bill Burns** — VP Research and Analytics, MPL Association (industry trade group, Data Sharing Project)
- **Anna Wirth-Granlund, CPHRM, CPCU, ARM** — Director of Risk Financing and Insurance, Temple Health; President, TUHS Insurance Company (captive)
- **Heather A. Tereshko, Esq.** — Principal, Post & Schell (the firm represented HUP in Hagans appeal)

Note: Lisa is at an institution with an active appeal of a nine-figure verdict (Jefferson Einstein); Heather's firm represented HUP in Hagans. Both will likely speak to generalizable themes.

## Other context

- **Volodoc-DrChrono integration work**: kept in a separate dedicated chat per Anish's preference. Does not belong in this project.
- **HTML files in knowledge**: `malpractice_climate_map.html` and `dashboard.html` are the rendered outputs. Claude can read them but iterative editing is awkward — for content changes, edit `parse_naic.py` (data) or the HTML source directly and re-deploy.
