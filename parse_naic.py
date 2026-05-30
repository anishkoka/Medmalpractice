#!/usr/bin/env python3
"""
parse_naic.py — Parse a NAIC Countrywide Summary of Medical Professional Liability
Insurance PDF into the JSON format used by the dashboard.

Usage:
    pip install pdfplumber
    python3 parse_naic.py path/to/MED_MAL_RPT_YYYY.pdf

Outputs:
    naic_medmal_data.json — All state-year records.
    map_data.json        — State-level scoring + history for the dashboard.

Annual update workflow:
    1. NAIC publishes the new vintage of "Countrywide Summary of Medical
       Professional Liability Insurance" (typically 18 months after year-end)
       at https://content.naic.org/insurance-topics/medical-malpractice-insurance
    2. Download the PDF from the Soutron library link.
    3. Run this script.
    4. Update physician counts in PHYSICIAN_COUNTS below from the latest
       AAMC State Physician Workforce Data Report (annual, January).
    5. Commit the updated map_data.json.

Sources:
    NAIC: https://content.naic.org/insurance-topics/medical-malpractice-insurance
    AAMC: https://www.aamc.org/data-reports/data/2024-key-findings-and-definitions
"""

import sys
import re
import json
from pathlib import Path

# ============================================================
# AAMC State Physician Workforce Data Report — total active physicians
# Update this annually from the latest AAMC data report.
# Current values: 2023 vintage. NAIC data current through CY2024.
# ============================================================
PHYSICIAN_COUNTS = {
    'MA': 32116, 'MD': 23791, 'NY': 75749, 'VT': 2410, 'RI': 4063,
    'CT': 12977, 'ME': 4459, 'PA': 42051, 'NH': 4391, 'HI': 4557,
    'NJ': 27832, 'MN': 17617, 'OR': 13127, 'OH': 35333, 'MI': 30040,
    'MO': 18297, 'CO': 16956, 'IL': 37122, 'DE': 2850, 'CA': 113718,
    'AK': 2101, 'WA': 21731, 'WI': 15975, 'WV': 4914, 'FL': 58822,
    'LA': 12557, 'VA': 22874, 'NC': 27650, 'TN': 17687, 'MT': 2750,
    'AZ': 18343, 'NM': 5269, 'SD': 2214, 'NE': 4820, 'ND': 1826,
    'SC': 12197, 'IN': 15918, 'GA': 25072, 'KS': 6874, 'KY': 10528,
    'TX': 67182, 'UT': 7198, 'AL': 10983, 'IA': 7056, 'NV': 6731,
    'AR': 6500, 'WY': 1225, 'OK': 8293, 'MS': 5857, 'ID': 3504,
    'DC': 5852,
}

