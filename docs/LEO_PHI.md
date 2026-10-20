# PHI scan / mask (not de-identification)

`bin/leo phi-scan` and `bin/leo phi-mask` flag or redact **likely** HIPAA identifiers. They are **not** Safe Harbor, not expert determination, and not a limited data set. Extract does **not** call them.

URMC’s list is the federal 18 ([research coordinator HIPAA topics](https://www.urmc.rochester.edu/MediaLibraries/URMCMedia/education/HIPAA-Topics-for-Research-Coordinators.pdf); [HHS de-identification](https://www.hhs.gov/hipaa/for-professionals/privacy/special-topics/de-identification/index.html)).

| HIPAA | Identifier | This scanner |
|---|---|---|
| A | Names | Labeled `Patient:` / `Mr.` lines only |
| B | Geography smaller than a state | Street + ZIP with a label or `NY 14620` |
| C | Dates except year; ages > 89 | `MM/DD/YYYY`, month names, `90-year-old` |
| D–F | Phone, fax, email | Regex |
| G–K | SSN, MRN, plan, account, license | Labeled numbers |
| L–M | Vehicle / device IDs | VIN, plate, serial, IMEI |
| N–O | URL, IP | Regex |
| P–Q | Biometrics, full-face photos | Phrase only (no image model) |
| R | Other unique codes | CSN / FIN / encounter / NPI |

A study ID must not be derived from these (initials do not count).

## Commands

```bash
bin/leo phi-scan note.txt
bin/leo phi-scan note.txt --json
bin/leo phi-mask note.txt -o note_phi.txt   # still PHI; banner on the file
```

Exit 2 from `phi-scan` means at least one heuristic hit — not “this is identified,” and 0 is not “this is clean.”

## Credible tools (use these if ISD says de-identify first)

| Tool | Why it counts | Here |
|---|---|---|
| **URMC honest broker / ISD pipeline** | The one the institution signs | Use if they have one |
| **Philter** (UCSF; Norgeot et al., *npj Digit Med* 2020) | Clinical-note de-id, published | Best open option if ISD allows |
| **NLM Scrubber** | NIH clinical scrubber | Conservative |
| **Microsoft Presidio** | NER + regex PII | Detector; not epilepsy-tuned |
| **i2b2/n2c2 2014 de-id** (Stubbs / Uzuner) | Shared-task baselines | Research, not a product |
| Cloud PHI APIs | Strong NER | **Do not use** — the note leaves the hospital |

RSRB + ISD choose Safe Harbor, expert determination, or a limited data set (DUA). If they allow **full PHI on this host**, do not mask — you need dates and ages for the phenotype. If they require de-id **first**, run Philter or their broker, then LEO.

## What we will not do

Wire the masker into `leo batch` / extract. Call the output de-identified. Send notes to a cloud PHI API. Treat `utils/validation.py` `sanitize_medical_text` as Safe Harbor (SSN/phone/email/MRN only; unused by extract).
