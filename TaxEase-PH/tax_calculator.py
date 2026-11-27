"""
TaxEase PH - Philippine Income Tax Calculator Module
Compliant with National Internal Revenue Code (NIRC) as amended by:
- TRAIN Act (Republic Act No. 10963)
- Ease of Paying Taxes (EOPT) Act (Republic Act No. 11976)
"""

from typing import Dict, Any, Tuple


def calculate_train_graduated_tax(taxable_income: float) -> Tuple[float, str]:
    """
    Computes Philippine Individual Income Tax under the TRAIN Act
    Graduated Tax Brackets (Effective 2023 onwards).
    
    Returns:
        (tax_due, explanation_string)
    """
    if taxable_income <= 0:
        return 0.0, "Taxable income is PHP 0.00 or negative (No tax due)."
    
    if taxable_income <= 250000:
        return 0.0, "Bracket 1: Up to PHP 250,000 -> 0% (Tax Exempt)."
    
    elif taxable_income <= 400000:
        excess = taxable_income - 250000
        tax = excess * 0.15
        return tax, f"Bracket 2: 15% of excess over PHP 250,000 (15% * PHP {excess:,.2f}) = PHP {tax:,.2f}"
    
    elif taxable_income <= 800000:
        excess = taxable_income - 400000
        tax = 22500 + (excess * 0.20)
        return tax, f"Bracket 3: PHP 22,500 + 20% of excess over PHP 400,000 = PHP {tax:,.2f}"
    
    elif taxable_income <= 2000000:
        excess = taxable_income - 800000
        tax = 102500 + (excess * 0.25)
        return tax, f"Bracket 4: PHP 102,500 + 25% of excess over PHP 800,000 = PHP {tax:,.2f}"
    
    elif taxable_income <= 8000000:
        excess = taxable_income - 2000000
        tax = 402500 + (excess * 0.30)
        return tax, f"Bracket 5: PHP 402,500 + 30% of excess over PHP 2,000,000 = PHP {tax:,.2f}"
    
    else:
        excess = taxable_income - 8000000
        tax = 2202500 + (excess * 0.35)
        return tax, f"Bracket 6: PHP 2,202,500 + 35% of excess over PHP 8,000,000 = PHP {tax:,.2f}"


def calculate_8_percent_flat_tax(gross_revenue: float) -> Tuple[float, str, bool]:
    """
    Computes Optional 8% Flat Income Tax for purely self-employed / freelancers.
    Condition: Gross sales/receipts must not exceed PHP 3,000,000 (VAT threshold).
    
    Deduction: First PHP 250,000 is exempt (for pure freelance/business income).
    Exemption: Exempt from 3% Percentage Tax under Section 116.
    
    Returns:
        (tax_due, explanation_string, is_eligible)
    """
    if gross_revenue > 3000000:
        return 0.0, "Gross revenue exceeds PHP 3,000,000 VAT threshold. Ineligible for the 8% flat rate (must use Graduated Rates + VAT).", False
    
    taxable_base = max(0.0, gross_revenue - 250000.0)
    tax_due = taxable_base * 0.08
    explanation = (
        f"8% Flat Tax on excess over PHP 250,000: 8% * (PHP {gross_revenue:,.2f} - PHP 250,000.00) "
        f"= 8% * PHP {taxable_base:,.2f} = PHP {tax_due:,.2f}. (Also exempt from 3% percentage tax)."
    )
    return tax_due, explanation, True


def calculate_annual_mandatory_contributions(monthly_income: float) -> Dict[str, float]:
    """
    Estimates typical annual voluntary/self-employed statutory contributions.
    - SSS (approx max MSC ~ PHP 4,200/mo)
    - PhilHealth (5% premium shared or self-employed ~ PHP 500-PHP 5,000/mo)
    - Pag-IBIG / HDMF (PHP 200/mo minimum)
    """
    # SSS approximate monthly contribution
    if monthly_income <= 4000:
        sss_mo = 560.0
    elif monthly_income >= 30000:
        sss_mo = 4200.0
    else:
        sss_mo = min(4200.0, monthly_income * 0.14)
    
    # PhilHealth 5% rate capped at 10,000 max, min 500
    ph_mo = max(500.0, min(5000.0, monthly_income * 0.05))
    
    # Pag-IBIG HDMF fixed standard
    pagibig_mo = 200.0 if monthly_income <= 10000 else 400.0
    
    return {
        "monthly_sss": sss_mo,
        "monthly_philhealth": ph_mo,
        "monthly_pagibig": pagibig_mo,
        "annual_sss": sss_mo * 12,
        "annual_philhealth": ph_mo * 12,
        "annual_pagibig": pagibig_mo * 12,
        "total_annual_deductions": (sss_mo + ph_mo + pagibig_mo) * 12,
    }


