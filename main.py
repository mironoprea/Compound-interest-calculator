#!/usr/bin/env python3
"""Compound Interest Calculator — CLI interface."""

from calculator import calculate_compound_interest


def get_float(prompt: str, minimum: float = 0.0) -> float:
    while True:
        try:
            value = float(input(prompt))
            if value < minimum:
                print(f"  Please enter a value of at least {minimum}.")
                continue
            return value
        except ValueError:
            print("  Invalid number. Please try again.")


def get_int(prompt: str, minimum: int = 1) -> int:
    while True:
        try:
            value = int(input(prompt))
            if value < minimum:
                print(f"  Please enter a value of at least {minimum}.")
                continue
            return value
        except ValueError:
            print("  Invalid number. Please try again.")


def choose_option(prompt: str, options: dict[str, str]) -> str:
    keys = list(options.keys())
    print(prompt)
    for i, key in enumerate(keys, 1):
        print(f"  {i}. {options[key]}")
    while True:
        try:
            choice = int(input("  Select (number): "))
            if 1 <= choice <= len(keys):
                return keys[choice - 1]
        except ValueError:
            pass
        print(f"  Please enter a number between 1 and {len(keys)}.")


def format_currency(amount: float) -> str:
    return f"${amount:,.2f}"


def print_breakdown(yearly_breakdown: list) -> None:
    header = f"{'Year':>5} | {'Start Balance':>15} | {'Contributions':>15} | {'Interest':>15} | {'End Balance':>15}"
    print("\n" + header)
    print("-" * len(header))
    for row in yearly_breakdown:
        print(
            f"{row.year:>5} | "
            f"{format_currency(row.starting_balance):>15} | "
            f"{format_currency(row.contributions):>15} | "
            f"{format_currency(row.interest_earned):>15} | "
            f"{format_currency(row.ending_balance):>15}"
        )


def main() -> None:
    print("=" * 50)
    print("   COMPOUND INTEREST CALCULATOR")
    print("=" * 50)

    principal = get_float("\nInitial deposit ($): ")
    annual_rate = get_float("Annual interest rate (%): ", minimum=0.0)
    years = get_int("Investment period (years): ", minimum=1)

    contribution = get_float("Periodic contribution ($, 0 for none): ")

    contribution_frequency = "monthly"
    if contribution > 0:
        contribution_frequency = choose_option(
            "Contribution frequency:",
            {"monthly": "Monthly", "yearly": "Yearly"},
        )

    compounding_frequency = choose_option(
        "Compounding frequency:",
        {
            "daily": "Daily (365x/year)",
            "monthly": "Monthly (12x/year)",
            "quarterly": "Quarterly (4x/year)",
            "yearly": "Yearly (1x/year)",
        },
    )

    inflation_input = input("\nAdjust for inflation? (y/N): ").strip().lower()
    inflation_rate = None
    if inflation_input == "y":
        inflation_rate = get_float("Annual inflation rate (%): ", minimum=0.0)

    result = calculate_compound_interest(
        principal=principal,
        annual_rate=annual_rate,
        years=years,
        contribution=contribution,
        contribution_frequency=contribution_frequency,
        compounding_frequency=compounding_frequency,
        inflation_rate=inflation_rate,
    )

    # Summary
    print("\n" + "=" * 50)
    print("   RESULTS")
    print("=" * 50)
    print(f"  Final Balance:        {format_currency(result.final_balance)}")
    print(f"  Total Contributions:  {format_currency(result.total_contributions)}")
    print(f"  Total Interest Earned:{format_currency(result.total_interest)}")
    if result.inflation_adjusted_balance is not None:
        print(f"  Inflation-Adjusted:   {format_currency(result.inflation_adjusted_balance)}")

    # Breakdown
    show_breakdown = input("\nShow year-by-year breakdown? (y/N): ").strip().lower()
    if show_breakdown == "y":
        print_breakdown(result.yearly_breakdown)

    print()


if __name__ == "__main__":
    main()
