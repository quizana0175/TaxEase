"""
TaxEase PH - Philippine BIR Knowledge Base & RAG Retrieval Module
Curated statutory references covering:
- National Internal Revenue Code (NIRC)
- TRAIN Act (Republic Act No. 10963)
- Ease of Paying Taxes (EOPT) Act (Republic Act No. 11976)
- BIR Revenue Regulations & Deadlines
"""

from typing import List, Dict, Any


BIR_KNOWLEDGE_DOCS = [
    {
        "id": "freelancer_scope",
        "title": "Philippine Freelancer and Independent-Contractor Tax Scope",
        "keywords": ["freelancer", "independent contractor", "virtual assistant", "va", "upwork", "fiverr", "online work", "professional", "sole proprietor"],
        "content": (
            "Philippine freelancers and independent contractors who receive client fees are generally "
            "treated as self-employed individuals or professionals. This includes VAs, designers, "
            "developers, writers, tutors, and online sellers. Registration, books or simplified records, "
            "quarterly payments, and annual filing depend on business/professional income, not on whether "
            "the client is local or foreign. Foreign-platform income is still Philippine gross receipt "
            "when it is received, and all material facts should be documented and reported."
        ),
    },
    {
        "id": "bir_form_1901",
        "title": "BIR Form 1901: Application for Registration for Self-Employed & Professionals",
        "keywords": ["1901", "register", "registration", "freelancer", "dti", "tin", "requirements", "start", "books"],
        "content": (
            "BIR Form 1901 is the Application for Registration for Self-Employed Individuals, "
            "Sole Proprietorships, Freelancers, and Professionals (General Professional Partnerships).\n"
            "- Key Requirements: Valid Government ID, DTI Certificate of Business Name (if trade name used) "
            "or PRC ID/Professional tax receipt (for licensed professionals), Proof of Address/Barangay Clearance, "
            "and BIR Form 1906 (Application for Authority to Print Official Receipts/Invoices).\n"
            "- Crucial Step: Opting for the 8% Flat Income Tax must be indicated on the initial Form 1901 registration "
            "or in the 1st Quarter Income Tax Return (Form 1701Q). Otherwise, Graduated Rates will default."
        ),
    },
    {
        "id": "bir_form_1701q",
        "title": "BIR Form 1701Q: Quarterly Income Tax Return for Individuals",
        "keywords": ["1701q", "quarterly", "deadlines", "q1", "q2", "q3", "filing", "may 15", "august 15", "november 15"],
        "content": (
            "BIR Form 1701Q is filed quarterly by self-employed individuals, freelancers, and mixed-income earners.\n"
            "- Filing Deadlines:\n"
            "  * Q1 (Jan - Mar): On or before MAY 15\n"
            "  * Q2 (Apr - Jun): On or before AUGUST 15\n"
            "  * Q3 (Jul - Sep): On or before NOVEMBER 15\n"
            "- Note: There is NO Q4 Form 1701Q; the final quarter is covered in the Annual Return (Form 1701 / 1701A).\n"
            "- 8% Taxpayers: Compute tax on cumulative gross revenue minus the PHP 250,000 standard deduction (for pure business/freelance income)."
        ),
    },
    {
        "id": "bir_form_1701a",
        "title": "BIR Form 1701A: Annual Income Tax Return for Purely Business/Profession",
        "keywords": ["1701a", "annual", "april 15", "return", "year-end", "income tax return"],
        "content": (
            "BIR Form 1701A is the Annual Income Tax Return for Individuals Earning Purely from Business/Profession "
            "under either Graduated Rates with Optional Standard Deduction (OSD) or the Optional 8% Flat Tax.\n"
            "- Filing Deadline: On or before APRIL 15 following the close of the calendar year.\n"
        ),
    },
    {
        "id": "train_act_8pct",
        "title": "TRAIN Act (RA 10963): Optional 8% Flat Income Tax vs. Graduated Rates",
        "keywords": ["8%", "flat tax", "train act", "regime", "graduated", "percentage tax", "3m", "3000000", "threshold"],
        "content": (
            "Under the TRAIN Act (RA 10963):\n"
            "- Self-employed individuals and freelancers with gross sales/receipts NOT exceeding PHP 3,000,000 "
            "may elect the Optional 8% Flat Income Tax Rate.\n"
            "- Tax Basis: 8% on gross sales/receipts in excess of PHP 250,000 (for pure freelance/business income).\n"
            "- Advantage: In lieu of both graduated income tax AND 3% percentage tax (Section 116).\n"
            "- Non-Eligibility: If gross exceeds PHP 3,000,000 or if the taxpayer is subject to VAT, "
            "they MUST use graduated income tax rates."
        ),
    },
    {
        "id": "eopt_act_11976",
        "title": "Ease of Paying Taxes (EOPT) Act (RA 11976) Highlights",
        "keywords": ["eopt", "11976", "ease of paying taxes", "classification", "micro", "books of accounts", "file anywhere"],
        "content": (
            "The Ease of Paying Taxes (EOPT) Act (Republic Act No. 11976) introduced taxpayer-friendly reforms:\n"
            "1. Taxpayer Classification: Categorizes taxpayers into Micro (gross sales < PHP 3M), Small (PHP 3M to < 20M), "
            "Medium (PHP 20M to < 1B), and Large (PHP 1B and above).\n"
            "2. File and Pay Anywhere: Taxpayers can now file returns and pay internal revenue taxes at ANY authorized "
            "agent bank (AAB), Revenue District Office (RDO), or authorized tax software provider without territorial penalty.\n"
            "3. Micro Taxpayer Relief: Micro taxpayers are exempt from maintaining complex books of accounts "
            "if utilizing simplified invoicing/accounting rules."
        ),
    },
]


def retrieve_relevant_bir_context(query: str, top_k: int = 2) -> str:
    """
    Retrieves the most relevant BIR documents using keyword and semantic matching.
    Provides RAG-grounded context for the LLM chatbot.
    """
    q_tokens = set(query.lower().replace("?", "").replace(",", "").split())
    scored_docs = []
    
    for doc in BIR_KNOWLEDGE_DOCS:
        score = 0
        # Match keywords
        for kw in doc["keywords"]:
            if kw in query.lower():
                score += 3
        # Match token overlap in title and content
        title_tokens = set(doc["title"].lower().split())
        score += len(q_tokens.intersection(title_tokens)) * 2
        
        content_tokens = set(doc["content"].lower().split())
        score += len(q_tokens.intersection(content_tokens)) * 0.5
        
        scored_docs.append((score, doc))
        
    # Sort by descending score
    scored_docs.sort(key=lambda x: x[0], reverse=True)
    top_matches = [d for s, d in scored_docs[:top_k] if s > 0]
    
    if not top_matches:
        # Fallback to general TRAIN and 1701Q info if no specific keyword matched
        top_matches = [BIR_KNOWLEDGE_DOCS[1], BIR_KNOWLEDGE_DOCS[4]]
        
    context_blocks = []
    for doc in top_matches:
        context_blocks.append(f"[{doc['title']}]\n{doc['content']}")
        
    return "\n\n".join(context_blocks)
