# Week 22 — DevOps, IaC & Kubernetes

## Commit #324
**Message:** `feat(k8s): add Deployment manifest`
**Files:**

```file:advanced/devops_k8s/deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: web
  labels: {app: web}
spec:
  replicas: 3
  selector:
    matchLabels: {app: web}
  template:
    metadata:
      labels: {app: web}
    spec:
      containers:
        - name: web
          image: registry.example.com/mysite:latest
          ports: [{containerPort: 8000}]
          envFrom:
            - secretRef: {name: mysite-secrets}
          readinessProbe:
            httpGet: {path: /readyz, port: 8000}
            initialDelaySeconds: 5
          livenessProbe:
            httpGet: {path: /healthz, port: 8000}
          resources:
            requests: {cpu: 100m, memory: 256Mi}
            limits: {cpu: 500m, memory: 512Mi}
```

---

## Commit #325
**Message:** `feat(k8s): add Service and Ingress`
**Files:**

```file:advanced/devops_k8s/service-ingress.yaml
apiVersion: v1
kind: Service
metadata: {name: web}
spec:
  selector: {app: web}
  ports: [{port: 80, targetPort: 8000}]
---
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: web
  annotations:
    cert-manager.io/cluster-issuer: letsencrypt-prod
spec:
  tls:
    - hosts: [app.example.com]
      secretName: web-tls
  rules:
    - host: app.example.com
      http:
        paths:
          - path: /
            pathType: Prefix
            backend: {service: {name: web, port: {number: 80}}}
```

---

## Commit #326
**Message:** `feat(k8s): add ConfigMap and Secret templates`
**Files:**

```file:advanced/devops_k8s/config.yaml
apiVersion: v1
kind: ConfigMap
metadata: {name: mysite-config}
data:
  DJANGO_SETTINGS_MODULE: mysite.settings
  ALLOWED_HOSTS: app.example.com
---
apiVersion: v1
kind: Secret
metadata: {name: mysite-secrets}
type: Opaque
stringData:
  SECRET_KEY: "change-me"          # inject via sealed-secrets / SOPS in CI
  DATABASE_URL: "postgres://..."
  REDIS_URL: "redis://redis:6379/0"
```

---

## Commit #327
**Message:** `feat(k8s): add HorizontalPodAutoscaler`
**Files:**

```file:advanced/devops_k8s/hpa.yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata: {name: web}
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: web
  minReplicas: 3
  maxReplicas: 12
  metrics:
    - type: Resource
      resource:
        name: cpu
        target: {type: Utilization, averageUtilization: 70}
```

---

## Commit #328
**Message:** `feat(k8s): add migration Job`
**Files:**

```file:advanced/devops_k8s/migrate-job.yaml
apiVersion: batch/v1
kind: Job
metadata:
  name: migrate
spec:
  backoffLimit: 3
  template:
    spec:
      restartPolicy: Never
      containers:
        - name: migrate
          image: registry.example.com/mysite:latest
          command: ["python", "manage.py", "migrate", "--noinput"]
          envFrom:
            - secretRef: {name: mysite-secrets}
# Run as a pre-deploy hook (Helm hook / ArgoCD PreSync).
```

---

## Commit #329
**Message:** `feat(iac): add Terraform for managed Postgres`
**Files:**

```file:advanced/devops_k8s/postgres.tf
resource "aws_db_instance" "mysite" {
  identifier            = "mysite-prod"
  engine                = "postgres"
  engine_version        = "16"
  instance_class        = "db.t4g.medium"
  allocated_storage     = 50
  max_allocated_storage = 200
  multi_az              = true
  storage_encrypted     = true
  backup_retention_period = 14
  deletion_protection   = true
  db_name               = "mysite"
  username              = var.db_username
  password              = var.db_password
  skip_final_snapshot   = false
}
```

---

## Commit #330
**Message:** `feat(devops): add Makefile for common tasks`
**Files:**

```file:advanced/devops_k8s/Makefile
.PHONY: install test lint run migrate deploy

install:
	pip install -r requirements.txt

test:
	pytest -q

lint:
	ruff check . && ruff format --check .

run:
	python manage.py runserver

migrate:
	python manage.py migrate

deploy:
	kubectl apply -f advanced/devops_k8s/
```

---

## Commit #331
**Message:** `chore(devops): add pre-commit and ruff config`
**Files:**

```file:advanced/devops_k8s/.pre-commit-config.yaml
repos:
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.6.0
    hooks:
      - id: ruff
        args: [--fix]
      - id: ruff-format
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.6.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-added-large-files
```

---

## Commit #332
**Message:** `feat(devops): add database backup and restore scripts`
**Files:**

```file:advanced/devops_k8s/backup.sh
#!/usr/bin/env bash
# Nightly encrypted Postgres backup to S3.
set -euo pipefail

STAMP=$(date +%Y%m%d-%H%M%S)
FILE="backup-${STAMP}.sql.gz"

pg_dump "$DATABASE_URL" | gzip > "/tmp/${FILE}"
aws s3 cp "/tmp/${FILE}" "s3://${BACKUP_BUCKET}/postgres/${FILE}" \
  --sse aws:kms
rm -f "/tmp/${FILE}"
echo "backup uploaded: ${FILE}"
```

---

## Commit #333
**Message:** `docs(devops): add zero-downtime migration guide`
**Files:**

```file:advanced/devops_k8s/ZERO_DOWNTIME_MIGRATIONS.md
# Zero-downtime migrations

Deploy schema and code in compatible steps so old + new pods coexist.

## Adding a column
1. Add nullable column (or with DB default) — deploy.
2. Backfill in batches via a management command.
3. Start writing/reading it in code — deploy.
4. Add NOT NULL / constraints — deploy.

## Removing a column
1. Stop using it in code — deploy.
2. Drop the column in a later migration — deploy.

## Rules
- Never rename in one step: add new → migrate data → drop old.
- Avoid long table locks; use `CREATE INDEX CONCURRENTLY`.
- Keep each migration reversible.
```

---

## Commit #334
**Message:** `feat(observability): add OpenTelemetry tracing`
**Files:**

```file:advanced/devops_k8s/otel_tracing.py
"""
Distributed tracing with OpenTelemetry.

pip install opentelemetry-distro opentelemetry-instrumentation-django
opentelemetry-bootstrap -a install
"""

from opentelemetry import trace
from opentelemetry.instrumentation.django import DjangoInstrumentor


def setup_tracing():
    DjangoInstrumentor().instrument()
    return trace.get_tracer(__name__)

# Run with: opentelemetry-instrument python manage.py runserver
# Export via OTEL_EXPORTER_OTLP_ENDPOINT to Tempo/Jaeger.
```

---

## Commit #335
**Message:** `docs(week22): add DevOps and deployment reference`
**Files:**

```file:advanced/DEVOPS_REFERENCE.md
# Week 22 — DevOps, IaC & Kubernetes

- **Kubernetes** — Deployment with probes/resources, Service + Ingress (TLS),
  ConfigMap/Secret, HPA, pre-deploy migration Job.
- **IaC** — Terraform for managed, encrypted, multi-AZ Postgres.
- **Developer UX** — Makefile, pre-commit + ruff.
- **Operations** — encrypted nightly backups, zero-downtime migrations.
- **Tracing** — OpenTelemetry auto-instrumentation → OTLP collector.

## Release checklist
- [ ] Migrations are backward-compatible
- [ ] Probes green before traffic shifts
- [ ] Secrets sealed (SOPS/sealed-secrets), never plaintext in git
- [ ] Rollback path verified
```
