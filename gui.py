#!/usr/bin/env python3
"""Compound Interest Calculator — Tkinter GUI."""

import tkinter as tk
from tkinter import ttk, messagebox

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from calculator import calculate_compound_interest


class CalculatorApp(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.title("Compound Interest Calculator")
        self.geometry("960x720")
        self.minsize(800, 600)

        self._build_input_frame()
        self._build_results_frame()

    # ── Input Panel ──────────────────────────────────────────────

    def _build_input_frame(self) -> None:
        frame = ttk.LabelFrame(self, text="Inputs", padding=12)
        frame.pack(fill="x", padx=12, pady=(12, 6))

        row = 0

        def add_field(label: str, default: str = "") -> ttk.Entry:
            nonlocal row
            ttk.Label(frame, text=label).grid(row=row, column=0, sticky="w", pady=4)
            entry = ttk.Entry(frame, width=20)
            entry.insert(0, default)
            entry.grid(row=row, column=1, sticky="w", padx=(8, 0), pady=4)
            row += 1
            return entry

        self.principal_entry = add_field("Initial Deposit ($):", "10000")
        self.rate_entry = add_field("Annual Interest Rate (%):", "7")
        self.years_entry = add_field("Investment Period (years):", "20")
        self.contribution_entry = add_field("Periodic Contribution ($):", "500")

        # Contribution frequency
        ttk.Label(frame, text="Contribution Frequency:").grid(row=row, column=0, sticky="w", pady=4)
        self.contrib_freq = ttk.Combobox(frame, values=["Monthly", "Yearly"], state="readonly", width=17)
        self.contrib_freq.set("Monthly")
        self.contrib_freq.grid(row=row, column=1, sticky="w", padx=(8, 0), pady=4)
        row += 1

        # Compounding frequency
        ttk.Label(frame, text="Compounding Frequency:").grid(row=row, column=0, sticky="w", pady=4)
        self.comp_freq = ttk.Combobox(
            frame, values=["Daily", "Monthly", "Quarterly", "Yearly"], state="readonly", width=17
        )
        self.comp_freq.set("Monthly")
        self.comp_freq.grid(row=row, column=1, sticky="w", padx=(8, 0), pady=4)
        row += 1

        # Inflation
        self.inflation_var = tk.BooleanVar()
        ttk.Checkbutton(frame, text="Adjust for inflation", variable=self.inflation_var).grid(
            row=row, column=0, sticky="w", pady=4
        )
        self.inflation_entry = ttk.Entry(frame, width=20)
        self.inflation_entry.insert(0, "3")
        self.inflation_entry.grid(row=row, column=1, sticky="w", padx=(8, 0), pady=4)
        ttk.Label(frame, text="% / year").grid(row=row, column=2, sticky="w", pady=4)
        row += 1

        # Calculate button
        ttk.Button(frame, text="Calculate", command=self._calculate).grid(
            row=row, column=0, columnspan=3, pady=(12, 0)
        )

    # ── Results Panel ────────────────────────────────────────────

    def _build_results_frame(self) -> None:
        self.results_frame = ttk.Frame(self)
        self.results_frame.pack(fill="both", expand=True, padx=12, pady=(6, 12))

        # Left: summary + table
        left = ttk.Frame(self.results_frame)
        left.pack(side="left", fill="both", expand=True)

        self.summary_label = ttk.Label(left, text="", justify="left", font=("Consolas", 11))
        self.summary_label.pack(anchor="nw", pady=(0, 8))

        cols = ("Year", "Start", "Contributions", "Interest", "End Balance")
        self.tree = ttk.Treeview(left, columns=cols, show="headings", height=12)
        for col in cols:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=110, anchor="e")
        self.tree.column("Year", width=50, anchor="center")
        scrollbar = ttk.Scrollbar(left, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="left", fill="y")

        # Right: chart
        self.chart_frame = ttk.Frame(self.results_frame)
        self.chart_frame.pack(side="right", fill="both", expand=True, padx=(12, 0))

    # ── Calculation Logic ────────────────────────────────────────

    def _calculate(self) -> None:
        try:
            principal = float(self.principal_entry.get())
            rate = float(self.rate_entry.get())
            years = int(self.years_entry.get())
            contribution = float(self.contribution_entry.get())
        except ValueError:
            messagebox.showerror("Input Error", "Please enter valid numbers for all fields.")
            return

        if principal < 0 or rate < 0 or years < 1 or contribution < 0:
            messagebox.showerror("Input Error", "Values must be non-negative (years >= 1).")
            return

        contrib_freq = self.contrib_freq.get().lower()
        comp_freq = self.comp_freq.get().lower()

        inflation_rate = None
        if self.inflation_var.get():
            try:
                inflation_rate = float(self.inflation_entry.get())
            except ValueError:
                messagebox.showerror("Input Error", "Please enter a valid inflation rate.")
                return

        result = calculate_compound_interest(
            principal=principal,
            annual_rate=rate,
            years=years,
            contribution=contribution,
            contribution_frequency=contrib_freq,
            compounding_frequency=comp_freq,
            inflation_rate=inflation_rate,
        )

        self._display_results(result)

    def _display_results(self, result) -> None:
        # Summary
        fmt = lambda v: f"${v:,.2f}"
        text = (
            f"Final Balance:         {fmt(result.final_balance)}\n"
            f"Total Contributions:   {fmt(result.total_contributions)}\n"
            f"Total Interest Earned: {fmt(result.total_interest)}"
        )
        if result.inflation_adjusted_balance is not None:
            text += f"\nInflation-Adjusted:    {fmt(result.inflation_adjusted_balance)}"
        self.summary_label.config(text=text)

        # Table
        self.tree.delete(*self.tree.get_children())
        for row in result.yearly_breakdown:
            self.tree.insert(
                "", "end",
                values=(
                    row.year,
                    fmt(row.starting_balance),
                    fmt(row.contributions),
                    fmt(row.interest_earned),
                    fmt(row.ending_balance),
                ),
            )

        # Chart
        for widget in self.chart_frame.winfo_children():
            widget.destroy()

        years = [r.year for r in result.yearly_breakdown]
        balances = [r.ending_balance for r in result.yearly_breakdown]
        contributions_cum = []
        cum = result.yearly_breakdown[0].starting_balance  # principal
        for r in result.yearly_breakdown:
            cum += r.contributions
            contributions_cum.append(cum)

        fig = Figure(figsize=(4.5, 3.5), dpi=100)
        ax = fig.add_subplot(111)
        ax.fill_between(years, balances, alpha=0.3, label="Total Balance", color="#2196F3")
        ax.fill_between(years, contributions_cum, alpha=0.3, label="Total Contributions", color="#4CAF50")
        ax.plot(years, balances, color="#1565C0", linewidth=2)
        ax.plot(years, contributions_cum, color="#2E7D32", linewidth=2)
        ax.set_xlabel("Year")
        ax.set_ylabel("Amount ($)")
        ax.set_title("Growth Over Time")
        ax.legend(loc="upper left", fontsize=8)
        ax.ticklabel_format(style="plain", axis="y")
        fig.tight_layout()

        canvas = FigureCanvasTkAgg(fig, master=self.chart_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)


if __name__ == "__main__":
    app = CalculatorApp()
    app.mainloop()
