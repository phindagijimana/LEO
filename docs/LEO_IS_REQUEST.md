# Request text for hospital privacy / research IS

Fill the brackets. Send from the PI or the honest broker. LEO cannot submit this for you.

---

**Subject.** Local LLM phenotype extract (LEO / Med42-8B) on protocol [NUMBER] — host approval

We request written confirmation that identifiable (or limited-dataset) epilepsy clinic notes under IRB protocol **[NUMBER]** may be processed as follows.

**Software.** LEO (`leo-v0.9`), local Med42-8B + EpExtra. No cloud LLM. Hugging Face and UMLS downloads are disabled in research-host mode. Research use only; not a medical device; no write-back to the EHR.

**Compute we will use**

- Login / UI bind: **[hostname]**, `127.0.0.1` or SSH tunnel
- Note and output path: **[NFS path, e.g. /mnt/…/study/leo/]**
- Slurm partition and GRES: **[partition]**, **[gres]**
- GPU nodes those jobs can land on: **[node list or constraint]**

**What is written.** Full note text in `*_leo.csv|xlsx`, `.claims.csv`, `.provenance.json`, and owner-only job folders (`data/leo_jobs/`, 24-hour scratch, **not encrypted**). Optional `data/leo_training/` if a reviewer permits training use (not deleted with the job). Audit log has user/event only, not note text.

**Who can read it.** The named investigators; OS/NFS group as configured; backup/snapshot owners. Web UI login is required when research-host mode binds the UI to a node address. `bin/leo batch` and `bin/leo run` open no port. A UI on `127.0.0.1` does not require a user.

**Network.** No note text to OpenAI, Hugging Face, or other external APIs during extract. Weights and the MedCAT CDB are already on disk.

**Ask.** May we run this workflow on the hosts and paths above? If the home directory is not an approved PHI volume, please name the volume we must use.

---

Keep their reply with the protocol. Then run `bin/leo start --local --research` (offline extract). No extra env flag is required.
