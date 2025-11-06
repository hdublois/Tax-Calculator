"""
Jupyter Notebook-style script to calculate SGO credit cost.
This can be run cell-by-cell or as a script.
"""

from taxcalc import *
import pandas as pd
import numpy as np

# Define the baseline (current law without SGO credit - already set to 0 in policy_current_law.json)
baseline = {
    # Baseline has CR_SGO_c = 0 by default in policy_current_law.json
}

# Define the reform (SGO credit enabled)
# Format: [single, mjoint, mseparate, headhh, widow]
sgo_reform = {
    "CR_SGO_c": {
        "2025": [1700.0, 3400.0, 1700.0, 1700.0, 1700.0],
        "2026": [1700.0, 3400.0, 1700.0, 1700.0, 1700.0],
        "2027": [1700.0, 3400.0, 1700.0, 1700.0, 1700.0],
        "2028": [1700.0, 3400.0, 1700.0, 1700.0, 1700.0],
        "2029": [1700.0, 3400.0, 1700.0, 1700.0, 1700.0],
        "2030": [1700.0, 3400.0, 1700.0, 1700.0, 1700.0],
        "2031": [1700.0, 3400.0, 1700.0, 1700.0, 1700.0],
        "2032": [1700.0, 3400.0, 1700.0, 1700.0, 1700.0],
        "2033": [1700.0, 3400.0, 1700.0, 1700.0, 1700.0],
        "2034": [1700.0, 3400.0, 1700.0, 1700.0, 1700.0]
    }
}

def run_calc(yr_range, refs_policy, refs_base, rec, df):
    """
    Calculate revenue differences for given year range.
    
    Parameters
    ----------
    yr_range : range
        Years to calculate
    refs_policy : list
        List of reform dictionaries
    refs_base : list
        List of baseline dictionaries
    rec : Records
        Records object
    df : DataFrame
        DataFrame to store results
    
    Returns
    -------
    DataFrame
        Results dataframe
    """
    for year in yr_range:
        col = []
        for (ref_policy, ref_base) in zip(refs_policy, refs_base):
            # Baseline
            pol_base = Policy()
            if ref_base:
                pol_base.implement_reform(ref_base)
            calc_base = Calculator(pol_base, rec)
            calc_base.advance_to_year(year)
            calc_base.calc_all()
            
            # Reform
            pol_ref = Policy()
            if ref_base:
                pol_ref.implement_reform(ref_base)
            pol_ref.implement_reform(ref_policy)
            calc_ref = Calculator(pol_ref, rec)
            calc_ref.advance_to_year(year)
            calc_ref.calc_all()
            
            # Calculate revenue difference
            base_df = calc_base.dataframe(['iitax', 's006'])
            ref_df = calc_ref.dataframe(['iitax', 's006'])
            
            base_rev = (base_df['iitax'] * base_df['s006']).sum() / 1e9  # billions
            ref_rev = (ref_df['iitax'] * ref_df['s006']).sum() / 1e9  # billions
            dif_rev = ref_rev - base_rev  # negative = cost
            col.append(round(dif_rev, 2))
        df[year] = col
    return df

# Run the calculation
print("Calculating 10-year fiscal cost of SGO credit...")
print("=" * 80)

results_df = run_calc(
    yr_range=range(2025, 2035),
    refs_policy=[sgo_reform],
    refs_base=[baseline],
    rec=Records.cps_constructor(),
    df=pd.DataFrame(index=["SGO Credit Cost"])
)

# Display results
print("\nAnnual Costs (in billions):")
print(results_df.T)

# Calculate totals
total_cost = results_df.sum(axis=1).values[0]
print(f"\n10-Year Total Cost: ${total_cost:,.2f} billion")
print(f"Average Annual Cost: ${total_cost/10:,.2f} billion")

# Save to CSV
results_df.T.to_csv('sgo_credit_cost_analysis.csv')
print("\nResults saved to: sgo_credit_cost_analysis.csv")

