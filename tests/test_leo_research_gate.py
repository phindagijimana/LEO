"""Research-host gates. No GPU, no note text."""
from __future__ import annotations

import os

import pytest

from services import leo_research_gate as g


def test_research_flag_and_offline(monkeypatch):
    monkeypatch.delenv("LEO_RESEARCH", raising=False)
    assert g.research_requested(False) is False
    assert g.research_requested(True) is True
    monkeypatch.setenv("LEO_RESEARCH", "1")
    assert g.research_requested(False) is True
    g.apply_offline_env()
    assert os.environ["HF_HUB_OFFLINE"] == "1"
    assert os.environ["TRANSFORMERS_OFFLINE"] == "1"
    assert g.offline_env_set()


def test_cloud_backend_blocked(monkeypatch):
    monkeypatch.delenv("LEO_BACKEND", raising=False)
    assert g.cloud_backend_requested() is False
    monkeypatch.setenv("LEO_BACKEND", "openai:gpt-4")
    assert g.cloud_backend_requested() is True


def test_loopback_login_not_required():
    assert g.bind_is_loopback("127.0.0.1")
    assert g.bind_is_loopback("localhost")
    assert not g.bind_is_loopback("gpu-node-01")


def test_secure_dir_owner_only(tmp_path):
    d = tmp_path / "jobs"
    chk = g.secure_dir(d)
    assert chk.ok
    assert (d.stat().st_mode & 0o077) == 0


def test_optional_rows_do_not_block_enforce(tmp_path, monkeypatch):
    monkeypatch.setenv("HF_HUB_OFFLINE", "1")
    monkeypatch.setenv("TRANSFORMERS_OFFLINE", "1")
    monkeypatch.delenv("LEO_IRB_ACK", raising=False)
    monkeypatch.delenv("LEO_BACKEND", raising=False)
    monkeypatch.setenv("LEO_USERS", str(tmp_path / "nousers.json"))
    monkeypatch.setenv("APP_HOME", str(tmp_path))
    cache = tmp_path / "model_cache" / "models--m42-health--Llama3-Med42-8B"
    cache.mkdir(parents=True)
    (cache / "config.json").write_text("{}")
    (tmp_path / "data" / "medcat_cdb_epilepsy" / "cdb").mkdir(parents=True)
    rows = {c.name: c for c in g.report(tmp_path, host="127.0.0.1")}
    assert rows["web login"].required is False
    assert rows["IRB/IS written approval"].required is False
    g.enforce(apply_offline=True, repo=tmp_path, host="127.0.0.1")


def test_login_required_on_node_bind(tmp_path, monkeypatch):
    monkeypatch.setenv("HF_HUB_OFFLINE", "1")
    monkeypatch.setenv("TRANSFORMERS_OFFLINE", "1")
    monkeypatch.delenv("LEO_BACKEND", raising=False)
    monkeypatch.setenv("LEO_USERS", str(tmp_path / "nousers.json"))
    monkeypatch.setenv("APP_HOME", str(tmp_path))
    cache = tmp_path / "model_cache" / "models--m42-health--Llama3-Med42-8B"
    cache.mkdir(parents=True)
    (cache / "config.json").write_text("{}")
    (tmp_path / "data" / "medcat_cdb_epilepsy" / "cdb").mkdir(parents=True)
    rows = {c.name: c for c in g.report(tmp_path, host="gpu-node-01")}
    assert rows["web login"].required is True
    with pytest.raises(SystemExit) as ei:
        g.enforce(apply_offline=True, repo=tmp_path, host="gpu-node-01")
    assert "web login" in str(ei.value)


def test_batch_needs_no_login_but_node_ui_does(tmp_path, monkeypatch):
    from argparse import Namespace
    from scripts import leo_cli
    monkeypatch.setattr(g, "REPO", tmp_path)
    monkeypatch.setenv("SERVICE_HOST", "0.0.0.0")
    monkeypatch.delenv("LEO_BACKEND", raising=False)
    monkeypatch.setenv("LEO_USERS", str(tmp_path / "nousers.json"))
    monkeypatch.setenv("APP_HOME", str(tmp_path))
    cache = tmp_path / "model_cache" / "models--m42-health--Llama3-Med42-8B"
    cache.mkdir(parents=True)
    (cache / "config.json").write_text("{}")
    (tmp_path / "data" / "medcat_cdb_epilepsy" / "cdb").mkdir(parents=True)
    leo_cli._enforce_research(Namespace(research=True, local=True))
    with pytest.raises(SystemExit) as ei:
        leo_cli._enforce_research(Namespace(research=True, local=True, host="0.0.0.0"))
    assert "web login" in str(ei.value)


def test_enforce_refuses_without_weights(tmp_path, monkeypatch):
    monkeypatch.delenv("LEO_BACKEND", raising=False)
    monkeypatch.setenv("APP_HOME", str(tmp_path))
    with pytest.raises(SystemExit) as ei:
        g.enforce(apply_offline=True, repo=tmp_path, host="127.0.0.1")
    assert "--research refused" in str(ei.value)