# ============================================================
# Cap structure scoring + ATRA litigation environment
# Cap data verified Apr 2026 against state codes via Tavrn aggregator
# (April 2026 update, with statutory citations) cross-checked against
# AMA State Laws Chart I and primary state-code lookups. ATRA data
# from 2025–26 Judicial Hellholes Report.
#
# Cap-score bucket key:
#   0 = Strong cap (≤$500K noneconomic) OR PCF state limiting MD personal exposure
#  10 = Moderate cap ($500K-$1M noneconomic)
#  20 = Weak/partial cap (>$1M total cap, OR cap only on subset)
#  30 = No cap (struck unconstitutional or never enacted)
#  35 = Constitutional bar to enacting caps
#
# Litig-score bucket: 0 none / 5 ATRA Watch List / 10 Hellhole #5-8 / 15 Hellhole #1-4
# ============================================================
STATE_INPUTS = {
    "AK": {"name": "Alaska", "fips": "02", "cap": 0,  "litig": 0,  "cap_note": "$250K noneconomic / $400K severe (AS § 09.55.549)"},
    "AL": {"name": "Alabama", "fips": "01", "cap": 30, "litig": 0,  "cap_note": "Cap struck (Moore v. Mobile Infirmary, 1991)"},
    "AR": {"name": "Arkansas", "fips": "05", "cap": 35, "litig": 0,  "cap_note": "Constitutional bar (Ark Const Art 5 § 32)"},
    "AZ": {"name": "Arizona", "fips": "04", "cap": 35, "litig": 0,  "cap_note": "Constitutional bar (Ariz Const Art 2 § 31, Art 18 § 6)"},
    "CA": {"name": "California", "fips": "06", "cap": 0,  "litig": 15, "cap_note": "MICRA: $470K noneconomic (2026), scaling to $750K by 2033 (Civ Code § 3333.2). LA ATRA Hellhole #4"},
    "CO": {"name": "Colorado", "fips": "08", "cap": 10, "litig": 0,  "cap_note": "$530K noneconomic (2026), scaling to $875K by 2029 (CRS § 13-64-302; HB24-1472)"},
    "CT": {"name": "Connecticut", "fips": "09", "cap": 30, "litig": 0,  "cap_note": "No cap (no statute enacted)"},
    "DC": {"name": "DC", "fips": "11", "cap": 30, "litig": 0,  "cap_note": "No cap"},
    "DE": {"name": "Delaware", "fips": "10", "cap": 30, "litig": 0,  "cap_note": "No cap (no statute enacted)"},
    "FL": {"name": "Florida", "fips": "12", "cap": 30, "litig": 0,  "cap_note": "Cap struck (N. Broward Hosp Dist v. Kalitan, 2017)"},
    "GA": {"name": "Georgia", "fips": "13", "cap": 30, "litig": 0,  "cap_note": "Cap struck (Atlanta Oculoplastic v. Nestlehutt, 2010)"},
    "HI": {"name": "Hawaii", "fips": "15", "cap": 10, "litig": 0,  "cap_note": "$375K cap on pain-and-suffering only; other noneconomic uncapped (HRS § 663-8.7)"},
    "IA": {"name": "Iowa", "fips": "19", "cap": 10, "litig": 0,  "cap_note": "$250K base; $1M clinics / $2M hospitals for severe injury (Iowa Code § 147.136A)"},
    "ID": {"name": "Idaho", "fips": "16", "cap": 0,  "litig": 0,  "cap_note": "$510K noneconomic cap, indexed (Idaho Code § 6-1603)"},
    "IL": {"name": "Illinois", "fips": "17", "cap": 30, "litig": 10, "cap_note": "Cap struck (LeBron v. Gottlieb Memorial Hospital, 2010). Cook/Madison/St. Clair ATRA Hellhole #7"},
    "IN": {"name": "Indiana", "fips": "18", "cap": 0,  "litig": 0,  "cap_note": "$1.8M total cap; MD personal exposure $500K, PCF pays excess (Ind Code § 34-18-14-3)"},
    "KS": {"name": "Kansas", "fips": "20", "cap": 30, "litig": 0,  "cap_note": "Cap struck (Hilburn v. Enerpipe, 2019)"},
    "KY": {"name": "Kentucky", "fips": "21", "cap": 35, "litig": 5,  "cap_note": "Constitutional bar (Ky Const § 54)"},
    "LA": {"name": "Louisiana", "fips": "22", "cap": 0,  "litig": 15, "cap_note": "$500K total cap (ex. future medical); MD exposure $100K, PCF pays excess (La RS § 40:1231.2). ATRA Hellhole #1"},
    "MA": {"name": "Massachusetts", "fips": "25", "cap": 0,  "litig": 0,  "cap_note": "$500K noneconomic cap (MGL ch. 231 § 60H)"},
    "MD": {"name": "Maryland", "fips": "24", "cap": 10, "litig": 0,  "cap_note": "$920K noneconomic cap, +$15K/yr (Cts & Jud Proc § 3-2A-09)"},
    "ME": {"name": "Maine", "fips": "23", "cap": 30, "litig": 0,  "cap_note": "No cap on noneconomic (no statute except ~$1M wrongful-death cap)"},
    "MI": {"name": "Michigan", "fips": "26", "cap": 10, "litig": 5,  "cap_note": "$596K standard / $1.07M catastrophic, indexed (MCL § 600.1483)"},
    "MN": {"name": "Minnesota", "fips": "27", "cap": 30, "litig": 0,  "cap_note": "No cap (no statute enacted)"},
    "MO": {"name": "Missouri", "fips": "29", "cap": 0,  "litig": 10, "cap_note": "$481K noneconomic / $843K catastrophic, indexed 1.7%/yr (RSMo § 538.210). St. Louis ATRA Hellhole #6"},
    "MS": {"name": "Mississippi", "fips": "28", "cap": 0,  "litig": 0,  "cap_note": "$500K noneconomic cap, fixed (Miss Code § 11-1-60)"},
    "MT": {"name": "Montana", "fips": "30", "cap": 0,  "litig": 0,  "cap_note": "$350K noneconomic (2026), scaling to $500K by 2029 (MCA § 25-9-411; HB 195/2025)"},
    "NC": {"name": "N. Carolina", "fips": "37", "cap": 10, "litig": 0,  "cap_note": "$713K noneconomic cap, CPI-adjusted (NC GS § 90-21.19)"},
    "ND": {"name": "N. Dakota", "fips": "38", "cap": 0,  "litig": 0,  "cap_note": "$500K noneconomic cap, fixed (ND Cent Code § 32-42-02)"},
    "NE": {"name": "Nebraska", "fips": "31", "cap": 0,  "litig": 0,  "cap_note": "$2.25M total cap; MD exposure $800K via Excess Liability Fund (Neb RS § 44-2825)"},
    "NH": {"name": "N. Hampshire", "fips": "33", "cap": 30, "litig": 0,  "cap_note": "Cap struck (Carson v. Maurer, 1980; Brannigan v. Usitalo, 1991)"},
    "NJ": {"name": "New Jersey", "fips": "34", "cap": 30, "litig": 0,  "cap_note": "No cap (no statute enacted)"},
    "NM": {"name": "New Mexico", "fips": "35", "cap": 10, "litig": 0,  "cap_note": "$770K physician / $1M independent facility / $5.5M hospital; PCF state (NMSA § 41-5-6)"},
    "NV": {"name": "Nevada", "fips": "32", "cap": 10, "litig": 0,  "cap_note": "$590K noneconomic (2026), scaling to $750K by 2028 (NRS § 41A.035)"},
    "NY": {"name": "New York", "fips": "36", "cap": 30, "litig": 15, "cap_note": "No cap (no statute enacted). NYC ATRA Hellhole #2"},
    "OH": {"name": "Ohio", "fips": "39", "cap": 0,  "litig": 0,  "cap_note": "$250K base / max $350K per plaintiff; $500K catastrophic (Ohio RC § 2323.43)"},
    "OK": {"name": "Oklahoma", "fips": "40", "cap": 30, "litig": 0,  "cap_note": "Cap struck (Beason v. I.E. Miller Services, 2019)"},
    "OR": {"name": "Oregon", "fips": "41", "cap": 30, "litig": 0,  "cap_note": "Cap struck (Busch v. McInnis Waste Systems, 2020)"},
    "PA": {"name": "Pennsylvania", "fips": "42", "cap": 35, "litig": 10, "cap_note": "Constitutional bar (PA Const Art III § 18). Philly ATRA Hellhole #5"},
    "RI": {"name": "Rhode Island", "fips": "44", "cap": 30, "litig": 0,  "cap_note": "No cap (no statute enacted)"},
    "SC": {"name": "S. Carolina", "fips": "45", "cap": 10, "litig": 15, "cap_note": "$580K per provider / $1.74M aggregate, indexed (SC Code § 15-32-220). ATRA Hellhole #3"},
    "SD": {"name": "S. Dakota", "fips": "46", "cap": 0,  "litig": 0,  "cap_note": "$500K noneconomic cap, fixed (SDCL § 21-3-11)"},
    "TN": {"name": "Tennessee", "fips": "47", "cap": 10, "litig": 0,  "cap_note": "$750K noneconomic / $1M catastrophic (Tenn Code § 29-39-102)"},
    "TX": {"name": "Texas", "fips": "48", "cap": 0,  "litig": 5,  "cap_note": "$250K per MD / $250K per institution (max $500K from institutions) (Tex CPRC § 74.301). Watch List"},
    "UT": {"name": "Utah", "fips": "49", "cap": 0,  "litig": 0,  "cap_note": "$450K noneconomic cap, fixed (Utah Code § 78B-3-410)"},
    "VA": {"name": "Virginia", "fips": "51", "cap": 20, "litig": 0,  "cap_note": "$2.70M total cap (FY2025–26), rising to $3M by 2031 (Va Code § 8.01-581.15)"},
    "VT": {"name": "Vermont", "fips": "50", "cap": 30, "litig": 0,  "cap_note": "No cap (no statute enacted)"},
    "WA": {"name": "Washington", "fips": "53", "cap": 30, "litig": 10, "cap_note": "Cap struck (Sofie v. Fibreboard, 1989). King Co/WA SC ATRA #8"},
    "WI": {"name": "Wisconsin", "fips": "55", "cap": 0,  "litig": 0,  "cap_note": "$750K noneconomic cap, fixed; IPFCF backstop (Wis Stat § 893.55)"},
    "WV": {"name": "W. Virginia", "fips": "54", "cap": 0,  "litig": 0,  "cap_note": "$375K noneconomic / $750K wrongful-death/catastrophic (W Va Code § 55-7B-8)"},
    "WY": {"name": "Wyoming", "fips": "56", "cap": 35, "litig": 0,  "cap_note": "Constitutional bar (WY Const Art 10 § 4)"},
}