def compare_tax_regimes(gross_annual: float, annual_deductions: float = 0.0) -> Dict[str, Any]:
    """
    Performs comprehensive side-by-side comparison between TRAIN Graduated Rates
    and the Optional 8% Flat Tax.
    """
    # 1. Graduated Rates computation
    taxable_graduated = max(0.0, gross_annual - annual_deductions)
    tax_graduated, exp_graduated = calculate_train_graduated_tax(taxable_graduated)
    net_graduated = gross_annual - tax_graduated - annual_deductions
    effective_rate_graduated = (tax_graduated / gross_annual * 100) if gross_annual > 0 else 0.0
    
    # 2. 8% Flat Tax computation
    tax_8pct, exp_8pct, eligible_8pct = calculate_8_percent_flat_tax(gross_annual)
    # The 8% option uses gross receipts less the PHP 250,000 exemption and
    # does not additionally deduct business expenses or mandatory contributions.
    net_8pct = gross_annual - tax_8pct
    effective_rate_8pct = (tax_8pct / gross_annual * 100) if gross_annual > 0 else 0.0
    
    # 3. Recommendation
    if not eligible_8pct:
        recommended_regime = "Graduated Rates (Mandatory: Gross > PHP 3,000,000)"
        savings = 0.0
        reason = "Gross revenue exceeds the statutory PHP 3M threshold for the 8% flat rate."
    elif tax_8pct < tax_graduated:
        recommended_regime = "Optional 8% Flat Tax"
        savings = tax_graduated - tax_8pct
        reason = f"The 8% Flat Tax saves you PHP {savings:,.2f} in taxes compared to Graduated Rates."
    elif tax_8pct > tax_graduated:
        recommended_regime = "Graduated Tax Rates"
        savings = tax_8pct - tax_graduated
        reason = f"Graduated Rates save you PHP {savings:,.2f} in taxes compared to the 8% Flat Tax."
    else:
        recommended_regime = "Either Regime"
        savings = 0.0
        reason = "Both tax regimes yield the exact same tax liability."
    
    return {
        "gross_annual": gross_annual,
        "annual_deductions": annual_deductions,
        "graduated": {
            "taxable_income": taxable_graduated,
            "tax_due": tax_graduated,
            "net_take_home": net_graduated,
            "effective_rate": effective_rate_graduated,
            "explanation": exp_graduated,
        },
        "flat_8pct": {
            "eligible": eligible_8pct,
            "taxable_base": max(0.0, gross_annual - 250000.0) if eligible_8pct else 0.0,
            "tax_due": tax_8pct,
            "net_take_home": net_8pct,
            "effective_rate": effective_rate_8pct,
            "explanation": exp_8pct,
        },
        "recommended_regime": recommended_regime,
        "savings": savings,
        "reason": reason,
    }


def parse_freelancer_income_text(text: str) -> Dict[str, float]:
    """
    Parses an uploaded freelance income summary or CSV to extract gross fees
    and reported mandatory contribution figures.
    """
    import re
    
    extracted = {
        "gross_pay": 0.0,
        "sss": 0.0,
        "philhealth": 0.0,
        "pagibig": 0.0,
        "tax_withheld": 0.0,
    }
    
    lines = text.splitlines()
    for line in lines:
        line_clean = line.strip().lower()
        
        # Look for numbers with optional commas and decimals
        nums = re.findall(r"[\d,]+(?:\.\d+)?", line)
        if not nums:
            continue
        try:
            val = float(nums[-1].replace(",", ""))
        except ValueError:
            continue
        
        if any(k in line_clean for k in ["gross", "total earnings", "basic salary", "client fee", "revenue"]):
            if val > extracted["gross_pay"]:
                extracted["gross_pay"] = val
        elif "sss" in line_clean:
            extracted["sss"] = val
        elif any(k in line_clean for k in ["philhealth", "philh"]):
            extracted["philhealth"] = val
        elif any(k in line_clean for k in ["pagibig", "pag-ibig", "hdmf"]):
            extracted["pagibig"] = val
        elif any(k in line_clean for k in ["withheld", "tax withheld", "wht", "bir"]):
            extracted["tax_withheld"] = val
            
    return extracted
