"""
Accounts Receivable (A/R) Aging & Allowance Analysis
Author: Shadrack Makomere Amboka
Description: Classifies unpaid customer invoices into standard aging buckets 
             and calculates expected credit loss / bad debt provision reserves.
"""

from datetime import datetime
import pandas as pd


def categorize_aging(days_overdue: int) -> str:
    """Categorizes overdue days into standard aging brackets."""
    if days_overdue <= 0:
        return 'Current (0 Days)'
    elif days_overdue <= 30:
        return '1 - 30 Days'
    elif days_overdue <= 60:
        return '31 - 60 Days'
    elif days_overdue <= 90:
        return '61 - 90 Days'
    else:
        return '90+ Days (High Risk)'


def calculate_bad_debt_provision(amount: float, bucket: str) -> float:
    """Applies risk-based provision percentages to aged balances."""
    rates = {
        'Current (0 Days)': 0.01,       # 1% allowance
        '1 - 30 Days': 0.05,            # 5% allowance
        '31 - 60 Days': 0.15,           # 15% allowance
        '61 - 90 Days': 0.40,           # 40% allowance
        '90+ Days (High Risk)': 0.75    # 75% allowance
    }
    return amount * rates.get(bucket, 0.0)


def analyze_ar_ledger(invoices: list, evaluation_date_str: str) -> pd.DataFrame:
    """Processes invoice schedule and generates an aged receivables schedule."""
    eval_date = datetime.strptime(evaluation_date_str, '%Y-%m-%d')
    records = []

    for inv in invoices:
        due_date = datetime.strptime(inv['due_date'], '%Y-%m-%d')
        days_overdue = (eval_date - due_date).days
        aging_bucket = categorize_aging(days_overdue)
        provision = calculate_bad_debt_provision(inv['amount'], aging_bucket)

        records.append({
            'Customer Name': inv['customer'],
            'Invoice Ref': inv['invoice_no'],
            'Amount (KES)': inv['amount'],
            'Due Date': inv['due_date'],
            'Days Overdue': max(0, days_overdue),
            'Aging Bracket': aging_bucket,
            'Bad Debt Provision (KES)': round(provision, 2)
        })

    return pd.DataFrame(records)


# Demonstration Run
if __name__ == "__main__":
    sample_invoices = [
        {'customer': 'Acreage Ltd', 'invoice_no': 'INV-1001', 'amount': 120000.0, 'due_date': '2026-09-15'},
        {'customer': 'Beacon School', 'invoice_no': 'INV-1002', 'amount': 45000.0, 'due_date': '2026-08-20'},
        {'customer': 'Crestline Traders', 'invoice_no': 'INV-1003', 'amount': 88000.0, 'due_date': '2026-07-10'},
        {'customer': 'Delta Logistics', 'invoice_no': 'INV-1004', 'amount': 210000.0, 'due_date': '2026-05-01'},
        {'customer': 'Acreage Ltd', 'invoice_no': 'INV-1005', 'amount': 35000.0, 'due_date': '2026-09-28'}
    ]

    analysis_date = "2026-10-01"
    ar_df = analyze_ar_ledger(sample_invoices, analysis_date)

    print("=========================================================================")
    print(f"             A/R AGING & PROVISION REPORT (As of {analysis_date})        ")
    print("=========================================================================")
    print(ar_df.to_string(index=False))

    # Summary by Bucket
    summary = ar_df.groupby('Aging Bracket').agg(
        Total_Outstanding=('Amount (KES)', 'sum'),
        Total_Provision=('Bad Debt Provision (KES)', 'sum')
    ).reset_index()

    print("\n-------------------------------------------------------------------------")
    print("                     EXPOSURE SUMMARY BY AGING BRACKET                     ")
    print("-------------------------------------------------------------------------")
    print(summary.to_string(index=False))