def parse_naic_pdf(pdf_path):
    """Extract all state-year records from the NAIC PDF."""
    try:
        import pdfplumber
    except ImportError:
        sys.exit("ERROR: pdfplumber not installed. Run: pip install pdfplumber")

    state_codes = set(PHYSICIAN_COUNTS.keys())
    pattern = re.compile(
        r'^(\d{4})\s+([A-Z]{2})\s+(\d+)\s+'
        r'(-?[\d,]+)\s+(-?[\d,]+)\s+(-?[\d,]+)\s+(-?[\d,]+)\s+(-?[\d.]+)$'
    )

    def parse_num(s):
        return int(s.replace(',', ''))

    records = []
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text() or ""
            for line in text.split('\n'):
                m = pattern.match(line.strip())
                if m and m.group(2) in state_codes:
                    year, state, n, dpw, dpe, dli, dcc, ratio = m.groups()
                    records.append({
                        'year': int(year),
                        'state': state,
                        'insurers': int(n),
                        'direct_premium_written': parse_num(dpw),
                        'direct_premium_earned': parse_num(dpe),
                        'direct_losses_incurred': parse_num(dli),
                        'direct_dcc_incurred': parse_num(dcc),
                        'loss_dcc_ratio': float(ratio)
                    })

    seen = set()
    unique = []
    for r in records:
        key = (r['year'], r['state'])
        if key not in seen:
            seen.add(key)
            unique.append(r)
    return unique


