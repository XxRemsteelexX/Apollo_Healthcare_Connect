# Apollo Healthcare Connect Agent Guide

## Purpose

Apollo Healthcare Connect is Glenn's WGU Data Science capstone: a Flask-based, multi-modal medical triage demo with text symptom routing and medical image classification.

This project is **educational/research/demo software only**. It must not be represented as clinical advice, diagnosis, treatment guidance, or an FDA/clinical decision system.

## First-read checklist for agents

Before changing code, read:

1. `readme.md` for project purpose and disclaimers.
2. `app_production.py` for deployed behavior.
3. `app.py` for development behavior.
4. `changes/TEMPLATE.md` for the required change packet.
5. Existing templates in `templates/` before editing route flows.

## Run commands

Local development:

```bash
python -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
python app.py
```

Production command currently documented by the app:

```bash
gunicorn --bind 0.0.0.0:5000 app_production:app
```

Lightweight baseline verification that does **not** require installing heavy ML dependencies:

```bash
python -m py_compile app.py app_production.py symptom_classifier.py medical_classifier_training.py
python -m pytest tests/test_static_contracts.py -q
```

Optional static checks:

```bash
ruff check .
bandit -q -r . -x ./.venv,./notebooks
```

## Change process

For non-trivial changes:

1. Create a new file under `changes/<short-id>.md` from `changes/TEMPLATE.md`.
2. Define intent, scope, acceptance criteria, risk, rollback, and verification.
3. Use a branch/worktree; do not make risky direct edits to `main`.
4. Add/update tests before changing behavior when practical.
5. Run the lightweight baseline verification before handoff.
6. Report files changed, commands run, risks, and rollback notes.

## Safety and compliance rules

- Preserve the educational/research disclaimer on public pages and reports.
- Do not claim the system is medically validated, approved, diagnostic, or safe for real clinical decision-making.
- Do not remove conservative emergency-routing behavior without explicit review.
- Do not log, commit, or print patient symptoms, phone numbers, uploaded image paths, AWS credentials, Flask secret keys, or model bucket credentials.
- Uploaded medical images are sensitive; treat local `uploads/` as private runtime data, not source code.
- Do not commit model artifacts, downloaded S3 zips, `.env` files, credentials, or runtime uploads.
- Backend validation is authoritative; frontend validation is only user experience.

## Deployment and rollback notes

- Production is Flask/Gunicorn using `app_production:app`.
- Model downloads come from S3; failures fall back to demo predictions. Any model-loading change needs explicit testing of both real-model and fallback paths.
- Before production deployment, verify:
  - app starts with required environment variables/secrets present;
  - `/`, `/triage`, `/upload`, `/schedule`, `/about`, and `/contact` render;
  - medical disclaimer still appears;
  - uploads are size/type constrained;
  - rollback target/previous commit is known.

## High-risk changes needing review

Require second-agent or human review for:

- triage/routing logic;
- emergency keyword changes;
- model thresholds or label mappings;
- S3/model download behavior;
- patient data/session/report handling;
- file upload handling;
- public medical/disclaimer copy;
- deployment/runtime configuration.
