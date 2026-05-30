# Climate Map & Dashboard — What They Show

**Last refreshed:** April 2026 — NAIC vintage through CY2024, cap data verified against state codes

The HTML files (`malpractice_climate_map.html` and `dashboard.html`) are the rendered visual outputs. This document describes what they contain so a Claude reading from knowledge can answer questions without parsing the HTML.

## `malpractice_climate_map.html` — Static map

A US choropleth showing each state's composite score (0–75) on the medical malpractice climate, color-coded green/yellow/red. Hovering on a state surfaces a tooltip with:

- Composite score and three component scores
- NAIC 2024 direct premium written
- Premium per active physician
- Loss & DCC ratio
- 5-year DPW change with trend arrow
- Cap note with statutory or case citation

The methodology is shown on-page in a card explaining the three components and their scoring. Source line cites NAIC 2010–2024, AAMC 2023, ATRA 2025–26, and state codes (see `medmal_cap_citations.md` for full citations).

## `dashboard.html` — Interactive recurring-update dashboard

Loads `map_data.json` dynamically. Vintage labels are auto-detected from data.

Four view modes (toggle at top):
1. **Composite Rating** — same as static map
2. **Premium $/MD** — continuous color ramp on premium per physician
3. **Loss Ratio** — color ramp on loss & DCC ratio (red = >100%)
4. **5-yr Trend** — DPW change 2019→2024

State detail panel: clicking a state reveals full breakdown including 15-year DPW history.

Time-series chart at bottom: click states to add/remove from comparison. Four presets:
- Benchmarks (PA, NY, TX, CA)
- All hostile states
- Reform states (CA, TX, IN, WI)
- Clear

## Full state table (2024 vintage, refreshed April 2026)

Sorted by composite score, descending. Loss% is the NAIC 2024 loss & DCC ratio. Distribution: 21 green / 12 yellow / 18 red.

