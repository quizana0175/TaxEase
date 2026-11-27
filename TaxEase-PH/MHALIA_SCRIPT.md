# Mhalia's Word-for-Word Video Presentation Script
**TaxEase PH: Philippine Income Tax & Advisory Assistant**  
**CSIT 349: Applied AI | Section G01 | Cebu Institute of Technology – University**  
**Presenter:** Paton-og, Mhalia Nicole P.  
**Coverage:** Slide 1 (Title & Intro), Slide 3 (Core Features), Slide 4 (Tech Stack & Design), Demo Tab 1 (Advisory Chatbot), Demo Tab 3 (BIR Deadlines & Forms)

> **Tips before recording:**
> - Speak clearly and at a conversational pace — no need to rush.
> - You may say "po" and "sir/ma'am" naturally where it feels right.
> - Each section has a **[Pause]** marker — use that moment to click to the next slide or switch tabs.

---

## SLIDE 1 — Title & Group Introduction

*(Show the title slide — TaxEase PH: Philippine Income Tax & Advisory Assistant)*

---

**SCRIPT:**

"Good day, Engr. Pardillo, and to everyone watching.

My name is **Mhalia Nicole Paton-og**, and I will be introducing our CSIT 349 final project: **TaxEase PH — Philippine Income Tax and Advisory Assistant**.

TaxEase PH is an **LLM-powered fintech chatbot** designed specifically to help **Filipino freelancers and self-employed professionals** understand and manage their income tax compliance under Philippine law.

This project was built by our group — **Ethan James Saranza**, **Louise Daniella Quizana**, and myself. I handled the **system architecture and UI development**. Ethan worked on the **prompt engineering and security defenses**, and Louise handled the **tax computation logic and testing**.

We developed this under the guidance of **Engr. Jun Albert Pardillo**, for CSIT 349 Section G01 here at Cebu Institute of Technology – University.

[Pause — click to Slide 3]"

---

## SLIDE 3 — Core Features & Architecture

*(Show the Core Features slide — 5 feature cards)*

---

**SCRIPT:**

"Now let me walk you through the **five core features** of TaxEase PH.

**Feature 1: The Real-Time Tax Metrics Dashboard.**  
At the top of the application, you will see four live metric cards — Taxable Base, Estimated Tax Due, Net Take-Home Pay, and Optimal Tax Savings. These cards update automatically every time the user adjusts their income input, so Filipino freelancers can see their tax picture in real time.

**Feature 2: The Regime Comparison Engine.**  
This is the heart of the application. TaxEase PH performs a deterministic, side-by-side comparison of two tax regimes under the TRAIN Act: the **Graduated Income Tax Rate Schedule** and the **Optional 8% Flat Income Tax**. The system calculates the exact take-home difference between the two, so the freelancer knows exactly which option saves them more money — and by how much.

**Feature 3: The Conversational Advisory Chatbot.**  
Powered by the **Google Gemini API**, the chatbot answers tax-related questions from Filipino freelancers in natural language. It covers BIR Forms 1901, 1701Q, 1701A, and 2316. And importantly — if there is no internet connection or no API key available, the app switches to an **offline fallback engine** that uses built-in statutory knowledge, so users are never left without guidance.

**Feature 4: The Payslip and Earnings File Parser.**  
Freelancers can upload their payslip or income summary in `.txt` or `.csv` format. The system automatically reads the file, detects the gross receipts amount, and applies it directly to the calculator inputs with one click.

**Feature 5: The Exportable Compliance Report.**  
Once the user has entered their income details, they can download a formatted `.txt` compliance report that includes their computed tax figures, the recommended tax regime, and a BIR filing checklist — all in one document they can keep for reference.

[Pause — click to Slide 4]"

---

## SLIDE 4 — Tech Stack & Design Decisions

*(Show the Tech Stack & Design Decisions slide — 5 horizontal stack rows)*

---

**SCRIPT:**

"Now let's look at how TaxEase PH was **built** — our tech stack and the design decisions we made.

**For the frontend**, we used **Streamlit**. It gave us a clean, reactive single-page application with tab navigation, chat message components, and real-time session state management — all without needing a separate backend.

**For the AI engine**, we integrated the **Google Gemini API** — specifically the `gemini-2.5-flash` and `gemini-1.5-flash` models. We chose Gemini for its low latency, large context window, and the fact that it has a free tier — making it very practical for academic deployment on Streamlit Community Cloud.

