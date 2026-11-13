"""Heuristic HIPAA Safe Harbor *scanner* (optional mask).

This is **not** de-identification. It does not implement Safe Harbor, expert
determination, or a limited data set. It does not replace Philter, NLM Scrubber,
Presidio, or a URMC honest broker. Extract never calls this.

Identifiers follow URMC research-coordinator materials and HHS §164.514(b)(2)
(the 18). See ``docs/LEO_PHI.md``.
"""
from __future__ import annotations

import json
import re
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable

BANNER = (
    "NOT DE-IDENTIFIED. Heuristic scan/mask only. Not HIPAA Safe Harbor, "
    "not expert determination, not a limited data set. Do not treat this "
    "file as clean. Do not feed it to LEO extract as if PHI were gone. "
    "Approved path: honest broker / Philter / NLM Scrubber / ISD tool. "
    "docs/LEO_PHI.md"
)

# (code, hipaa letter, label) — 18 Safe Harbor classes
KINDS = (
    ("name", "A", "Names"),
    ("geo", "B", "Geography smaller than a state"),
    ("date", "C", "Dates related to a person (except year) / age > 89"),
    ("phone", "D", "Telephone numbers"),
    ("fax", "E", "Fax numbers"),
    ("email", "F", "E-mail addresses"),
    ("ssn", "G", "Social security numbers"),
    ("mrn", "H", "Medical record numbers"),
    ("plan", "I", "Health plan beneficiary numbers"),
    ("account", "J", "Account numbers"),
    ("license", "K", "Certificate / license numbers"),
    ("vehicle", "L", "Vehicle identifiers"),
    ("device", "M", "Device identifiers"),
    ("url", "N", "URLs"),
    ("ip", "O", "IP addresses"),
    ("biometric", "P", "Biometric identifiers"),
    ("photo", "Q", "Full-face photos"),
    ("other", "R", "Other unique identifying numbers / codes"),
)

_LABEL = {k: lab for k, _h, lab in KINDS}
_TAG = {
    "name": "[NAME]", "geo": "[GEO]", "date": "[DATE]", "phone": "[PHONE]",
    "fax": "[FAX]", "email": "[EMAIL]", "ssn": "[SSN]", "mrn": "[MRN]",
    "plan": "[PLAN_ID]", "account": "[ACCOUNT]", "license": "[LICENSE]",
    "vehicle": "[VEHICLE]", "device": "[DEVICE]", "url": "[URL]", "ip": "[IP]",
    "biometric": "[BIOMETRIC]", "photo": "[PHOTO]", "other": "[ID]",
}


@dataclass(frozen=True)
class Hit:
    kind: str
    hipaa: str
    start: int
    end: int
    excerpt: str


def _hits_for(kind: str, hipaa: str, text: str, rx: re.Pattern) -> list[Hit]:
    out = []
    for m in rx.finditer(text):
        raw = m.group(0)
        out.append(Hit(kind, hipaa, m.start(), m.end(), raw[:80]))
    return out


