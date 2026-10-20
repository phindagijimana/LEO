"""Gates for a locally hosted single-user research extract.

**Required (notes must not leave the box).** CDB and Med42 already on disk;
Hugging Face / transformers offline; no cloud LLM backend.

**Not required on 127.0.0.1.** Web login, ``MEDAI_LEO_IRB_ACK``, job-folder
``0700`` — reported as info. Login **is** required if the UI binds a node
address (Slurm). Written IRB/IS approval is policy, not a code flag.

``bin/leo check --research`` reports all rows. ``start|batch|run --research``
fails only on required misses.
"""
from __future__ import annotations

import os
import stat
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

REPO = Path(__file__).resolve().parent.parent
WEIGHTS_GLOB = "models--m42-health--Llama3-Med42-8B"
CDB = REPO / "data" / "medcat_cdb_epilepsy" / "cdb"
JOBS = REPO / "data" / "leo_jobs"
TRAINING = REPO / "data" / "leo_training"

OFFLINE_KEYS = ("HF_HUB_OFFLINE", "TRANSFORMERS_OFFLINE", "HF_HUB_DISABLE_TELEMETRY")


@dataclass(frozen=True)
class Check:
    ok: bool
    name: str
    detail: str
    required: bool = True


def research_requested(flag: bool | None = None) -> bool:
    if flag:
        return True
    return os.environ.get("MEDAI_LEO_RESEARCH", "").strip().lower() in ("1", "true", "yes")


def apply_offline_env() -> None:
    """Stop Hugging Face / transformers from phoning home or downloading."""
    os.environ["HF_HUB_OFFLINE"] = "1"
    os.environ["TRANSFORMERS_OFFLINE"] = "1"
    os.environ["HF_HUB_DISABLE_TELEMETRY"] = "1"
    os.environ.setdefault("MEDAI_LEO_BLOCK_CLOUD", "1")


def offline_env_set() -> bool:
    return all(os.environ.get(k, "").strip() in ("1", "true", "yes") for k in ("HF_HUB_OFFLINE", "TRANSFORMERS_OFFLINE"))


def weights_dir(repo: Path | None = None) -> Path:
    return (repo or REPO) / "model_cache"


def weights_present(repo: Path | None = None) -> bool:
    cache = weights_dir(repo)
    return cache.is_dir() and any(cache.glob(WEIGHTS_GLOB))


def cdb_present(repo: Path | None = None) -> bool:
    return ((repo or REPO) / "data" / "medcat_cdb_epilepsy" / "cdb").exists()


def irb_acked() -> bool:
    return os.environ.get("MEDAI_LEO_IRB_ACK", "").strip().lower() in ("1", "true", "yes")


def cloud_backend_requested() -> bool:
    for key in ("MEDAI_LEO_BACKEND", "MEDAI_EXTRACT_BACKEND", "LEO_LLM_BACKEND"):
        val = os.environ.get(key, "").strip().lower()
        if val.startswith("openai") or val in ("cloud", "api"):
            return True
    return False


def bind_is_loopback(host: str | None = None) -> bool:
    h = (host or os.environ.get("SERVICE_HOST") or "").strip().lower()
    return h in ("", "127.0.0.1", "localhost", "::1")


def login_ready() -> tuple[bool, str]:
    from services import leo_auth
    users = leo_auth.load_users()
    if users:
        return True, f"{len(users)} user(s) in {leo_auth.users_path()}"
    if leo_auth.enabled():
        return False, "MEDAI_LEO_REQUIRE_LOGIN is on but no users — nobody can sign in. bin/leo user add NAME"
    return False, "login off (optional on 127.0.0.1; required if the UI binds a node address)"


def _mode_bits(path: Path) -> int:
    return stat.S_IMODE(path.stat().st_mode)


def secure_dir(path: Path, *, mode: int = 0o700) -> Check:
    """Create *path* owner-only. Fail if group/other can still read."""
    path.mkdir(parents=True, exist_ok=True)
    try:
        path.chmod(mode)
    except OSError as e:
        return Check(False, f"permissions {path}", str(e))
    bits = _mode_bits(path)
    if bits & 0o077:
        return Check(False, f"permissions {path}", f"mode {oct(bits)} still allows group/other — chmod 0700 failed (NFS?)")
    return Check(True, f"permissions {path}", oct(bits))


def jobs_secure(repo: Path | None = None) -> list[Check]:
    root = repo or REPO
    out = []
    for p in (root / "data" / "leo_jobs", root / "data" / "leo_training"):
        chk = secure_dir(p)
        out.append(Check(chk.ok, chk.name, chk.detail, required=False))
    return out


def report(repo: Path | None = None, host: str | None = None) -> list[Check]:
    root = repo or REPO
    login_ok, login_detail = login_ready()
    need_login = not bind_is_loopback(host)
    rows = [
        Check(cdb_present(root), "EpExtra CDB on disk", str(root / "data" / "medcat_cdb_epilepsy" / "cdb")),
        Check(weights_present(root), "Med42-8B weights on disk (no download)", str(weights_dir(root))),
        Check(offline_env_set(), "HF/transformers offline",
              "set by --research; or export HF_HUB_OFFLINE=1 TRANSFORMERS_OFFLINE=1"),
        Check(not cloud_backend_requested(), "no cloud LLM backend",
              "unset MEDAI_LEO_BACKEND=openai — notes must not leave the host"),
        Check(login_ok, "web login", login_detail, required=need_login),
        Check(irb_acked(), "IRB/IS written approval",
              "policy — send docs/LEO_IS_REQUEST.md; not a code gate", required=False),
    ]
    rows.extend(jobs_secure(root))
    return rows


def failed(rows: Iterable[Check], *, required_only: bool = True) -> list[Check]:
    return [c for c in rows if not c.ok and (c.required if required_only else True)]


def enforce(*, apply_offline: bool = True, repo: Path | None = None,
            host: str | None = None) -> list[Check]:
    if apply_offline:
        apply_offline_env()
    rows = report(repo, host=host)
    bad = failed(rows)
    if bad:
        lines = "; ".join(f"{c.name}: {c.detail}" for c in bad)
        raise SystemExit(
            "[leo] --research refused: " + lines +
            ". See docs/LEO_RESEARCH_DEPLOY.md. Synthetic smoke: omit --research."
        )
    return rows
