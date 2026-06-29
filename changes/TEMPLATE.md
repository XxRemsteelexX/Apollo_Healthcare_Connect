# Change: <short name>

## Intent

What problem are we solving, and why now?

## Scope

### In

- 

### Out

- 

## Acceptance criteria

- [ ] 

## Affected systems

- Routes/templates:
- Models/inference:
- Uploads/session data:
- Deployment/runtime:
- External services/secrets:

## Risk classification

Pick all that apply:

- [ ] docs-only
- [ ] frontend/template only
- [ ] Flask route or session behavior
- [ ] file upload or patient data
- [ ] model inference/triage logic
- [ ] S3/model artifact/deployment behavior
- [ ] public medical/safety copy

## Safety/privacy considerations

- Does this affect patient symptoms, phone numbers, uploaded images, or reports?
- Does this alter any medical routing recommendation or confidence threshold?
- Does this preserve the educational/research disclaimer?
- Could this fail open or present demo output as clinical guidance?

## Test / verification plan

Required lightweight baseline:

```bash
python -m py_compile app.py app_production.py symptom_classifier.py medical_classifier_training.py
python -m pytest tests/test_static_contracts.py -q
```

Additional checks for this change:

- [ ] 

## Rollback / roll-forward plan

How do we safely return to the previous behavior if this breaks?

## Worker handoff

- Branch/worktree:
- Files changed:
- Commands run:
- Known risks:
- Clean git status or explanation:
