# Mortgage Affordability Analyzer

This project is a command-line tool that models mortgage affordability in a professional way. It calculates how much someone can borrow based on their income, deposit, and debts, generates a clean PDF report, and even runs scenario testing to see how affordability changes if market conditions shift. I built this as part of my portfolio to show how financial logic, automation, and professional reporting can all come together in Python.

## Features
- Calculates maximum mortgage amount using the **UK 4.5× income multiplier**.
- Runs a **Debt-to-Income (DTI) check** to validate affordability realistically.
- Generates a **professional PDF report** summarizing inputs and results.
- Scenario analysis that models:
  - Higher interest rates (+1.5%),
  - Lower deposits (–£10,000),
  - And other what-if conditions.
- Console outputs for quick review alongside shareable reports.

## Tech Stack
- **Python** (argparse, datetime)
- **ReportLab** for dynamic PDF generation
- **Standard amortization formula** for mortgage calculations
- **Command-line interface (CLI)** for clean, reusable usage

## Example Output

**Base Case (Income: £100k, Deposit: £60k, Debts: £500, Rate: 5%)**
- Max Loan: £450,000  
- Affordable Property Value: £510,000  
- Monthly Payment: £2,415.70  
- DTI Ratio: 34.99%

**Scenario Testing**
- High Interest Rate (+1.5%): £2,844 / month  
- Lower Deposit (–£10,000): £500,000 property value  

---

## How It Works
1. User provides income, deposit, debts, and interest rate as command-line arguments.  
2. Script calculates affordability using the income multiplier + DTI check.  
3. Results are saved into a professionally formatted PDF.  
4. If the `--scenario` flag is added, alternative affordability cases are also modeled and included in the PDF.  

---

## Why I Built This
Mortgage affordability is never a simple “income × 4.5” calculation. In reality, analysts run stress tests, compare different conditions, and generate reports that can be handed over to clients.  

This project let me combine:
- My **finance knowledge** (income multipliers, DTI, loan amortization),  
- My **Python development skills** (CLI, formulas, automation),  
- And my ability to create **professional deliverables** (PDF reports with scenario modeling).  

It reflects the way real-world financial tools are expected to work: accurate, automated, and presentation-ready.

---

## Next Steps
- Add **more scenarios** (e.g., different mortgage terms, variable income multipliers).  
- Expand the PDF layout with **charts/graphs** for visual clarity.  
- Turn this into a **web app or Streamlit dashboard** for non-technical users.  

---
