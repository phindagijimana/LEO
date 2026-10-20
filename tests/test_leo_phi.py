"""PHI scanner/masker. Synthetic strings only — not real notes."""
from __future__ import annotations

from services import leo_phi as p

SYNTH = """
Patient: Jane Q Public
DOB: 03/15/1930
90-year-old woman.
MRN: 99887766
SSN 123-45-6789
Phone 585-555-0100
fax: 585-555-0199
Email jane.public@example.com
Lives at 12 Main Street, NY 14620
http://intranet.example/note/1
IP 10.1.2.3
Member ID: HPB998877
account number: 4400998877
driver license: D1234567
VIN: 1HGCM82633A004352
device serial: ABC12345XYZ
CSN: 4400112233
fingerprint on file
full-face photograph stored
Takes lamotrigine 200 mg for focal epilepsy.
"""


def test_scan_hits_safe_harbor_classes():
    kinds = {h.kind for h in p.scan(SYNTH)}
    for need in ("name", "date", "mrn", "ssn", "phone", "fax", "email", "geo",
                 "url", "ip", "vehicle", "device", "other", "plan", "account",
                 "license", "biometric", "photo"):
        assert need in kinds, need


def test_does_not_blank_drug_or_phenotype():
    hits = p.scan("Takes lamotrigine 200 mg for focal epilepsy. Onset age 11.")
    kinds = {h.kind for h in hits}
    assert "name" not in kinds
    assert "mrn" not in kinds
    masked = p.mask("Takes lamotrigine 200 mg for focal epilepsy.")
    assert "lamotrigine" in masked
    assert "focal epilepsy" in masked


def test_mask_replaces_ssn_and_keeps_banner_out_of_span():
    text = "SSN 123-45-6789 and lamotrigine"
    out = p.mask(text)
    assert "123-45-6789" not in out
    assert "[SSN]" in out
    assert "lamotrigine" in out


def test_report_disclaimer():
    r = p.scan_report(SYNTH, source="synth")
    assert "NOT DE-IDENTIFIED" in r["disclaimer"]
    assert r["n_hits"] > 0
    assert "Safe Harbor" in p.format_text_report(r)


def test_not_imported_by_extract():
    from pathlib import Path
    root = Path(__file__).resolve().parents[1]
    for rel in (
        "services/leo_runtime.py",
        "services/leo_batch.py",
        "services/leo_job.py",
        "services/extract.py",
        "services/router.py",
    ):
        text = (root / rel).read_text(encoding="utf-8")
        assert "leo_phi" not in text, rel