def score_naic(per_phys):
    """0-25 point scale based on NAIC premium per physician."""
    if per_phys < 5500: return 0
    elif per_phys < 7500: return 5
    elif per_phys < 10000: return 10
    elif per_phys < 13000: return 15
    elif per_phys < 16000: return 20
    else: return 25


def rating_for(score):
    if score <= 25: return "green"
    if score <= 45: return "yellow"
    return "red"


def build_map_data(records):
    """Build the dashboard's map_data.json."""
    by_state = {}
    for r in records:
        by_state.setdefault(r['state'], []).append(r)

    final = {}
    for code, inp in STATE_INPUTS.items():
        if code not in by_state:
            print(f"  WARNING: No NAIC data for {code}", file=sys.stderr)
            continue
        history = sorted(by_state[code], key=lambda r: r['year'])
        latest = history[-1]
        # Find a record 5 years prior
        target_year = latest['year'] - 5
        prior = next((h for h in history if h['year'] == target_year), history[0])

        phys = PHYSICIAN_COUNTS[code]
        ppp = round(latest['direct_premium_written'] / phys)
        naic_score = score_naic(ppp)
        total = inp['cap'] + naic_score + inp['litig']

        final[code] = {
            'name': inp['name'],
            'code': code,
            'fips': inp['fips'],
            'cap_score': inp['cap'],
            'naic_score': naic_score,
            'litig_score': inp['litig'],
            'total_score': total,
            'rating': rating_for(total),
            'cap_note': inp['cap_note'],
            'naic_dpw': latest['direct_premium_written'],
            'naic_loss_ratio': latest['loss_dcc_ratio'],
            'naic_premium_per_physician': ppp,
            'physicians': phys,
            'naic_2014_dpw': prior['direct_premium_written'],
            'pct_change_5yr': round(
                (latest['direct_premium_written'] - prior['direct_premium_written']) /
                prior['direct_premium_written'] * 100, 1
            ),
            'history': [
                {'year': h['year'], 'dpw': h['direct_premium_written'],
                 'loss_ratio': h['loss_dcc_ratio']}
                for h in history
            ]
        }
    return final


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python3 parse_naic.py <NAIC_PDF_PATH>")

    pdf_path = Path(sys.argv[1])
    if not pdf_path.exists():
        sys.exit(f"File not found: {pdf_path}")

    print(f"Parsing {pdf_path}...")
    records = parse_naic_pdf(pdf_path)
    print(f"  Extracted {len(records)} state-year records")
    years = sorted(set(r['year'] for r in records))
    print(f"  Years: {years[0]}–{years[-1]}")

    # Save raw
    with open('naic_medmal_data.json', 'w') as f:
        json.dump(records, f, indent=1)
    print("  -> naic_medmal_data.json")

    # Build dashboard data
    print("Building map_data.json...")
    map_data = build_map_data(records)
    with open('map_data.json', 'w') as f:
        json.dump(map_data, f, indent=1)
    print(f"  -> map_data.json ({len(map_data)} states)")

    # Summary
    buckets = {'green': 0, 'yellow': 0, 'red': 0}
    for d in map_data.values():
        buckets[d['rating']] += 1
    print(f"\nDistribution: G={buckets['green']} Y={buckets['yellow']} R={buckets['red']}")
    print("Done.")


if __name__ == '__main__':
    main()
