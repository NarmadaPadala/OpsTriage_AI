# Data Quality Report

## Source

- Source CSV: `data/sample/sample_incidents.csv`
- Total records: 100
- Required columns: incident_id, incident_title, incident_description, support_team
- Split seed: 42
- Target split: 70% train / 15% validation / 15% test

## Validation Summary

- Required columns: passed
- Required values: passed
- Support-team taxonomy: passed
- Duplicate title and description pairs: 0

## Class Distribution

| Support Team | Records |
|---|---:|
| Claims Engineering | 7 |
| Membership Engineering | 7 |
| Provider Systems | 7 |
| Digital Experience | 7 |
| Billing Systems | 7 |
| Data Engineering | 7 |
| API Platform | 7 |
| Integration Services | 7 |
| Infrastructure | 7 |
| Database Engineering | 7 |
| Identity & Access | 6 |
| Security | 6 |
| Reporting & Analytics | 6 |
| Batch Processing | 6 |
| DevOps | 6 |

## Split Distribution

| Split | Records |
|---|---:|
| train | 70 |
| validation | 15 |
| test | 15 |

## Split Distribution by Support Team

| Support Team | Train | Validation | Test |
|---|---:|---:|---:|
| Claims Engineering | 5 | 1 | 1 |
| Membership Engineering | 5 | 1 | 1 |
| Provider Systems | 5 | 1 | 1 |
| Digital Experience | 5 | 1 | 1 |
| Billing Systems | 5 | 1 | 1 |
| Data Engineering | 5 | 1 | 1 |
| API Platform | 5 | 1 | 1 |
| Integration Services | 5 | 1 | 1 |
| Infrastructure | 5 | 1 | 1 |
| Database Engineering | 5 | 1 | 1 |
| Identity & Access | 4 | 1 | 1 |
| Security | 4 | 1 | 1 |
| Reporting & Analytics | 4 | 1 | 1 |
| Batch Processing | 4 | 1 | 1 |
| DevOps | 4 | 1 | 1 |

## Duplicate Pairs

No duplicate title and description pairs found.

## Review Notes

- This report validates the 100-row public-safe synthetic pilot dataset.
- The processed JSON files are intended for SFT pipeline testing, not final model claims.
- No model training was performed by the dataset preparation utility.
