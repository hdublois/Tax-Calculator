"""
Simple script to calculate 10-year fiscal cost of SGO credit.
Run this from the Tax-Calculator directory with the appropriate environment activated.
"""

from taxcalc import *
import pandas as pd

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

print("=" * 80)
print("SGO Credit 10-Year Fiscal Cost Analysis")
print("=" * 80)
print("\nBaseline: Current law without SGO credit (CR_SGO_c = 0)")
print("Reform: Current law with SGO credit ($1,700/$3,400)")
print("\nAnalysis period: 2025-2034")
print("=" * 80)

# Load records
print("\nLoading CPS data...")
recs = Records.cps_constructor()

# Calculate for each year
results = []
total_cost = 0.0

print("\nCalculating revenues...")
print("-" * 80)
print(f"{'Year':<8} {'Baseline ($B)':<18} {'Reform ($B)':<18} {'Cost ($B)':<18}")
print("-" * 80)

for year in range(2025, 2035):
    # Baseline (current law, CR_SGO_c = 0 by default)
    pol_base = Policy()
    calc_base = Calculator(pol_base, Records.cps_constructor())
    calc_base.advance_to_year(year)
    calc_base.calc_all()
    base_df = calc_base.dataframe(['iitax', 's006'])
    base_rev = (base_df['iitax'] * base_df['s006']).sum() / 1e9  # billions
    
    # Reform (with SGO credit)
    pol_ref = Policy()
    pol_ref.implement_reform(sgo_reform)
    calc_ref = Calculator(pol_ref, Records.cps_constructor())
    calc_ref.advance_to_year(year)
    calc_ref.calc_all()
    ref_df = calc_ref.dataframe(['iitax', 's006'])
    ref_rev = (ref_df['iitax'] * ref_df['s006']).sum() / 1e9  # billions
    
    # Cost = baseline revenue - reform revenue
    cost = base_rev - ref_rev
    total_cost += cost
    
    results.append({
        'year': year,
        'baseline_revenue': base_rev,
        'reform_revenue': ref_rev,
        'cost': cost
    })
    
    print(f"{year:<8} ${base_rev:>15,.2f}    ${ref_rev:>15,.2f}    ${cost:>15,.2f}")

print("-" * 80)
print(f"{'TOTAL':<8} {'':<18} {'':<18} ${total_cost:>15,.2f}")
print("=" * 80)

# Summary
print("\nSummary Statistics:")
print(f"  10-Year Total Cost: ${total_cost:,.2f} billion")
print(f"  Average Annual Cost: ${total_cost/10:,.2f} billion")
print(f"  First Year Cost (2025): ${results[0]['cost']:,.2f} billion")
print(f"  Final Year Cost (2034): ${results[-1]['cost']:,.2f} billion")

# Save results
results_df = pd.DataFrame(results)
results_df.to_csv('sgo_credit_cost_analysis.csv', index=False)
print(f"\nResults saved to: sgo_credit_cost_analysis.csv")

