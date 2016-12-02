# Problem Set 1C
# Name: sco1
# Collaborators: N/A 
# Time Spent: 0:45

# Initialize our constants
portion_down_payment = 0.25  # Portion of total cost needed for down payment
r = 0.04  # Annual return on investment
semi_annual_raise = 0.07  # Amount our salary increases every 6 months
total_cost = 1000000  # Total cost of our house
month_target = 36  # The month where we want to hit our goal

# Get user inputs
# Assume that the users follow directions, so we won't check the inputs
annual_salary_start = float(input('Enter the starting salary: '))

# Make preliminary calculations
down_payment = total_cost * portion_down_payment

# Define our portion bounds
# For desired precision, range between 0 and 10000 and convert the integer to decimal float
portion_lower = 0
portion_upper = 10000
portion_max = 10000

n_iterations = 0  # Start our counter
goal_met = False
while not goal_met:
    n_iterations += 1
    annual_salary = annual_salary_start
    monthly_salary = annual_salary / 12.0

    portion_saved_int = (portion_upper + portion_lower)/2
    portion_saved = portion_saved_int/10000.00
    saved_monthly = monthly_salary * portion_saved

    # Rather than do creative investment math, use a loop
    current_savings = 0.0
    n_months = 0
    while abs(down_payment - current_savings) > 100.00:        
        # Interest is calculated based on current savings, then the deposit is made
        interest_earned = current_savings * (r/12.0)
        current_savings += interest_earned # Add our interest
        current_savings += saved_monthly  # Make our deposit
        n_months += 1
        
        if n_months == month_target:
            break

        if n_months % 6 == 0:  # Salary bump every 6 months, at the end of the month (after deposit)
            annual_salary *= (1 + semi_annual_raise)
            monthly_salary = annual_salary / 12.0
            saved_monthly = monthly_salary * portion_saved

    if abs(down_payment - current_savings) < 100.00:
        print('Best savings rate: %.4f' % portion_saved)
        print('Steps in bisection search: %i' % n_iterations)
        goal_met = True

    elif down_payment - current_savings > 100.00:
        if portion_saved_int == portion_max:
            print('It is not possible to pay the down payment in three years')
            break
        portion_lower = portion_saved_int
    elif down_payment - current_savings < -100.00:
        portion_upper = portion_saved_int