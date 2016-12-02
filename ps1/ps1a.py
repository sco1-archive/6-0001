# Problem Set 1A
# Name: sco1
# Collaborators: N/A 
# Time Spent: 0:30

# Initialize our constants
portion_down_payment = 0.25  # Portion of total cost needed for down payment
r = 0.04  # Annual return on investment

# Get user inputs
# Assume that the users follow directions, so we won't check the inputs
annual_salary = float(input('Enter your annual salary: '))
portion_saved = float(input('Enter the percent of your salary to save, as a decimal: '))
total_cost = float(input('Enter the cost of your dream home: '))

# Make preliminary calculations
down_payment = total_cost * portion_down_payment

monthly_salary = annual_salary / 12.0
saved_monthly = monthly_salary * portion_saved

# Rather than do creative investment math, use a loop
current_savings = 0.0
n_months = 0
while current_savings < down_payment:
    # Interest is calculated based on current savings, then the deposit is made
    interest_earned = current_savings * (r/12.0)
    current_savings += interest_earned # Add our interest
    current_savings += saved_monthly  # Make our deposit
    n_months += 1

print('Number of months: %i' % n_months)