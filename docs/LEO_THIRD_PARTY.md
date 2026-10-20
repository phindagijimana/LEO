# Third-party pieces you bring (not shipped)

LEO’s git repo is source + docs. A second lab installs the same way QSIPrep-class tools do: clone, create `venv-medcat`, place licensed artifacts.

| Artifact | Whose license | Where it lives | In git? |
|---|---|---|---|
| Llama-3-Med42-8B | M42 / Llama 3 community license | `model_cache/models--m42-health--Llama3-Med42-8B` | No |
| UMLS | NLM UMLS license | `.env` `UMLS_API_KEY` (never printed) | No |
| Epilepsy MedCAT CDB | Built from UMLS locally | `data/medcat_cdb_epilepsy/cdb` | No |
| ILAE / ACNS text | Society copyright | cited; not a gazetteer dump into E | n/a |

Do not vendor these into a zip you email. Do not commit `.env`. Hugging Face access is per-user. `--research` **refuses** to download weights at extract time. The container image is code-only (`Dockerfile.leo`); mount these paths at run time (`docs/LEO_CONTAINER.md`).

See `docs/LEO_HOSTING.md` and `docs/MedCAT.md`.
