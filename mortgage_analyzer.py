import argparse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from datetime import datetime

# --- Core Financial Constants ---.
INCOME_MULTIPLIER = 4.5 
MORTGAGE_TERM_YEARS = 30 

def calculate_affordability(income, deposit, monthly_debts, interest_rate_annual):
    """
    Calculates mortgage affordability based on UK guidelines.
    
    Returns a dictionary containing all key financial metrics.
    """
    
    max_loan_from_income = income * INCOME_MULTIPLIER

    
    affordable_property_price = max_loan_from_income + deposit

    loan_amount = max_loan_from_income
    monthly_interest_rate = (interest_rate_annual / 100) / 12
    number_of_payments = MORTGAGE_TERM_YEARS * 12

    if monthly_interest_rate > 0:
        monthly_payment = loan_amount * (monthly_interest_rate * (1 + monthly_interest_rate)**number_of_payments) / ((1 + monthly_interest_rate)**number_of_payments - 1)
    else:
        monthly_payment = loan_amount / number_of_payments

    total_monthly_outgoings = monthly_payment + monthly_debts
    gross_monthly_income = income / 12
    dti_ratio = (total_monthly_outgoings / gross_monthly_income) * 100

    results = {
        "income": income,
        "deposit": deposit,
        "monthly_debts": monthly_debts,
        "interest_rate": interest_rate_annual,
        "max_loan_amount": max_loan_from_income,
        "affordable_property_price": affordable_property_price,
        "estimated_monthly_payment": monthly_payment,
        "dti_ratio": dti_ratio
    }
    return results

def generate_pdf_report(data, scenarios=None):
    """
    Generates a professional PDF report from the calculation results.
    Optionally includes scenario testing results.
    """
    filename = f"Mortgage_Affordability_Report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    c = canvas.Canvas(filename, pagesize=letter)
    width, height = letter

    y_pos = height - 1*inch

    def check_page_break(y_pos, needed_space=1*inch):
        """Start a new page if there isn't enough space left."""
        if y_pos < needed_space:
            c.showPage()
            return height - 1*inch
        return y_pos

    # --- Header ---
    c.setFont("Helvetica-Bold", 18)
    c.drawCentredString(width / 2.0, y_pos, "Mortgage Affordability Report")
    y_pos -= 0.5*inch

    c.setFont("Helvetica", 10)
    c.drawString(1*inch, y_pos, f"Report Generated: {datetime.now().strftime('%d %B %Y, %H:%M')}")
    y_pos -= 0.7*inch

    # --- Input Summary ---
    c.setFont("Helvetica-Bold", 14)
    c.drawString(1*inch, y_pos, "Financial Summary")
    c.line(1*inch, y_pos - 0.05*inch, width - 1*inch, y_pos - 0.05*inch)
    y_pos -= 0.5*inch

    c.setFont("Helvetica", 12)
    c.drawString(1.2*inch, y_pos, f"Annual Gross Income: £{data['income']:,.2f}")
    y_pos -= 0.3*inch
    c.drawString(1.2*inch, y_pos, f"Deposit Amount: £{data['deposit']:,.2f}")
    y_pos -= 0.3*inch
    c.drawString(1.2*inch, y_pos, f"Existing Monthly Debts: £{data['monthly_debts']:,.2f}")
    y_pos -= 0.7*inch

    # --- Affordability Results ---
    y_pos = check_page_break(y_pos)
    c.setFont("Helvetica-Bold", 14)
    c.drawString(1*inch, y_pos, "Affordability Analysis")
    c.line(1*inch, y_pos - 0.05*inch, width - 1*inch, y_pos - 0.05*inch)
    y_pos -= 0.5*inch

    c.setFont("Helvetica", 12)
    c.drawString(1.2*inch, y_pos, f"Assumed Interest Rate: {data['interest_rate']:.2f}%")
    y_pos -= 0.4*inch
    c.drawString(1.2*inch, y_pos, f"Maximum Loan Amount: £{data['max_loan_amount']:,.2f}")
    y_pos -= 0.3*inch
    c.drawString(1.2*inch, y_pos, f"Total Affordable Property Value: £{data['affordable_property_price']:,.2f}")
    y_pos -= 0.3*inch
    c.drawString(1.2*inch, y_pos, f"Estimated Monthly Payment: £{data['estimated_monthly_payment']:,.2f}")
    y_pos -= 0.3*inch
    c.drawString(1.2*inch, y_pos, f"Debt-to-Income (DTI) Ratio: {data['dti_ratio']:.2f}%")
    y_pos -= 0.7*inch

    # --- Scenario Analysis ---
    if scenarios:
        y_pos = check_page_break(y_pos, needed_space=2*inch)
        c.setFont("Helvetica-Bold", 14)
        c.drawString(1*inch, y_pos, "Scenario Analysis")
        c.line(1*inch, y_pos - 0.05*inch, width - 1*inch, y_pos - 0.05*inch)
        y_pos -= 0.5*inch

        c.setFont("Helvetica", 12)
        for name, res in scenarios:
            y_pos = check_page_break(y_pos, needed_space=1*inch)
            c.drawString(1.2*inch, y_pos, f"Scenario: {name}")
            y_pos -= 0.3*inch
            c.drawString(1.5*inch, y_pos, f"Property Value: £{res['affordable_property_price']:,.0f}")
            y_pos -= 0.3*inch
            c.drawString(1.5*inch, y_pos, f"Monthly Payment: £{res['estimated_monthly_payment']:,.0f}")
            y_pos -= 0.5*inch

    # --- Footer Disclaimer (always at end, after page breaks) ---
    y_pos = check_page_break(y_pos, needed_space=1*inch)
    c.setFont("Helvetica-Oblique", 8)
    c.drawCentredString(width / 2.0, 0.75*inch, "Disclaimer: This is an estimate for informational purposes only.")

    c.save()
    print(f"\n✅ Successfully generated report: {filename}")