| Rank | State | Score | $/MD | Loss% | 5yr Δ | Rating | Cap status |
|---|---|---|---|---|---|---|---|
| 1 | New York | 70 | $23,628 | 77.0% | +12.9% | red | No cap (no statute enacted). NYC ATRA Hellhole #2 |
| 2 | Pennsylvania | 70 | $21,684 | 97.5% | +26.7% | red | Constitutional bar (PA Const Art III § 18). Philly ATRA Hellhole #5 |
| 3 | Illinois | 65 | $16,642 | 65.2% | +36.2% | red | Cap struck (LeBron v. Gottlieb, 2010). Cook/Madison/St. Clair ATRA #7 |
| 4 | Wyoming | 60 | $20,231 | 53.6% | +31.0% | red | Constitutional bar (WY Const Art 10 § 4) |
| 5 | Kentucky | 60 | $15,107 | 126.5% | +43.0% | red | Constitutional bar (Ky Const § 54) |
| 6 | New Jersey | 55 | $20,823 | 78.3% | +38.2% | red | No cap (no statute enacted) |
| 7 | Connecticut | 55 | $19,723 | 132.4% | +24.7% | red | No cap (no statute enacted) |
| 8 | Georgia | 55 | $18,445 | 108.6% | +62.2% | red | Cap struck (Atlanta Oculoplastic v. Nestlehutt, 2010) |
| 9 | Alabama | 55 | $18,248 | 72.3% | +53.6% | red | Cap struck (Moore v. Mobile Infirmary, 1991) |
| 10 | Florida | 55 | $17,891 | 68.5% | +62.4% | red | Cap struck (N. Broward Hosp Dist v. Kalitan, 2017) |
| 11 | Delaware | 55 | $16,140 | 79.1% | +52.4% | red | No cap (no statute enacted) |
| 12 | Kansas | 55 | $16,111 | 78.5% | +58.1% | red | Cap struck (Hilburn v. Enerpipe, 2019) |
| 13 | Arizona | 55 | $14,899 | 63.4% | +29.6% | red | Constitutional bar (Ariz Const Art 2 § 31, Art 18 § 6) |
| 14 | Arkansas | 55 | $13,995 | 66.0% | +41.3% | red | Constitutional bar (Ark Const Art 5 § 32) |
| 15 | Washington | 55 | $11,514 | 64.0% | +30.9% | red | Cap struck (Sofie v. Fibreboard, 1989). King Co/WA SC ATRA #8 |
| 16 | Oklahoma | 50 | $15,012 | 73.3% | +27.2% | red | Cap struck (Beason v. I.E. Miller Services, 2019) |
| 17 | New Hampshire | 50 | $14,859 | 23.8% | +33.9% | red | Cap struck (Carson v. Maurer, 1980; Brannigan v. Usitalo, 1991) |
| 18 | Maine | 50 | $13,218 | 53.2% | +13.2% | red | No cap on noneconomic (no statute except wrongful-death) |
| 19 | Rhode Island | 45 | $10,784 | 120.2% | +38.7% | yellow | No cap (no statute enacted) |
| 20 | Vermont | 45 | $10,047 | 106.9% | +42.1% | yellow | No cap (no statute enacted) |
| 21 | Oregon | 40 | $9,570 | 83.6% | +37.8% | yellow | Cap struck (Busch v. McInnis Waste Systems, 2020) |
| 22 | New Mexico | 35 | $18,258 | 122.8% | +60.4% | yellow | $770K MD / $1M indep / $5.5M hospital; PCF (NMSA § 41-5-6) |
| 23 | Nevada | 35 | $17,181 | 47.8% | +55.1% | yellow | $590K noneconomic (2026), → $750K by 2028 (NRS § 41A.035) |
| 24 | Tennessee | 35 | $16,837 | 60.4% | +26.8% | yellow | $750K noneconomic / $1M catastrophic (Tenn Code § 29-39-102) |
| 25 | Virginia | 35 | $11,173 | 50.9% | +36.5% | yellow | $2.70M total cap, → $3M by 2031 (Va Code § 8.01-581.15) |
| 26 | South Carolina | 35 | $8,056 | -1.2% | +22.7% | yellow | $580K per provider / $1.74M aggregate. ATRA #3 |
| 27 | Minnesota | 35 | $6,624 | 59.7% | +39.8% | yellow | No cap (no statute enacted) |
| 28 | Maryland | 30 | $14,271 | 50.8% | +12.8% | yellow | $920K noneconomic cap, +$15K/yr (Cts & Jud Proc § 3-2A-09) |
| 29 | Iowa | 30 | $14,002 | 33.9% | +45.4% | yellow | $250K base; $1M/$2M severe (Iowa Code § 147.136A) |
| 30 | DC | 30 | $5,440 | 101.2% | +23.8% | yellow | No cap |
| 31 | Montana | 25 | $16,792 | 185.2% | +29.5% | green | $350K noneconomic (2026), → $500K by 2029 (MCA § 25-9-411) |
| 32 | West Virginia | 25 | $16,394 | 75.5% | -16.6% | green | $375K noneconomic / $750K wrongful-death (W Va Code § 55-7B-8) |
| 33 | Missouri | 25 | $12,018 | 74.5% | +41.7% | green | $481K noneconomic / $843K catastrophic. St. Louis ATRA #6 |
| 34 | Colorado | 25 | $11,885 | 61.1% | +33.2% | green | $530K noneconomic (2026), → $875K by 2029 (HB24-1472) |
| 35 | California | 25 | $9,397 | 62.9% | +31.4% | green | MICRA: $470K (2026), → $750K by 2033. LA ATRA #4 |
| 36 | Louisiana | 25 | $9,309 | 49.2% | +14.5% | green | $500K total cap; MD exposure $100K, PCF pays excess. ATRA #1 |
| 37 | Michigan | 25 | $8,794 | 67.7% | +34.0% | green | $596K / $1.07M catastrophic, indexed (MCL § 600.1483) |
| 38 | Nebraska | 20 | $15,754 | 77.0% | +122.3% | green | $2.25M total; MD exposure $800K via Excess Liability Fund |
| 39 | Idaho | 20 | $13,177 | 9.9% | +35.7% | green | $510K noneconomic cap, indexed (Idaho Code § 6-1603) |
| 40 | Utah | 20 | $13,174 | 73.7% | +67.5% | green | $450K noneconomic cap, fixed (Utah Code § 78B-3-410) |
| 41 | Massachusetts | 20 | $13,143 | 74.9% | +24.3% | green | $500K noneconomic cap (MGL ch. 231 § 60H) |
| 42 | Hawaii | 20 | $9,215 | 85.7% | +39.5% | green | $375K p&s only; other noneconomic uncapped (HRS § 663-8.7) |
| 43 | North Carolina | 20 | $8,142 | 45.1% | +12.9% | green | $713K noneconomic cap, CPI-adjusted (NC GS § 90-21.19) |
| 44 | Alaska | 15 | $12,965 | 43.2% | +13.1% | green | $250K noneconomic / $400K severe (AS § 09.55.549) |
| 45 | Indiana | 15 | $11,757 | 52.5% | +46.5% | green | $1.8M total; MD exposure $500K, PCF pays excess |
| 46 | Mississippi | 15 | $11,177 | 61.3% | +45.0% | green | $500K noneconomic cap, fixed (Miss Code § 11-1-60) |
| 47 | Texas | 15 | $8,504 | 44.2% | +66.5% | green | $250K per MD / $250K per institution (Tex CPRC § 74.301). Watch List |
| 48 | South Dakota | 10 | $9,414 | 15.5% | +32.6% | green | $500K noneconomic cap, fixed (SDCL § 21-3-11) |
| 49 | Ohio | 10 | $8,136 | 36.6% | +21.6% | green | $250K base / max $350K per plaintiff (Ohio RC § 2323.43) |
| 50 | Wisconsin | 5 | $6,871 | 58.3% | +45.3% | green | $750K noneconomic cap, fixed; IPFCF backstop (Wis Stat § 893.55) |
| 51 | North Dakota | 5 | $6,508 | 21.7% | +0.9% | green | $500K noneconomic cap, fixed (ND Cent Code § 32-42-02) |

