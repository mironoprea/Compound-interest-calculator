"""Unit tests for the compound interest calculator."""

import pytest
from calculator import calculate_compound_interest


class TestBasicCompoundInterest:
    def test_no_contributions_annual_compounding(self):
        """$10,000 at 10% annual for 5 years = $16,105.10"""
        result = calculate_compound_interest(
            principal=10000, annual_rate=10, years=5,
            compounding_frequency="yearly",
        )
        assert result.final_balance == 16105.10
        assert result.total_contributions == 10000.0
        assert result.total_interest == 6105.10

    def test_no_contributions_monthly_compounding(self):
        """$10,000 at 10% monthly compounding for 5 years = $16,453.09"""
        result = calculate_compound_interest(
            principal=10000, annual_rate=10, years=5,
            compounding_frequency="monthly",
        )
        # Known value: 10000 * (1 + 0.10/12)^(12*5) = 16453.09
        assert result.final_balance == pytest.approx(16453.09, abs=1.0)

    def test_zero_interest_rate(self):
        """0% rate should return principal + contributions only."""
        result = calculate_compound_interest(
            principal=5000, annual_rate=0, years=10,
            contribution=100, contribution_frequency="monthly",
            compounding_frequency="monthly",
        )
        expected_contributions = 5000 + (100 * 12 * 10)
        assert result.final_balance == pytest.approx(expected_contributions, abs=0.01)
        assert result.total_interest == pytest.approx(0.0, abs=0.01)

    def test_zero_principal_with_contributions(self):
        """Starting from $0 with monthly contributions."""
        result = calculate_compound_interest(
            principal=0, annual_rate=7, years=10,
            contribution=500, contribution_frequency="monthly",
            compounding_frequency="monthly",
        )
        assert result.final_balance > 0
        assert result.total_contributions == 500 * 12 * 10
        assert result.total_interest > 0

    def test_one_year_period(self):
        result = calculate_compound_interest(
            principal=1000, annual_rate=12, years=1,
            compounding_frequency="monthly",
        )
        # 1000 * (1 + 0.01)^12 = 1126.83
        assert result.final_balance == pytest.approx(1126.83, abs=0.01)


class TestContributions:
    def test_monthly_contributions_monthly_compounding(self):
        result = calculate_compound_interest(
            principal=10000, annual_rate=7, years=20,
            contribution=500, contribution_frequency="monthly",
            compounding_frequency="monthly",
        )
        assert result.final_balance > 10000 + (500 * 12 * 20)
        assert result.total_contributions == 10000 + (500 * 12 * 20)

    def test_yearly_contributions_yearly_compounding(self):
        result = calculate_compound_interest(
            principal=10000, annual_rate=7, years=20,
            contribution=6000, contribution_frequency="yearly",
            compounding_frequency="yearly",
        )
        assert result.final_balance > 10000 + (6000 * 20)

    def test_no_contributions(self):
        result = calculate_compound_interest(
            principal=10000, annual_rate=5, years=10,
            contribution=0, compounding_frequency="yearly",
        )
        assert result.total_contributions == 10000.0


class TestCompoundingFrequencies:
    def test_higher_frequency_yields_more(self):
        """Daily compounding should yield more than yearly."""
        daily = calculate_compound_interest(
            principal=10000, annual_rate=10, years=10,
            compounding_frequency="daily",
        )
        yearly = calculate_compound_interest(
            principal=10000, annual_rate=10, years=10,
            compounding_frequency="yearly",
        )
        assert daily.final_balance > yearly.final_balance

    def test_quarterly_between_monthly_and_yearly(self):
        monthly = calculate_compound_interest(
            principal=10000, annual_rate=10, years=10,
            compounding_frequency="monthly",
        )
        quarterly = calculate_compound_interest(
            principal=10000, annual_rate=10, years=10,
            compounding_frequency="quarterly",
        )
        yearly = calculate_compound_interest(
            principal=10000, annual_rate=10, years=10,
            compounding_frequency="yearly",
        )
        assert yearly.final_balance < quarterly.final_balance < monthly.final_balance


class TestInflation:
    def test_inflation_adjusted_is_less(self):
        result = calculate_compound_interest(
            principal=10000, annual_rate=7, years=20,
            inflation_rate=3.0, compounding_frequency="yearly",
        )
        assert result.inflation_adjusted_balance is not None
        assert result.inflation_adjusted_balance < result.final_balance

    def test_no_inflation_returns_none(self):
        result = calculate_compound_interest(
            principal=10000, annual_rate=7, years=20,
            compounding_frequency="yearly",
        )
        assert result.inflation_adjusted_balance is None


class TestYearlyBreakdown:
    def test_breakdown_length_matches_years(self):
        result = calculate_compound_interest(
            principal=10000, annual_rate=5, years=15,
            compounding_frequency="yearly",
        )
        assert len(result.yearly_breakdown) == 15

    def test_breakdown_first_year_starts_with_principal(self):
        result = calculate_compound_interest(
            principal=5000, annual_rate=10, years=5,
            compounding_frequency="yearly",
        )
        assert result.yearly_breakdown[0].starting_balance == 5000.0

    def test_breakdown_last_year_ends_with_final_balance(self):
        result = calculate_compound_interest(
            principal=5000, annual_rate=10, years=5,
            compounding_frequency="yearly",
        )
        assert result.yearly_breakdown[-1].ending_balance == result.final_balance