def run_scenario_testing(income, deposit, monthly_debts, base_rate):
    """
    Runs the affordability calculation under different scenarios.
    Returns a list of scenario results (for PDF and terminal).
    """
    scenarios = {
        "Base Case": {"rate": base_rate, "deposit": deposit},
        "High Interest Rate (+1.5%)": {"rate": base_rate + 1.5, "deposit": deposit},
        "Lower Deposit (-£10,000)": {"rate": base_rate, "deposit": deposit - 10000}
    }

    scenario_results = []

    print("\n--- Running Scenario Analysis ---")
    for name, params in scenarios.items():
        if params['deposit'] < 0:
            print(f"\nSkipping '{name}' scenario: Deposit cannot be negative.")
            continue

        results = calculate_affordability(income, params['deposit'], monthly_debts, params['rate'])
        scenario_results.append((name, results))

    return scenario_results

def main():
    """ Main entry point for the command-line tool. """
    parser = argparse.ArgumentParser(description="Mortgage Affordability Calculator & Report Generator")
    
    parser.add_argument("--income", type=float, required=True, help="Your total annual gross income.")
    parser.add_argument("--deposit", type=float, required=True, help="Your total available deposit.")
    parser.add_argument("--debts", type=float, required=True, help="Your total monthly debt payments (loans, credit cards).")
    parser.add_argument("--rate", type=float, default=5.0, help="The estimated annual mortgage interest rate (e.g., 5.0).")
    
    parser.add_argument("--scenario", action="store_true", help="Run scenario testing for different rates and deposits.")

    args = parser.parse_args()

    base_results = calculate_affordability(args.income, args.deposit, args.debts, args.rate)

    scenario_results = None
    if args.scenario:
        scenario_results = run_scenario_testing(args.income, args.deposit, args.debts, args.rate)

    generate_pdf_report(base_results, scenarios=scenario_results)


if __name__ == "__main__":
    main()