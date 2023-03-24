import math
from fredapi import Fred

def calculate_monthly_interest_rate(annual_interest_rate):
    return annual_interest_rate / (12 * 100)

def calculate_monthly_payment(principal, monthly_interest_rate, loan_term):
    num_payments = loan_term * 12
    if monthly_interest_rate == 0:
        return principal / num_payments
    else:
        return principal * monthly_interest_rate * math.pow(1 + monthly_interest_rate, num_payments) / (math.pow(1 + monthly_interest_rate, num_payments) - 1)

def debt_to_income_ratio(monthly_income, monthly_debt):
    return (monthly_debt / monthly_income) * 100

def max_monthly_payment(monthly_income, target_dti_ratio, current_monthly_debt):
    return (monthly_income * target_dti_ratio / 100) - current_monthly_debt

def house_affordability(monthly_income, monthly_debt, credit_score, interest_rate, loan_term, homeowners_insurance, down_payment, cash_on_hand, target_dti_ratio=43):
    max_payment = max_monthly_payment(monthly_income, target_dti_ratio, monthly_debt)
    monthly_insurance = homeowners_insurance / 12
    max_principal_and_interest = max_payment - monthly_insurance
    monthly_interest_rate = calculate_monthly_interest_rate(interest_rate)
    principal = max_principal_and_interest / (monthly_interest_rate * math.pow(1 + monthly_interest_rate, loan_term * 12) / (math.pow(1 + monthly_interest_rate, loan_term * 12) - 1))

    total_house_price = principal + min(down_payment, cash_on_hand)
    return total_house_price

def get_input_values(prompt):
    values = []
    while True:
        value = input(prompt)
        if value.lower() == 'done':
            break
        values.append(float(value))
    return sum(values)

def get_interest_rate(api_key, loan_term, loan_type):
    fred = Fred(api_key=api_key)
    if loan_term == 30 and loan_type == 'fixed':
        series_id = 'MORTGAGE30US'
    elif loan_term == 15 and loan_type == 'fixed':
        series_id = 'MORTGAGE15US'
    else:
        print("Unsupported loan term and type combination. Using 30-year fixed rate as a reference.")
        series_id = 'MORTGAGE30US'

    rate = fred.get_series_latest_release(series_id)
    return rate[0]

if __name__ == "__main__":
    api_key = ""

    print("\nEnter your incomes line by line. When you're done, type 'done':")
    annual_income = get_input_values("Income: ")

    print("\nEnter your rental incomes line by line. When you're done, type 'done':")
    rental_income = get_input_values("Rental Income: ") * 0.7

    annual_income += rental_income

    print("\nEnter your monthly debt payments line by line. When you're done, type 'done':")
    monthly_debt = get_input_values("Debt: ")

    credit_score = int(input("\nEnter your credit score: "))
    down_payment = float(input("Enter your down payment amount: "))
    cash_on_hand = float(input("Enter your cash on hand amount: "))
    loan_term = int(input("Enter the loan term in years (e.g., 15, 30): "))
    loan_type = input("Enter the loan type (e.g., 'fixed'): ").lower()

    print("Fetching today's interest rate from FRED...")
    interest_rate = get_interest_rate(api_key, loan_term, loan_type)
    print(f"Today's {loan_term}-year {loan_type} mortgage interest rate is: {interest_rate:.2f}%")

    homeowners_insurance = float(input("Enter the annual homeowners insurance amount: "))

    monthly_income = annual_income / 12

    dti = debt_to_income_ratio(monthly_income, monthly_debt)
    print(f"\nYour debt-to-income ratio is: {dti:.2f}%")

    max_house_price = house_affordability(monthly_income, monthly_debt, credit_score, interest_rate, loan_term, homeowners_insurance, down_payment, cash_on_hand)
    formatted_max_house_price = f"{max_house_price:,.2f}"
    print(f"Based on your input, you can afford a house up to ${formatted_max_house_price}")

