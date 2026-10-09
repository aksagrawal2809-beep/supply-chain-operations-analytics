# Supply Chain Excellence Analytics: Brewery Operations Case Study

## Project purpose
A portfolio project aligned to the AB InBev Supply Excellence Trainee (SET) internship. It explores manufacturing productivity, downtime, quality, energy intensity, freight cost, and delivery reliability using **synthetic demonstration data**.

**Important:** This is an independent student case study. The data are simulated and are not AB InBev data. Do not present the results as real company findings.

## Business question
How could a brewery operations team prioritize improvement opportunities across production and logistics while balancing output, quality, cost, and service?

## Included
- `data/daily_operations.csv` — 240 synthetic daily plant-line observations.
- `src/analyze_operations.py` — Python analysis and chart generation.
- `sql/schema_and_queries.sql` — SQL table definition and example analyses.
- `powerbi/dashboard_blueprint.md` — dashboard pages, measures, and build steps.
- `reports/project_report.md` — executive-style report and recommended pilot.
- `reports/presentation_outline.md` — 5-slide presentation outline.
- `requirements.txt` — Python dependencies.

## Quick start
1. Install Python 3.10+.
2. Run `
`.
3. Run `python src/analyze_operations.py`.
4. Open `outputs/` for summary CSVs and charts.

## Core KPIs
- Production attainment = actual good units / planned units
- Downtime rate (proxy) = downtime minutes / (downtime minutes + 480 planned shift minutes)
- Defect rate
- Energy intensity = energy kWh / actual good units
- Freight cost per shipment
- On-time delivery rate

## Suggested Power BI pages
1. Executive Overview: output attainment, downtime, defect rate, freight cost, on-time delivery.
2. Manufacturing: plant/line comparison, downtime vs attainment, energy intensity.
3. Logistics: freight cost per shipment, route distance, on-time delivery.
4. Improvement Tracker: baseline, target, owner, status, estimated benefit.

## How to discuss it in an interview
Say: "I built a simulated operations dataset to demonstrate how I would structure a supply-chain improvement problem. I used Python for data cleaning and KPI analysis, SQL for repeatable business questions, and Power BI to design a decision-oriented dashboard. The numbers are illustrative, so I would validate the baseline with plant data before estimating savings."
