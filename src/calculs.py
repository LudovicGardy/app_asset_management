import numpy as np

def calculate_savings(P, E, n_years, r_annual, months_between_savings):
    periods_per_year = 12 / months_between_savings
    r_periodic = r_annual / periods_per_year
    capital_accumulated = [P]
    savings_accumulated = [P]
    interest_accumulated = [0]
    
    for year in range(1, n_years + 1):
        for period in range(int(periods_per_year)):
            interest = P * r_periodic
            P += interest + E
        capital_accumulated.append(P)
        savings_accumulated.append(savings_accumulated[-1] + E * periods_per_year)
        interest_accumulated.append(P - savings_accumulated[-1])
    
    return np.arange(0, n_years + 1), capital_accumulated, savings_accumulated, interest_accumulated, P

def calculate_mortgage(P, annual_interest_rate, years):
    n = years * 12
    r = annual_interest_rate / 12
    M = P * (r * (1 + r)**n) / ((1 + r)**n - 1)
    
    monthly_payment = np.array([M] * n)
    principal_paid = np.zeros(n)
    interest_paid = np.zeros(n)
    remaining_balance = np.zeros(n)
    total_interest = 0
    
    for month in range(n):
        interest = (P * r)
        principal = M - interest
        P -= principal
        
        interest_paid[month] = interest
        principal_paid[month] = principal
        remaining_balance[month] = P
        total_interest += interest
        
    return monthly_payment, principal_paid, interest_paid, remaining_balance, total_interest, M