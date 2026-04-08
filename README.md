# Compound Interest Calculator

A Python compound interest calculator with both a CLI and a Tkinter GUI, supporting periodic contributions, multiple compounding frequencies, and optional inflation adjustment.

## Features

- **Compound interest formula**: `A = P(1 + r/n)^(nt) + PMT contributions per period`
- **Compounding frequencies**: Daily, Monthly, Quarterly, Yearly
- **Periodic contributions**: Monthly or Yearly deposits
- **Inflation adjustment**: See your future balance in today's dollars
- **Year-by-year breakdown**: Table showing growth each year
- **GUI with chart**: Visual growth chart via Matplotlib

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Run the CLI
python main.py

# Run the GUI
python gui.py

# Run tests
pytest test_calculator.py -v
```

## Project Structure

```
main.py             # CLI interface
gui.py              # Tkinter GUI with Matplotlib chart
calculator.py       # Core calculation engine
test_calculator.py  # Unit tests (15 tests)
requirements.txt    # Python dependencies
```

## Formula

```
A = P(1 + r/n)^(nt)
```

With periodic contributions added each compounding period:

```
Each period:  balance = balance * (1 + r/n) + contribution_per_period
```

Where:
- **P** = Principal (initial deposit)
- **r** = Annual interest rate (decimal)
- **n** = Compounding frequency (times per year)
- **t** = Time in years
- **PMT** = Periodic contribution amount

## License

MIT
