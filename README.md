# Trajectory

A 5-year personal net worth visualizer. Enter your financial parameters and see three projection scenarios — conservative, moderate, and optimistic — update in real time.

## Quick Start (Docker)

```bash
docker-compose up --build
```

Open [http://localhost:8000](http://localhost:8000)

## Development (without Docker)

```bash
pip install -r backend/requirements.txt
uvicorn backend.main:app --reload
```

Open [http://localhost:8000](http://localhost:8000)

## API

**`POST /api/project`**

```json
{
  "current_net_worth": 50000,
  "annual_income": 80000,
  "monthly_investment": 1000,
  "annual_return_rate": 0.08,
  "annual_income_growth": 0.03,
  "annual_expenses": 48000,
  "years": 5
}
```

Returns `scenarios` (conservative / moderate / optimistic) each with year-by-year: `net_worth`, `total_invested`, `investment_gains`, `passive_income`, `savings_rate`. Also returns a `summary` block with headline metrics.

## Scenario Logic

| Scenario    | Return Rate          |
|-------------|----------------------|
| Conservative | rate − 2%           |
| Moderate     | rate (as entered)   |
| Optimistic   | rate + 2%           |

Passive income = portfolio × 4% (safe withdrawal rate).
