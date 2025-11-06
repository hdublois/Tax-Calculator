"""
Calculate the 10-year fiscal cost of the SGO (Scholarship Granting Organization) tax credit.

This script compares:
- Baseline: Current law without the SGO credit (CR_SGO_c = 0)
- Reform: Current law with the SGO credit (CR_SGO_c = $1,700/$3,400)
"""

import os
import sys
import pandas as pd
import numpy as np

# Add the taxcalc directory to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from taxcalc import Policy, Records, Calculator

def calculate_revenue(calc):
    """
    Calculate total income tax revenue from calculator.
    
    Parameters
    ----------
    calc : Calculator
        Calculator object with calculated taxes
    
    Returns
    -------
    float
        Total income tax revenue (in billions)
    """
    # Get the dataframe with calculated values
    df = calc.dataframe(['iitax', 's006'])
    
    # Calculate weighted sum: (iitax * weight).sum()
    total_revenue = (df['iitax'] * df['s006']).sum()
    
    # Convert to billions
    return total_revenue / 1e9

def main():
    """Main function to calculate 10-year cost of SGO credit."""
    
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
    
    # Start year for calculations
    start_year = 2025
    end_year = 2034
    
    print("=" * 80)
    print("SGO Credit 10-Year Fiscal Cost Analysis")
    print("=" * 80)
    print(f"\nBaseline: Current law without SGO credit (CR_SGO_c = 0)")
    print(f"Reform: Current law with SGO credit ($1,700/$3,400)")
    print(f"\nAnalysis period: {start_year}-{end_year}")
    print("=" * 80)
    
    # Load CPS data
    print("\nLoading CPS data...")
    recs = Records.cps_constructor()
    
    # Create baseline policy (current law, credit = 0 by default)
    print("Creating baseline policy...")
    baseline_policy = Policy()
    
    # Create reform policy (with SGO credit)
    print("Creating reform policy...")
    reform_policy = Policy()
    reform_policy.implement_reform(sgo_reform)
    
    # Calculate revenue for each year
    print("\nCalculating revenues...")
    print("-" * 80)
    print(f"{'Year':<8} {'Baseline ($B)':<18} {'Reform ($B)':<18} {'Cost ($B)':<18}")
    print("-" * 80)
    
    total_cost = 0.0
    results = []
    
    for year in range(start_year, end_year + 1):
        # Create fresh records for each year
        recs_base = Records.cps_constructor()
        recs_ref = Records.cps_constructor()
        
        # Baseline
        pol_base = Policy()
        calc_base = Calculator(policy=pol_base, records=recs_base)
        calc_base.advance_to_year(year)
        calc_base.calc_all()
        baseline_rev = calculate_revenue(calc_base)
        
        # Reform
        pol_ref = Policy()
        pol_ref.implement_reform(sgo_reform)
        calc_ref = Calculator(policy=pol_ref, records=recs_ref)
        calc_ref.advance_to_year(year)
        calc_ref.calc_all()
        reform_rev = calculate_revenue(calc_ref)
        
        # Calculate cost (negative of revenue change)
        cost = baseline_rev - reform_rev
        total_cost += cost
        
        results.append({
            'year': year,
            'baseline_revenue': baseline_rev,
            'reform_revenue': reform_rev,
            'cost': cost
        })
        
        print(f"{year:<8} ${baseline_rev:>15,.2f}    ${reform_rev:>15,.2f}    ${cost:>15,.2f}")
    
    print("-" * 80)
    print(f"{'TOTAL':<8} {'':<18} {'':<18} ${total_cost:>15,.2f}")
    print("=" * 80)
    
    # Summary statistics
    print("\nSummary Statistics:")
    print(f"  10-Year Total Cost: ${total_cost:,.2f} billion")
    print(f"  Average Annual Cost: ${total_cost/10:,.2f} billion")
    print(f"  First Year Cost ({start_year}): ${results[0]['cost']:,.2f} billion")
    print(f"  Final Year Cost ({end_year}): ${results[-1]['cost']:,.2f} billion")
    
    # Save results to CSV
    results_df = pd.DataFrame(results)
    output_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 
                               'sgo_credit_cost_analysis.csv')
    results_df.to_csv(output_file, index=False)
    print(f"\nResults saved to: {output_file}")
    
    return results_df, total_cost

if __name__ == '__main__':
    results_df, total_cost = main()

