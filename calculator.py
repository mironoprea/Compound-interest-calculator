"""Core compound interest calculation engine."""

from typing import NamedTuple


class YearBreakdown(NamedTuple):
    year: int
    starting_balance: float
    contributions: float
    interest_earned: float
    ending_balance: float


class CalculationResult(NamedTuple):
    final_balance: float
    total_contributions: float
    total_interest: float
    yearly_breakdown: list  # list[YearBreakdown]
    inflation_adjusted_balance: float | None


def calculate_compound_interest(
    principal: float,
    annual_rate: float,
    years: int,
    contribution: float = 0.0,
    contribution_frequency: str = "monthly",
    compounding_frequency: str = "monthly",
    inflation_rate: float | None = None,
) -> CalculationResult:
    """
    Calculate compound interest with optional periodic contributions.

    Args:
        principal: Initial deposit amount.
        annual_rate: Annual interest rate as a percentage (e.g. 7 for 7%).
        years: Number of years to grow.
        contribution: Amount added per contribution period.
        contribution_frequency: "monthly" or "yearly".
        compounding_frequency: "daily", "monthly", "quarterly", or "yearly".
        inflation_rate: Optional annual inflation rate as a percentage.

    Returns:
        CalculationResult with final balance, totals, and yearly breakdown.
    """
    comp_map = {"daily": 365, "monthly": 12, "quarterly": 4, "yearly": 1}
    n = comp_map[compounding_frequency]
    r = annual_rate / 100

    contrib_per_period = _contribution_per_compound_period(
        contribution, contribution_frequency, n
    )

    balance = principal
    total_contributions = principal
    yearly_breakdown: list[YearBreakdown] = []

    for year in range(1, years + 1):
        starting_balance = balance
        year_contributions = 0.0
        year_interest = 0.0

        for _ in range(n):
            interest = balance * (r / n)
            year_interest += interest
            balance += interest + contrib_per_period
            year_contributions += contrib_per_period

        total_contributions += year_contributions
        yearly_breakdown.append(
            YearBreakdown(
                year=year,
                starting_balance=round(starting_balance, 2),
                contributions=round(year_contributions, 2),
                interest_earned=round(year_interest, 2),
                ending_balance=round(balance, 2),
            )
        )

    total_interest = balance - total_contributions

    inflation_adjusted = None
    if inflation_rate is not None:
        inflation_adjusted = balance / ((1 + inflation_rate / 100) ** years)

    return CalculationResult(
        final_balance=round(balance, 2),
        total_contributions=round(total_contributions, 2),
        total_interest=round(total_interest, 2),
        yearly_breakdown=yearly_breakdown,
        inflation_adjusted_balance=round(inflation_adjusted, 2) if inflation_adjusted is not None else None,
    )


def _contribution_per_compound_period(
    contribution: float, contribution_frequency: str, compounds_per_year: int
) -> float:
    """Convert a contribution amount to per-compounding-period amount."""
    if contribution == 0:
        return 0.0
    if contribution_frequency == "yearly":
        return contribution / compounds_per_year
    # monthly contributions
    monthly = contribution
    return monthly * 12 / compounds_per_year
