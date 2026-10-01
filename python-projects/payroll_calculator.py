"""
Kenyan Statutory Payroll & Tax Reconciliation Engine
Author: Shadrack Makomere Amboka
Description: Computes PAYE, NSSF, SHIF, and Housing Levy according to Kenyan tax bands 
             and outputs a structured payroll summary.
"""

import pandas as pd


def calculate_nssf(gross_salary: float) -> float:
    """Calculates NSSF contribution based on Tier I & Tier II caps."""
    tier1_limit = 7000.0
    tier2_limit = 36000.0

    if gross_salary <= tier1_limit:
        return gross_salary * 0.06
    elif gross_salary <= tier2_limit:
        return (tier1_limit * 0.06) + ((gross_salary - tier1_limit) * 0.06)
    else:
        return (tier1_limit * 0.06) + ((tier2_limit - tier1_limit) * 0.06)


def calculate_shif(gross_salary: float) -> float:
    """Calculates Social Health Insurance Fund (SHIF) contribution at 2.75%."""
    min_shif = 300.0
    computed_shif = gross_salary * 0.0275
    return max(min_shif, computed_shif)


def calculate_housing_levy(gross_salary: float) -> float:
    """Calculates Affordable Housing Levy at 1.5%."""
    return gross_salary * 0.015


def calculate_paye(gross_salary: float, nssf_deduction: float) -> float:
    """
    Computes PAYE tax using standard progressive tax bands 
    after deducting NSSF tax-exempt contribution.
    """
    taxable_pay = gross_salary - nssf_deduction
    personal_relief = 2400.0  # Monthly Personal Relief

    # Progressive Tax Bands
    if taxable_pay <= 24000:
        gross_tax = taxable_pay * 0.10
    elif taxable_pay <= 32333:
        gross_tax = (24000 * 0.10) + ((taxable_pay - 24000) * 0.25)
    elif taxable_pay <= 500000:
        gross_tax = (24000 * 0.10) + (8333 * 0.25) + ((taxable_pay - 32333) * 0.30)
    elif taxable_pay <= 800000:
        gross_tax = (24000 * 0.10) + (8333 * 0.25) + (467667 * 0.30) + ((taxable_pay - 500000) * 0.325)
    else:
        gross_tax = (24000 * 0.10) + (8333 * 0.25) + (467667 * 0.30) + (300000 * 0.325) + ((taxable_pay - 800000) * 0.35)

    net_paye = max(0.0, gross_tax - personal_relief)
    return net_paye


def process_payroll(employee_data: list) -> pd.DataFrame:
    """Processes batch employee records and builds a payroll summary DataFrame."""
    processed_records = []

    for emp in employee_data:
        gross = emp['gross_salary']
        nssf = calculate_nssf(gross)
        shif = calculate_shif(gross)
        housing_levy = calculate_housing_levy(gross)
        paye = calculate_paye(gross, nssf)

        total_deductions = nssf + shif + housing_levy + paye
        net_pay = gross - total_deductions

        processed_records.append({
            'Employee ID': emp['emp_id'],
            'Employee Name': emp['name'],
            'Gross Salary (KES)': round(gross, 2),
            'NSSF (KES)': round(nssf, 2),
            'SHIF (KES)': round(shif, 2),
            'Housing Levy (KES)': round(housing_levy, 2),
            'PAYE (KES)': round(paye, 2),
            'Total Deductions (KES)': round(total_deductions, 2),
            'Net Pay (KES)': round(net_pay, 2)
        })

    return pd.DataFrame(processed_records)


# Demonstration Run
if __name__ == "__main__":
    sample_employees = [
        {'emp_id': 'EMP001', 'name': 'John Doe', 'gross_salary': 45000.0},
        {'emp_id': 'EMP002', 'name': 'Jane Smith', 'gross_salary': 85000.0},
        {'emp_id': 'EMP003', 'name': 'Samuel Otieno', 'gross_salary': 150000.0},
        {'emp_id': 'EMP004', 'name': 'Mary Wanjiku', 'gross_salary': 28000.0}
    ]

    payroll_df = process_payroll(sample_employees)
    print("=========================================================================")
    print("                 MONTHLY PAYROLL & TAX SUMMARY                           ")
    print("=========================================================================")
    print(payroll_df.to_string(index=False))
