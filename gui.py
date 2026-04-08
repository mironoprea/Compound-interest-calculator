#!/usr/bin/env python3
"""Compound Interest Calculator — Modern Dark GUI."""

import tkinter as tk
from tkinter import ttk, messagebox
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.ticker import FuncFormatter

from calculator import calculate_compound_interest


# ── Color Palette ─────────────────────────────────────────────────────────────
class C:
    BG         = "#0d1117"
    SURFACE    = "#161b22"
    CARD       = "#21262d"
    BORDER     = "#30363d"
    PRIMARY    = "#7c73e5"
    PRIMARY_DK = "#5a61d1"
    SUCCESS    = "#3fb950"
    CYAN       = "#58a6ff"
    WARNING    = "#e3b341"
    TEXT       = "#e6edf3"
    MUTED      = "#8b949e"
    INPUT_BG   = "#0d1117"


class CalculatorApp(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.title("Compound Interest Calculator")
        self.geometry("1160x760")
        self.minsize(960, 640)
        self.configure(bg=C.BG)

        self._setup_styles()
        self._build_header()

        content = tk.Frame(self, bg=C.BG)
        content.pack(fill="both", expand=True, padx=16, pady=(10, 16))

        left = tk.Frame(content, bg=C.BG, width=316)
        left.pack(side="left", fill="y", padx=(0, 12))
        left.pack_propagate(False)

        right = tk.Frame(content, bg=C.BG)
        right.pack(side="left", fill="both", expand=True)

        self._build_input_panel(left)
        self._build_results_panel(right)

    # ── Styling ───────────────────────────────────────────────────────────────

    def _setup_styles(self) -> None:
        style = ttk.Style(self)
        style.theme_use("clam")

        style.configure(".", background=C.BG, foreground=C.TEXT)

        # Treeview
        style.configure("Treeview",
                        background=C.SURFACE, foreground=C.TEXT,
                        fieldbackground=C.SURFACE, borderwidth=0, rowheight=26)
        style.configure("Treeview.Heading",
                        background=C.CARD, foreground=C.MUTED,
                        font=("Segoe UI", 9, "bold"), relief="flat")
        style.map("Treeview",
                  background=[("selected", C.PRIMARY_DK)],
                  foreground=[("selected", C.TEXT)])

        # Combobox
        style.configure("TCombobox",
                        fieldbackground=C.INPUT_BG, foreground=C.TEXT,
                        selectbackground=C.INPUT_BG, selectforeground=C.TEXT,
                        arrowcolor=C.MUTED, bordercolor=C.BORDER,
                        insertcolor=C.TEXT, padding=(8, 6))
        self.option_add("*TCombobox*Listbox.background",       C.CARD)
        self.option_add("*TCombobox*Listbox.foreground",       C.TEXT)
        self.option_add("*TCombobox*Listbox.selectBackground", C.PRIMARY_DK)
        self.option_add("*TCombobox*Listbox.selectForeground", C.TEXT)

        # Scrollbar
        style.configure("TScrollbar",
                        background=C.SURFACE, troughcolor=C.BG,
                        arrowcolor=C.MUTED, bordercolor=C.BG)

    # ── Header ────────────────────────────────────────────────────────────────

    def _build_header(self) -> None:
        hdr = tk.Frame(self, bg=C.SURFACE, height=58)
        hdr.pack(fill="x")
        hdr.pack_propagate(False)

        inner = tk.Frame(hdr, bg=C.SURFACE)
        inner.place(relx=0, rely=0.5, anchor="w", x=20)

        tk.Label(inner, text="\u2197",
                 font=("Segoe UI", 20, "bold"),
                 bg=C.SURFACE, fg=C.PRIMARY).pack(side="left", padx=(0, 10))

        tk.Label(inner, text="Compound Interest Calculator",
                 font=("Segoe UI", 13, "bold"),
                 bg=C.SURFACE, fg=C.TEXT).pack(side="left")

        tk.Label(inner, text="  —  Investment Growth Projector",
                 font=("Segoe UI", 10),
                 bg=C.SURFACE, fg=C.MUTED).pack(side="left")

        tk.Frame(self, bg=C.BORDER, height=1).pack(fill="x")

    # ── Input Panel ───────────────────────────────────────────────────────────

    def _build_input_panel(self, parent: tk.Frame) -> None:
        card = tk.Frame(parent, bg=C.CARD, padx=18, pady=16)
        card.pack(fill="x")

        tk.Label(card, text="INVESTMENT DETAILS",
                 font=("Segoe UI", 8, "bold"),
                 bg=C.CARD, fg=C.MUTED).pack(anchor="w", pady=(0, 14))

        self.principal_var      = tk.StringVar(value="10000")
        self.rate_var           = tk.StringVar(value="7")
        self.years_var          = tk.StringVar(value="20")
        self.contribution_var   = tk.StringVar(value="500")
        self.contrib_freq_var   = tk.StringVar(value="Monthly")
        self.comp_freq_var      = tk.StringVar(value="Monthly")
        self.inflation_enabled  = tk.BooleanVar(value=False)
        self.inflation_rate_var = tk.StringVar(value="3")

        self._add_field(card, "Initial Deposit",       self.principal_var,    prefix="$")
        self._add_field(card, "Annual Interest Rate",  self.rate_var,         suffix="%")
        self._add_field(card, "Investment Period",     self.years_var,        suffix="years")
        self._add_field(card, "Periodic Contribution", self.contribution_var, prefix="$")

        self._add_combobox(card, "Contribution Frequency",
                           ["Monthly", "Yearly"], self.contrib_freq_var)
        self._add_combobox(card, "Compounding Frequency",
                           ["Daily", "Monthly", "Quarterly", "Yearly"], self.comp_freq_var)

        self._build_inflation_section(card)

        tk.Frame(card, bg=C.BORDER, height=1).pack(fill="x", pady=(14, 12))

        calc_btn = tk.Button(card, text="  Calculate  \u2192",
                             font=("Segoe UI", 10, "bold"),
                             bg=C.PRIMARY, fg="white",
                             activebackground=C.PRIMARY_DK, activeforeground="white",
                             relief="flat", bd=0, pady=10, cursor="hand2",
                             command=self._calculate)
        calc_btn.pack(fill="x")

        reset_btn = tk.Button(card, text="Reset to defaults",
                              font=("Segoe UI", 9),
                              bg=C.CARD, fg=C.MUTED,
                              activebackground=C.SURFACE, activeforeground=C.TEXT,
                              relief="flat", bd=0, pady=7, cursor="hand2",
                              command=self._reset)
        reset_btn.pack(fill="x", pady=(6, 0))

    def _add_field(self, parent: tk.Frame, label: str, var: tk.StringVar,
                   prefix: str = "", suffix: str = "") -> None:
        wrapper = tk.Frame(parent, bg=C.CARD)
        wrapper.pack(fill="x", pady=(0, 10))

        tk.Label(wrapper, text=label, font=("Segoe UI", 9, "bold"),
                 bg=C.CARD, fg=C.TEXT).pack(anchor="w")

        inp_bg = tk.Frame(wrapper, bg=C.INPUT_BG)
        inp_bg.pack(fill="x", pady=(3, 0))

        if prefix:
            tk.Label(inp_bg, text=prefix, font=("Segoe UI", 10),
                     bg=C.INPUT_BG, fg=C.MUTED, padx=8).pack(side="left")

        entry = tk.Entry(inp_bg, textvariable=var,
                         font=("Segoe UI", 11),
                         bg=C.INPUT_BG, fg=C.TEXT,
                         insertbackground=C.TEXT,
                         relief="flat", bd=0)
        entry.pack(side="left", fill="x", expand=True,
                   pady=8, padx=(0 if prefix else 10, 0))

        if suffix:
            tk.Label(inp_bg, text=suffix, font=("Segoe UI", 9),
                     bg=C.INPUT_BG, fg=C.MUTED, padx=8).pack(side="right")

        bar = tk.Frame(wrapper, bg=C.BORDER, height=1)
        bar.pack(fill="x")

        entry.bind("<FocusIn>",  lambda e: bar.config(bg=C.PRIMARY))
        entry.bind("<FocusOut>", lambda e: bar.config(bg=C.BORDER))

    def _add_combobox(self, parent: tk.Frame, label: str,
                      options: list, var: tk.StringVar) -> None:
        wrapper = tk.Frame(parent, bg=C.CARD)
        wrapper.pack(fill="x", pady=(0, 10))

        tk.Label(wrapper, text=label, font=("Segoe UI", 9, "bold"),
                 bg=C.CARD, fg=C.TEXT).pack(anchor="w")

        ttk.Combobox(wrapper, values=options, textvariable=var,
                     state="readonly", font=("Segoe UI", 10)).pack(fill="x", pady=(3, 0))

    def _build_inflation_section(self, parent: tk.Frame) -> None:
        # Always-visible section container
        section = tk.Frame(parent, bg=C.CARD)
        section.pack(fill="x", pady=(0, 4))

        hdr = tk.Frame(section, bg=C.CARD)
        hdr.pack(fill="x")

        tk.Label(hdr, text="Inflation Adjustment",
                 font=("Segoe UI", 9, "bold"),
                 bg=C.CARD, fg=C.TEXT).pack(side="left")

        self._infl_btn = tk.Label(hdr, text=" OFF ",
                                  font=("Segoe UI", 8, "bold"),
                                  bg=C.BORDER, fg=C.MUTED,
                                  padx=8, pady=2, cursor="hand2")
        self._infl_btn.pack(side="right")
        self._infl_btn.bind("<Button-1>", self._toggle_inflation)

        # Rate input lives inside section; hidden initially
        self._infl_row = tk.Frame(section, bg=C.CARD)
        self._add_field(self._infl_row, "Annual Inflation Rate",
                        self.inflation_rate_var, suffix="%/yr")

    def _toggle_inflation(self, _event=None) -> None:
        if self.inflation_enabled.get():
            self.inflation_enabled.set(False)
            self._infl_btn.config(text=" OFF ", bg=C.BORDER, fg=C.MUTED)
            self._infl_row.pack_forget()
        else:
            self.inflation_enabled.set(True)
            self._infl_btn.config(text=" ON  ", bg=C.SUCCESS, fg="white")
            self._infl_row.pack(fill="x", pady=(6, 0))

    def _reset(self) -> None:
        self.principal_var.set("10000")
        self.rate_var.set("7")
        self.years_var.set("20")
        self.contribution_var.set("500")
        self.contrib_freq_var.set("Monthly")
        self.comp_freq_var.set("Monthly")
        self.inflation_enabled.set(False)
        self.inflation_rate_var.set("3")
        self._infl_btn.config(text=" OFF ", bg=C.BORDER, fg=C.MUTED)
        self._infl_row.pack_forget()

        for key, lbl in self._stat_vals.items():
            lbl.config(text="—" if key == "inflation" else "$0")
        self.tree.delete(*self.tree.get_children())
        self._draw_placeholder_chart()

    # ── Results Panel ─────────────────────────────────────────────────────────

    def _build_results_panel(self, parent: tk.Frame) -> None:
        # Stat cards row
        cards_row = tk.Frame(parent, bg=C.BG)
        cards_row.pack(fill="x", pady=(0, 10))

        card_defs = [
            ("final",    "Final Balance",       "$0", C.PRIMARY),
            ("contrib",  "Total Contributions", "$0", C.SUCCESS),
            ("interest", "Interest Earned",     "$0", C.CYAN),
            ("inflation","Inflation Adjusted",  "—",  C.WARNING),
        ]
        self._stat_vals: dict[str, tk.Label] = {}
        for i, (key, title, value, color) in enumerate(card_defs):
            padx = (0, 8) if i < 3 else (0, 0)
            self._stat_vals[key] = self._make_stat_card(
                cards_row, title, value, color, padx)

        # Lower area: chart + table
        lower = tk.Frame(parent, bg=C.BG)
        lower.pack(fill="both", expand=True)

        chart_card = tk.Frame(lower, bg=C.CARD, padx=14, pady=14)
        chart_card.pack(side="left", fill="both", expand=True, padx=(0, 8))

        tk.Label(chart_card, text="GROWTH OVER TIME",
                 font=("Segoe UI", 8, "bold"),
                 bg=C.CARD, fg=C.MUTED).pack(anchor="w", pady=(0, 6))

        self.chart_host = tk.Frame(chart_card, bg=C.CARD)
        self.chart_host.pack(fill="both", expand=True)
        self._draw_placeholder_chart()

        tbl_card = tk.Frame(lower, bg=C.CARD, padx=14, pady=14, width=340)
        tbl_card.pack(side="right", fill="both")
        tbl_card.pack_propagate(False)

        tk.Label(tbl_card, text="YEARLY BREAKDOWN",
                 font=("Segoe UI", 8, "bold"),
                 bg=C.CARD, fg=C.MUTED).pack(anchor="w", pady=(0, 6))

        self._build_table(tbl_card)

    def _make_stat_card(self, parent: tk.Frame, title: str, value: str,
                        color: str, padx) -> tk.Label:
        card = tk.Frame(parent, bg=C.CARD)
        card.pack(side="left", fill="x", expand=True, padx=padx)

        tk.Frame(card, bg=color, height=3).pack(fill="x")

        inner = tk.Frame(card, bg=C.CARD, padx=14, pady=12)
        inner.pack(fill="both", expand=True)

        val_lbl = tk.Label(inner, text=value,
                           font=("Segoe UI", 17, "bold"),
                           bg=C.CARD, fg=C.TEXT)
        val_lbl.pack(anchor="w")

        tk.Label(inner, text=title, font=("Segoe UI", 9),
                 bg=C.CARD, fg=C.MUTED).pack(anchor="w")

        return val_lbl

    def _build_table(self, parent: tk.Frame) -> None:
        frame = tk.Frame(parent, bg=C.CARD)
        frame.pack(fill="both", expand=True)

        cols = ("Year", "End Balance", "Interest")
        self.tree = ttk.Treeview(frame, columns=cols, show="headings", height=18)

        for col, width, anchor in [("Year", 50, "center"),
                                    ("End Balance", 140, "e"),
                                    ("Interest", 120, "e")]:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=width, anchor=anchor, stretch=False)

        sb = ttk.Scrollbar(frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=sb.set)
        self.tree.pack(side="left", fill="both", expand=True)
        sb.pack(side="right", fill="y")

        self.tree.tag_configure("odd",  background=C.CARD)
        self.tree.tag_configure("even", background=C.SURFACE)

    def _draw_placeholder_chart(self) -> None:
        for w in self.chart_host.winfo_children():
            w.destroy()

        fig = Figure(figsize=(5, 4), dpi=96, facecolor=C.CARD)
        ax  = fig.add_subplot(111, facecolor=C.SURFACE)
        ax.set_xlabel("Year",   color=C.MUTED, fontsize=9)
        ax.set_ylabel("Amount", color=C.MUTED, fontsize=9)
        ax.tick_params(colors=C.MUTED, labelsize=8)
        for sp in ax.spines.values():
            sp.set_color(C.BORDER)
        ax.text(0.5, 0.5, "Enter values and click  Calculate",
                ha="center", va="center", color=C.MUTED, fontsize=10,
                transform=ax.transAxes)
        fig.tight_layout(pad=1.5)

        cv = FigureCanvasTkAgg(fig, master=self.chart_host)
        cv.draw()
        cv.get_tk_widget().pack(fill="both", expand=True)

    # ── Calculation ───────────────────────────────────────────────────────────

    def _calculate(self) -> None:
        try:
            principal    = float(self.principal_var.get())
            rate         = float(self.rate_var.get())
            years        = int(self.years_var.get())
            contribution = float(self.contribution_var.get())
        except ValueError:
            messagebox.showerror("Input Error", "Please enter valid numbers for all fields.")
            return

        if principal < 0 or rate < 0 or years < 1 or contribution < 0:
            messagebox.showerror("Input Error", "Values must be non-negative (years \u2265 1).")
            return

        inflation_rate = None
        if self.inflation_enabled.get():
            try:
                inflation_rate = float(self.inflation_rate_var.get())
            except ValueError:
                messagebox.showerror("Input Error", "Please enter a valid inflation rate.")
                return

        result = calculate_compound_interest(
            principal=principal,
            annual_rate=rate,
            years=years,
            contribution=contribution,
            contribution_frequency=self.contrib_freq_var.get().lower(),
            compounding_frequency=self.comp_freq_var.get().lower(),
            inflation_rate=inflation_rate,
        )
        self._display_results(result)

    def _display_results(self, result) -> None:
        fmt  = lambda v: f"${v:,.0f}"
        fmt2 = lambda v: f"${v:,.2f}"

        self._stat_vals["final"].config(text=fmt(result.final_balance))
        self._stat_vals["contrib"].config(text=fmt(result.total_contributions))
        self._stat_vals["interest"].config(text=fmt(result.total_interest))
        self._stat_vals["inflation"].config(
            text=fmt(result.inflation_adjusted_balance)
            if result.inflation_adjusted_balance is not None else "\u2014"
        )

        # Table
        self.tree.delete(*self.tree.get_children())
        for i, row in enumerate(result.yearly_breakdown):
            self.tree.insert("", "end",
                             tags=("even" if i % 2 == 0 else "odd",),
                             values=(row.year,
                                     fmt2(row.ending_balance),
                                     fmt2(row.interest_earned)))

        # Chart
        for w in self.chart_host.winfo_children():
            w.destroy()

        yrs  = [r.year for r in result.yearly_breakdown]
        bals = [r.ending_balance for r in result.yearly_breakdown]

        cum = result.yearly_breakdown[0].starting_balance
        cum_contribs: list[float] = []
        for r in result.yearly_breakdown:
            cum += r.contributions
            cum_contribs.append(cum)

        interest_layer = [b - c for b, c in zip(bals, cum_contribs)]

        fig = Figure(figsize=(5, 4), dpi=96, facecolor=C.CARD)
        ax  = fig.add_subplot(111, facecolor=C.SURFACE)

        ax.stackplot(yrs, cum_contribs, interest_layer,
                     labels=["Contributions", "Interest Earned"],
                     colors=[C.SUCCESS + "88", C.PRIMARY + "88"])

        ax.plot(yrs, bals, color=C.CYAN, linewidth=2, zorder=5, label="Total Balance")

        def money_fmt(x: float, _pos) -> str:
            if abs(x) >= 1_000_000:
                return f"${x / 1_000_000:.1f}M"
            if abs(x) >= 1_000:
                return f"${x / 1_000:.0f}K"
            return f"${x:.0f}"

        ax.yaxis.set_major_formatter(FuncFormatter(money_fmt))
        ax.set_xlabel("Year", color=C.MUTED, fontsize=9)
        ax.tick_params(colors=C.MUTED, labelsize=8)
        ax.grid(axis="y", color=C.BORDER, linewidth=0.5, alpha=0.7)
        for sp in ax.spines.values():
            sp.set_color(C.BORDER)

        legend = ax.legend(loc="upper left", fontsize=8,
                           facecolor=C.CARD, edgecolor=C.BORDER)
        for text in legend.get_texts():
            text.set_color(C.TEXT)

        fig.tight_layout(pad=1.5)

        cv = FigureCanvasTkAgg(fig, master=self.chart_host)
        cv.draw()
        cv.get_tk_widget().pack(fill="both", expand=True)


if __name__ == "__main__":
    app = CalculatorApp()
    app.mainloop()
