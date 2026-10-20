# Ayebot Southeast Asia Buyer Index

**The Ayebot Southeast Asia Buyer Index is an open monthly dataset of how many acquirers are mapped in each of 12 sectors across 6 Southeast Asian markets (Singapore, Malaysia, Indonesia, Thailand, Vietnam, Philippines). The October 2026 snapshot covers 2,358 unique acquirers; the smallest sector and market cell is Education in the Philippines (21 acquirers) and the largest is Healthcare in Singapore (192).** It contains aggregate counts only. No buyer names, no deal data.

Live explorer: https://ayebot.com/buyers · Method in plain English: https://ayebot.com/how-it-works

## What is in this repository

| File | Content |
|---|---|
| `data/YYYY-MM.csv` | Tidy table, one row per sector and market: `snapshot_date, sector, market, mapped_acquirers` (72 rows) |
| `data/YYYY-MM.json` | Headline figures for the month, plus sector and market labels |
| `data/latest.csv`, `data/latest.json` | Copies of the newest month |
| `scripts/snapshot.py` | Fetches the live index and writes the month's files (standard library only) |
| `datapackage.json` | Frictionless Data descriptor |
| `CITATION.cff` | Machine-readable citation |

### Columns (`data/*.csv`)

| Column | Type | Meaning |
|---|---|---|
| `snapshot_date` | date | Date the index was generated (ISO 8601) |
| `sector` | string | One of 12 sector codes (labels in `data/*.json`) |
| `market` | string | `sg`, `my`, `id`, `th`, `vn`, `ph` |
| `mapped_acquirers` | integer | Unique acquirers that state interest in the sector and cover the market (see definition below) |

Sector codes: `healthcare`, `beauty`, `consumer`, `fnb`, `education`, `logistics`, `industrial`, `building`, `technology`, `services`, `financial`, `energy`.

### Headline fields (`data/*.json`)

| Field | October 2026 | Meaning |
|---|---|---|
| `register_unique_buyers` / `headline.unique` | 2,358 | De-duplicated acquirers on the register |
| `headline.pe` | 406 | Of which private equity |
| `headline.strategic` | 1,541 | Of which strategic (operating companies, including PE-backed operating companies) |
| `headline.listed` | 332 | Of which flagged as listed companies |

Private equity and strategic are not exhaustive: family offices, pension and sovereign funds and unclassified buyers make up the remainder.

## What "mapped acquirer" means

A mapped acquirer is a company or investor on the Ayebot buyer register that has stated interest in a given sector and whose stated geography covers a given market. A buyer counts in a market if it names that market directly, or carries a region-wide mandate (for example Southeast Asia, ASEAN or Asia Pacific), or a global mandate. "Mapped" means recorded on the register with those stated criteria. It does not mean the buyer is active, funded or willing to transact today.

## Method

1. The buyer register is compiled by Ayebot from public sources and its own work. Each record holds the buyer's stated target sectors, target geographies, category and, where known, a target revenue range.
2. Records are de-duplicated on company name after stripping legal suffixes (for example Pte, Ltd, Limited, Sdn Bhd, Group, Holdings), so the same company written two ways counts once.
3. Each record's sector text is matched against keyword patterns for the 12 sectors. Each record's geography text is matched against the 6 markets.
4. For every sector and market pair, the index counts distinct buyers that match the sector and whose geography names the market, or is region-wide, or is global.
5. Buyer type: private equity, strategic, family office or other, from the buyer's recorded category. Operating companies owned by a PE firm are counted as strategic. Pension and sovereign funds are counted as other.
6. Only integer counts are published. The builder aborts if any non-numeric value appears.

The source is one file, https://ayebot.com/data/buyer-index.json, which is the same data shown on https://ayebot.com/buyers. `scripts/snapshot.py` reads it, keeps the fields listed above and refuses to write if the source carries any field it does not recognise.

## Coverage

- 12 sectors: healthcare and medical; beauty, aesthetics and wellness; consumer brands and retail; food and beverage; education; logistics and supply chain; industrial and engineering; building services and infrastructure; technology and software; business and professional services; financial services; energy and environment.
- 6 markets: Singapore, Malaysia, Indonesia, Thailand, Vietnam, Philippines.
- Buyers worldwide are included if their stated mandate covers one or more of those markets.
- Snapshots: October 2026 onwards, one per month.

## Known limitations

- The register is compiled by Ayebot from public sources and its own work. These counts are not a census of the market and are not independently audited.
- A buyer's interest is its stated appetite. It is not a commitment, mandate or offer.
- Sector and market matching uses keyword patterns on recorded text, so some buyers may be misclassified or missed.
- Counts overlap between cells. One buyer can sit in many sectors and many markets, and region-wide and global mandates count in every market. Do not add the 72 cells together to get a number of buyers; use `register_unique_buyers`.
- A large share of the count in smaller markets comes from region-wide and global mandates rather than from buyers that name the market.
- Buyer type and listed status are approximate classifications from recorded categories.
- Fields on headquarters location are deliberately not published, because that part of the register is not accurate enough to release.
- The index contains no data from any live sale process.

## Update cadence

Monthly. Each month adds `data/YYYY-MM.*` and refreshes `data/latest.*`. Earlier months are never rewritten.

## How to cite

> Ayebot (2026). *Ayebot Southeast Asia Buyer Index*, October 2026 snapshot. https://github.com/gweeyichen/ayebot-buyer-index

Short form: "Ayebot (ayebot.com), Southeast Asia Buyer Index, October 2026." See `CITATION.cff`.

## Licence

Data released under Creative Commons Attribution 4.0 International (CC BY 4.0). You may copy, redistribute and adapt it, including commercially, provided you credit **"Ayebot (ayebot.com)"** and link to https://ayebot.com/buyers. Full text in `LICENSE`.

## Contact

hi@ayebot.com
