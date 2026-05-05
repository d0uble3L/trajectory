from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
import os

app = FastAPI(title="Trajectory API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class ProjectionInput(BaseModel):
    current_net_worth: float = Field(..., ge=0)
    annual_income: float = Field(..., ge=0)
    monthly_investment: float = Field(..., ge=0)
    annual_return_rate: float = Field(..., ge=0, le=1)
    annual_income_growth: float = Field(..., ge=0, le=1)
    annual_expenses: float = Field(..., ge=0)
    years: int = Field(default=5, ge=1, le=30)


def calculate_scenario(
    current_net_worth: float,
    annual_income: float,
    monthly_investment: float,
    return_rate: float,
    annual_income_growth: float,
    annual_expenses: float,
    years: int,
) -> list[dict]:
    results = []
    net_worth = current_net_worth
    income = annual_income
    total_principal = current_net_worth

    for year in range(1, years + 1):
        annual_investment = monthly_investment * 12
        investment_gains = net_worth * return_rate
        net_worth = net_worth + annual_investment + investment_gains
        total_principal += annual_investment
        total_gains = net_worth - total_principal
        passive_income = net_worth * 0.04
        savings_rate = ((income - annual_expenses) / income * 100) if income > 0 else 0

        results.append(
            {
                "year": year,
                "net_worth": round(net_worth, 2),
                "total_invested": round(total_principal, 2),
                "investment_gains": round(max(0.0, total_gains), 2),
                "passive_income": round(passive_income, 2),
                "savings_rate": round(max(0.0, min(100.0, savings_rate)), 1),
            }
        )

        income *= 1 + annual_income_growth

    return results


@app.post("/api/project")
def project(data: ProjectionInput):
    conservative_rate = max(0.0, data.annual_return_rate - 0.02)
    moderate_rate = data.annual_return_rate
    optimistic_rate = data.annual_return_rate + 0.02

    conservative = calculate_scenario(
        data.current_net_worth, data.annual_income, data.monthly_investment,
        conservative_rate, data.annual_income_growth, data.annual_expenses, data.years,
    )
    moderate = calculate_scenario(
        data.current_net_worth, data.annual_income, data.monthly_investment,
        moderate_rate, data.annual_income_growth, data.annual_expenses, data.years,
    )
    optimistic = calculate_scenario(
        data.current_net_worth, data.annual_income, data.monthly_investment,
        optimistic_rate, data.annual_income_growth, data.annual_expenses, data.years,
    )

    last = moderate[-1]
    first = moderate[0]

    return {
        "scenarios": {
            "conservative": conservative,
            "moderate": moderate,
            "optimistic": optimistic,
        },
        "summary": {
            "projected_net_worth": last["net_worth"],
            "total_gain": last["investment_gains"],
            "passive_income_final": last["passive_income"],
            "savings_rate": first["savings_rate"],
        },
        "rates": {
            "conservative": conservative_rate,
            "moderate": moderate_rate,
            "optimistic": optimistic_rate,
        },
    }


_frontend_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "frontend")
app.mount("/", StaticFiles(directory=_frontend_dir, html=True), name="static")
