# Documentation

## Key Dataset Terms

To help you interpret the data across tables, here’s a quick reference to common terms used throughout this dataset:

- ICD-10: International Classification of Diseases, 10th Revision — Standardized diagnostic codes used to describe medical conditions.

- CPT: Current Procedural Terminology — Codes used to identify medical procedures and services.

- HCP: Healthcare Professional — Refers to individual medical providers such as doctors, specialists, nurse practitioners, etc.

- HCO: Healthcare Organization — Entities like hospitals, health systems, clinics, and ambulatory surgical centers.

- Claim: A documented billable interaction between a patient and a provider for healthcare services.

- Patient: The individual receiving medical treatment or services.

- Procedure: A clinical or medical operation, including diagnostic or therapeutic services (e.g., surgeries, screenings).

- Drug: A pharmaceutical product that is either prescribed or administered (e.g., Ozempic, Humira).

- Therapy Area: The specific medical specialty or clinical area targeted by a drug or procedure (e.g., endocrinology, cardiology).

- KOL: Key Opinion Leader — Influential healthcare professionals engaged in research, education, or thought leadership.

- Trial: A clinical research study (often listed on ClinicalTrials.gov) used to evaluate drugs, medical devices, or treatments.

---

## Payments to HCPs (as_lsf_v1)

Tracks financial transactions between life science firms and healthcare providers. Captures provider NPIs, firm names, associated products, nature of payments (e.g., education, lodging), payment year, and transaction amount. Enables analysis of industry-provider financial relationships.

---

## Provider Details (as_providers_v1)
Comprehensive details about healthcare professionals, including full name, gender, specialties, NPI information, affiliated hospitals, contact methods, and social profiles. Serves as a central provider directory for identity resolution and segmentation.

---

## Referral Patterns (as_providers_referrals_v2)
Documents referral interactions between providers. Fields include provider NPIs, names, geolocation, hospital affiliations, diagnosis and procedure codes, total charges, and patient volumes. Key for studying care transitions and referral behaviors.

---

## Diagnosis & Procedure Details (as_providers_referrals_v2 duplicate)
Shares the schema with the referral patterns table but focuses on capturing detailed diagnosis (ICD-10) and procedure (CPT) metadata for deeper clinical and billing insights.

---

## Pharmacy Claims (fct_pharmacy_clear_claim_allstatus_cluster_brand)
Captures detailed prescription transaction records, including drug identifiers (NDC), prescriber and payer information, fill and payment details, and associated diagnoses. Crucial for analyzing drug utilization, access, and payer dynamics.

---

## Condition Directory (mf_conditions)
Provides a taxonomy of medical conditions and procedures used in the dataset, including display names, coding type, and trial cohort sizes. Supports tagging and semantic classification in clinical analytics.

---

## KOL Providers (mf_providers)
Contains rich profile data on Key Opinion Leaders (KOLs) including names, NPIs, affiliations, training history, contact info, ratings, and biographies. Useful for identifying high-impact providers across therapeutic areas.

---

## KOL Scores (mf_scores)
Links provider NPIs and medical conditions to a scored value, often reflecting expertise, relevance, or prominence. Supports benchmarking, ranking, and KOL network analysis.

---