## How to interpret the loss ratio

Loss & DCC ratio = (direct losses incurred + direct defense and cost containment expenses) ÷ direct premiums earned. A ratio over 100% means insurers paid out more in losses and defense costs than they collected in premium that year — unsustainable without rate increases or market exit.

The 2024 countrywide ratio is 71.05%; the 15-year mean is 67.58%. Five states exceeded 100% in 2024:
- Montana 185.2% (small market, volatility from few large cases)
- Connecticut 132.4%
- Kentucky 126.5%
- New Mexico 122.8%
- Rhode Island 120.2%

PA at 97.5% is the highest among large markets — unusual and structurally meaningful.

## Significant changes from earlier project versions

The cap structure data was rebuilt in April 2026 against authoritative sources. The largest correction:

- **Kansas moved from green to red.** Earlier project versions had Kansas at a $350K cap "recently restored." That was wrong. Kansas's cap was struck by the Kansas Supreme Court in *Hilburn v. Enerpipe* (2019) and has NOT been restored.

Other notable corrections (see `medmal_cap_citations.md` for full list):
- Hawaii moved from yellow to green (HRS § 663-8.7 imposes $375K cap on pain-and-suffering)
- Wyoming moved from yellow to red (constitutional bar under WY Const Art 10 § 4)
- Minnesota and Nevada moved from green to yellow (refined scoring)
- Tennessee and Virginia moved from green to yellow (refined scoring)
- Massachusetts and West Virginia moved into stronger-green tier

The PA story is unchanged: $21,684/MD, 97.5% loss ratio, constitutional bar to caps, Philadelphia ATRA #5. Score 70/75.