**For the offline fallback**, we built a **deterministic compliance engine** backed by a built-in statutory knowledge base. This means TaxEase PH works even without an API key or an internet connection — the app always has an answer for the user.

**For the knowledge base**, we implemented a **RAG — Retrieval-Augmented Generation — system** covering the NIRC, the TRAIN Act RA 10963, and the Ease of Paying Taxes Act RA 11976. And this RAG is **scoped exclusively to freelancer and self-employed tax rules** — which brings me to our most important design decision.

**Our scope decision.** Following consultation with our instructor, we made a deliberate choice: rather than building a broad system for all taxpayer categories, **we focused TaxEase PH entirely on Filipino freelancers and self-employed professionals**. This allowed us to go deeper — more accurate tax rules, more specific guidance, and a more reliable system overall. Quality over breadth. And we believe that decision made TaxEase PH significantly more useful for its intended users.

[Pause — switch to the live app]"

---

## DEMO — Tab 1: Advisory Chatbot

*(Switch to the running app at localhost:8501, go to Tab 1: Advisory Chatbot)*

---

**SCRIPT:**

"Let me now do a **live demonstration** of TaxEase PH.

Here is the application running live. You can see the sidebar on the left with the project title, our group members, the AI engine status, and the disclaimer.

At the very top, notice the **four metric cards** — right now they are showing values based on the default income entered in the calculator. These update live as the input changes.

I am now on **Tab 1: Advisory Chatbot**.

Let me type a question that a typical Filipino freelancer would ask:

*(Type in the chat:)*  
`I am a freelance graphic designer earning PHP 650,000 annually. Am I eligible to elect the Optional 8% Flat Income Tax?`

*(Press Enter / Send)*

You can see TaxEase AI is processing the query. *(Wait for response.)*

And here is the response. Notice how the AI:  
- Confirms **eligibility** based on the PHP 3,000,000 gross receipts threshold under the TRAIN Act  
- Shows the **mathematical computation step-by-step** — Gross Revenue minus the PHP 250,000 baseline exemption, multiplied by 8%  
- Compares that result with the Graduated Tax Rate so the freelancer can see the difference  
- And ends with the **mandatory advisory disclaimer** — reminding the user to verify the figures against official BIR forms before filing

This is the kind of clear, structured guidance that our system prompt engineering and math rules — which Louise will explain in detail on Slide 5 — are designed to produce.

[Pause — click to Tab 3]"

---

## DEMO — Tab 3: BIR Deadlines & Forms

*(Click on Tab 3: BIR Deadlines & Forms)*

---

**SCRIPT:**

"Now I will show you **Tab 3: BIR Deadlines and Forms**.

This tab is designed to solve one of the most common problems Filipino freelancers face — **not knowing when to file and what forms to submit**.

At the top, you will see the **2026 BIR Filing Calendar** — a full table of all statutory quarterly and annual deadlines under the Ease of Paying Taxes Act, RA 11976. This covers Form 1701Q quarterly returns, the annual Form 1701A, and other key BIR deadlines a self-employed professional needs to track throughout the year.

Below the calendar, we have the **BIR Form 1901 Registration Checklist**. Form 1901 is the registration form every Filipino freelancer must file with the BIR before they can legally start issuing official receipts and declaring income.

The checklist here is **interactive** — a freelancer can actually check off each requirement as they complete it, and they will see a live progress bar tracking how complete their registration preparation is.

The requirements listed include:  
- BIR Form 1901 — two copies  
- A valid government ID showing their address and date of birth  
- Their DTI certificate or Professional Tax Receipt  
- Proof of place of business — such as a barangay clearance or lease agreement  
- BIR Form 1906 for their Authority to Print official receipts  
- And their registered books of account

This checklist turns what used to be a confusing BIR visit into a simple, manageable process — especially for first-time freelancers who have never registered before.

That concludes my portion of the presentation. For the Tax Calculator and regime comparison demo, I will pass it to **Louise**. And for the Security and Prompt Defense demonstration, **Ethan** will take over.

Thank you."

---

*End of Mhalia's script.*

---

> **Reminders:**
> - Your Slide 1 opens the entire presentation — speak with confidence, it sets the tone.
> - During the chatbot demo, wait for the response to fully appear before continuing narration.
> - You do not need to memorise this word-for-word — read naturally and speak as if explaining to a friend.
> - If the teacher asks a question during your demo, it's okay to pause and answer directly.