def scan(text: str) -> list[Hit]:
    """Find likely identifier spans. Overlaps are kept; mask() resolves them."""
    if not text:
        return []
    hits: list[Hit] = []
    # Structured first (high precision).
    hits += _hits_for("ssn", "G", text, re.compile(r"\b\d{3}-\d{2}-\d{4}\b"))
    hits += _hits_for("phone", "D", text, re.compile(
        r"\b(?:\+?1[-.\s])?(?:\(?\d{3}\)?[-.\s])\d{3}[-.\s]\d{4}\b"))
    hits += _hits_for("fax", "E", text, re.compile(
        r"\bfax(?:\s*(?:number|#|:))?\s*[:#]?\s*(?:\+?1[-.\s])?(?:\(?\d{3}\)?[-.\s])\d{3}[-.\s]\d{4}\b",
        re.I))
    hits += _hits_for("email", "F", text, re.compile(
        r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"))
    hits += _hits_for("url", "N", text, re.compile(
        r"\bhttps?://[^\s<>\"]+", re.I))
    hits += _hits_for("ip", "O", text, re.compile(
        r"\b(?:(?:25[0-5]|2[0-4]\d|[01]?\d\d?)\.){3}(?:25[0-5]|2[0-4]\d|[01]?\d\d?)\b"))
    # Label must end as a word (FIN ≠ "findings", VIN ≠ "vincristine"); the ID must contain a digit.
    def labeled(labels: str, min_len: int = 4) -> re.Pattern:
        return re.compile(
            rf"\b(?:{labels})(?![A-Za-z0-9])\s*[:#]?\s*(?=[A-Za-z-]*\d)[A-Za-z0-9-]{{{min_len},}}\b", re.I)

    hits += _hits_for("mrn", "H", text, labeled(r"MRN|medical\s+record(?:\s+number)?"))
    hits += _hits_for("plan", "I", text, labeled(
        r"member\s+id|subscriber\s+id|health\s+plan\s+(?:id|number)|beneficiary\s+(?:id|number)"))
    hits += _hits_for("account", "J", text, labeled(r"account\s+(?:number|no\.?)|account\s*#|acct\.?"))
    hits += _hits_for("license", "K", text, labeled(
        r"driver'?s?\s+license|license\s+number|license\s*#|DEA\s*#|DEA"))
    hits += _hits_for("vehicle", "L", text, labeled(r"VIN|license\s+plate", 5))
    hits += _hits_for("device", "M", text, labeled(
        r"device\s+(?:id|serial)|serial\s+number|serial\s*#|IMEI"))
    hits += _hits_for("other", "R", text, labeled(
        r"CSN|FIN|HAR|visit\s+number|encounter\s+(?:number|id)|NPI"))
    hits += _hits_for("date", "C", text, re.compile(
        r"\b(?:\d{1,2}[/-]\d{1,2}[/-]\d{2,4}|(?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2},\s+\d{4}|DOB\s*[:#]?\s*\S+)\b",
        re.I))
    hits += _hits_for("date", "C", text, re.compile(
        r"\b(?:9\d|1[0-2]\d)(?:\s*|-)?(?:year(?:s)?(?:\s+old)?|-year-old)\b", re.I))
    hits += _hits_for("geo", "B", text, re.compile(
        r"\b\d{1,5}\s+[A-Za-z0-9.'-]+(?:\s+[A-Za-z0-9.'-]+){0,4}\s+(?:Street|St\.?|Avenue|Ave\.?|Road|Rd\.?|Boulevard|Blvd\.?|Drive|Lane|Ln\.?|Court|Ct\.?|Way|Parkway)\b",
        re.I))
    hits += _hits_for("geo", "B", text, re.compile(
        r"\b(?:ZIP(?:\s*code)?|zip(?:\s*code)?)\s*[:#]?\s*\d{5}(?:-\d{4})?\b", re.I))
    hits += _hits_for("geo", "B", text, re.compile(
        r"\b[A-Z]{2}\s+\d{5}(?:-\d{4})?\b"))
    hits += _hits_for("name", "A", text, re.compile(
        r"\b(?i:patient(?:\s+name)?|pt\.?|name)\s*[:#]\s*[A-Z][A-Za-z.'-]+(?:\s+[A-Z][A-Za-z.'-]*)+\b"))
    hits += _hits_for("name", "A", text, re.compile(
        r"\b(?:Mr|Mrs|Ms|Miss|Mx|Dr)\.?\s+[A-Z][A-Za-z.'-]+(?:\s+[A-Z][A-Za-z.'-]*)?\b"))
    hits += _hits_for("biometric", "P", text, re.compile(
        r"\b(?:fingerprint|voice\s+print|retinal\s+scan|biometric)\b", re.I))
    hits += _hits_for("photo", "Q", text, re.compile(
        r"\b(?:full[-\s]?face\s+(?:photo|photograph|image)|facial\s+photograph)\b", re.I))
    return sorted(hits, key=lambda h: (h.start, -(h.end - h.start)))


def summarize(hits: Iterable[Hit]) -> dict[str, int]:
    counts = {k: 0 for k, _h, _l in KINDS}
    for h in hits:
        counts[h.kind] = counts.get(h.kind, 0) + 1
    return counts


def mask(text: str, hits: list[Hit] | None = None) -> str:
    """Replace scanned spans. Overlaps: longest first. Not Safe Harbor."""
    found = list(hits if hits is not None else scan(text))
    found.sort(key=lambda h: (h.start, -(h.end - h.start)))
    kept: list[Hit] = []
    last = -1
    for h in found:
        if h.start < last:
            continue
        kept.append(h)
        last = h.end
    parts: list[str] = []
    cursor = 0
    for h in kept:
        parts.append(text[cursor:h.start])
        parts.append(_TAG.get(h.kind, "[PHI]"))
        cursor = h.end
    parts.append(text[cursor:])
    return "".join(parts)


def scan_report(text: str, *, source: str = "") -> dict:
    hits = scan(text)
    counts = summarize(hits)
    return {
        "disclaimer": BANNER,
        "source": source,
        "n_hits": len(hits),
        "by_kind": {k: n for k, n in counts.items() if n},
        "kinds_documented": [
            {"kind": k, "hipaa": h, "label": lab} for k, h, lab in KINDS
        ],
        "hits": [asdict(h) for h in hits],
    }


def format_text_report(report: dict) -> str:
    lines = [BANNER, ""]
    if report.get("source"):
        lines.append(f"source: {report['source']}")
    lines.append(f"heuristic hits: {report['n_hits']}")
    if report["by_kind"]:
        lines.append("by kind:")
        for k, n in sorted(report["by_kind"].items()):
            lines.append(f"  {n:4d}  {k:10s}  {_LABEL.get(k, k)}")
    else:
        lines.append("No structured identifiers matched. That is not a clean bill.")
    lines.append("")
    lines.append("Credible de-id (not this command): Philter, NLM Scrubber, Presidio,")
    lines.append("URMC honest broker / ISD. Cloud PHI APIs: do not use.")
    return "\n".join(lines) + "\n"


def read_input(path: Path | None, stdin: str | None = None) -> tuple[str, str]:
    if path is None or str(path) == "-":
        return stdin or "", "-"
    p = path.expanduser()
    return p.read_text(encoding="utf-8", errors="replace"), str(p)
