# CD Pipeline — Post CI Stage: End-to-End Deployment Guide

## Where CD Begins

```
CI Complete ✓
  Image: company.jfrog.io/docker-dev-local/my-app:a3f5c2d1
  Stored in: Artifactory
  Build Info: Published
        ↓
  CD Pipeline Triggered
        ↓
  Pull Image from Artifactory
        ↓
  Deploy to DEV → QA → STAGING → PRODUCTION
        ↓
  Health Checks + Smoke Tests
        ↓
  Live ✅
```

```mermaid
flowchart TD
    A[CI Complete - Image in Artifactory] --> B[CD Pipeline Triggered]
    B --> C{Trigger Type}
    C -->|Auto - main branch| D[Deploy to DEV]
    C -->|Manual / Tag| E[Deploy to STAGING]
    C -->|Release Tag| F[Deploy to PRODUCTION]

    D --> D1[Pull Image from Artifactory]
    D1 --> D2[Helm Chart Update / K8s Manifest]
    D2 --> D3[kubectl apply / helm upgrade]
    D3 --> D4[Health Check + Smoke Test]
    D4 --> D5{Dev OK?}
    D5 -->|Pass| E
    D5 -->|Fail| D6[Rollback - helm rollback]

    E --> E1[Pull Image from Artifactory]
    E1 --> E2[Promote Image - dev to staging repo]
    E2 --> E3[Helm Upgrade - staging namespace]
    E3 --> E4[Integration Tests]
    E4 --> E5{Staging OK?}
    E5 -->|Pass| G[Manual Approval Gate]
    E5 -->|Fail| E6[Rollback + Alert]

    G -->|Approved| F
    G -->|Rejected| H[Stop - Fix Required]

    F --> F1[Promote Image - staging to release repo]
    F1 --> F2[Blue/Green or Canary Deploy]
    F2 --> F3[Health Check + Smoke Test]
    F3 --> F4{Prod OK?}
    F4 -->|Pass| DONE[✅ Production Live]
    F4 -->|Fail| F5[Automatic Rollback]
```

---

## 1. CD Pipeline Trigger Mechanisms

```mermaid
flowchart LR
    A[CI Pipeline Finish] -->|downstream trigger| B[CD Pipeline]
    C[GitLab Tag Push v1.4.2] -->|tag event| B
    D[Manual GitLab UI button] -->|manual trigger| B
    E[Scheduled Pipeline] -->|cron trigger| B
    F[ArgoCD Git Polling] -->|GitOps sync| G[ArgoCD CD]
```

| Trigger | When Used | Branch/Tag |
|---|---|---|
| Auto downstream | Every merge to `main` → deploy to DEV | `main` |
| Git tag push | Version release → deploy to STAGING/PROD | `v*.*.*` |
| Manual button | On-demand deploy to any environment | Any |
| ArgoCD sync | GitOps — detects image tag change in Git | Any |
| Scheduled | Nightly deploy to QA with latest image | `main` |

---

## 2. Environment Promotion Flow

```
Artifactory Repos mirror environment promotion:

  docker-dev-local      ← CI pushes here (every commit)
         ↓  jfrog promote
  docker-staging-local  ← QA & Staging deploys pull from here
         ↓  jfrog promote (release only)
  docker-release-local  ← Production pulls ONLY from here
```

### Image Pull per Environment
| Environment | Pulls From | Who Triggers |
|---|---|---|
| DEV | `docker-dev-local` | Automatic after CI |
| QA | `docker-staging-local` | Automatic after DEV pass |
| STAGING | `docker-staging-local` | Automatic after QA pass |
| PRODUCTION | `docker-release-local` | Manual approval required |

---

## 3. Complete CD `.gitlab-ci.yml`

```yaml
# This is the CD pipeline — separate file or same file with environment stages
stages:
  - deploy-dev
  - test-dev
  - deploy-qa
  - test-qa
  - deploy-staging
  - test-staging
  - approve-production
  - deploy-production
  - verify-production

variables:
  ARTIFACTORY_URL: "$ARTIFACTORY_URL"
  ARTIFACTORY_USER: "$ARTIFACTORY_USER"
  ARTIFACTORY_PASSWORD: "$ARTIFACTORY_PASSWORD"
  IMAGE_NAME: "my-app"
  IMAGE_TAG: "$CI_COMMIT_SHORT_SHA"
  HELM_CHART_PATH: "./helm/my-app"
  KUBE_NAMESPACE_DEV: "dev"
  KUBE_NAMESPACE_QA: "qa"
  KUBE_NAMESPACE_STAGING: "staging"
  KUBE_NAMESPACE_PROD: "production"

# ── STAGE 1: Deploy to DEV ───────────────────────────────────────
deploy-dev:
  stage: deploy-dev
  image: dtzar/helm-kubectl:latest
  environment:
    name: development
    url: https://dev.myapp.company.com
  before_script:
    # Authenticate to Kubernetes cluster
    - echo "$KUBE_CONFIG_DEV" | base64 -d > ~/.kube/config
    # Login to Artifactory for image pull secret
    - kubectl create secret docker-registry artifactory-creds
        --docker-server=$ARTIFACTORY_URL
        --docker-username=$ARTIFACTORY_USER
        --docker-password=$ARTIFACTORY_PASSWORD
        --namespace=$KUBE_NAMESPACE_DEV
        --dry-run=client -o yaml | kubectl apply -f -
  script:
    # Promote image from dev to staging repo in Artifactory
    - |
      curl -u $ARTIFACTORY_USER:$ARTIFACTORY_PASSWORD \
        -X POST "$ARTIFACTORY_URL/artifactory/api/docker/docker-dev-local/v2/promote" \
        -H "Content-Type: application/json" \
        -d "{\"targetRepo\":\"docker-staging-local\",
             \"dockerRepository\":\"$IMAGE_NAME\",
             \"tag\":\"$IMAGE_TAG\",
             \"copy\":true}"

    # Deploy using Helm
    - helm upgrade --install my-app $HELM_CHART_PATH
        --namespace $KUBE_NAMESPACE_DEV
        --create-namespace
        --set image.repository=$ARTIFACTORY_URL/docker-dev-local/$IMAGE_NAME
        --set image.tag=$IMAGE_TAG
        --set image.pullSecret=artifactory-creds
        --set env=development
        --set replicaCount=1
        --wait
        --timeout 5m
        --atomic                              # auto-rollback on failure

    - echo "Deployed $IMAGE_NAME:$IMAGE_TAG to DEV"
  rules:
    - if: '$CI_COMMIT_BRANCH == "main"'

# ── STAGE 2: Smoke Test DEV ──────────────────────────────────────
test-dev:
  stage: test-dev
  image: curlimages/curl:latest
  script:
    - sleep 30   # wait for pods to be ready
    - |
      RESPONSE=$(curl -s -o /dev/null -w "%{http_code}" \
        https://dev.myapp.company.com/actuator/health)
      if [ "$RESPONSE" != "200" ]; then
        echo "Health check FAILED with HTTP $RESPONSE"
        exit 1
      fi
      echo "DEV health check PASSED"
    # Run smoke test suite
    - curl -f https://dev.myapp.company.com/api/smoke-test
  rules:
    - if: '$CI_COMMIT_BRANCH == "main"'

# ── STAGE 3: Deploy to QA ────────────────────────────────────────
deploy-qa:
  stage: deploy-qa
  image: dtzar/helm-kubectl:latest
  environment:
    name: qa
    url: https://qa.myapp.company.com
  before_script:
    - echo "$KUBE_CONFIG_QA" | base64 -d > ~/.kube/config
    - kubectl create secret docker-registry artifactory-creds
        --docker-server=$ARTIFACTORY_URL
        --docker-username=$ARTIFACTORY_USER
        --docker-password=$ARTIFACTORY_PASSWORD
        --namespace=$KUBE_NAMESPACE_QA
        --dry-run=client -o yaml | kubectl apply -f -
  script:
    - helm upgrade --install my-app $HELM_CHART_PATH
        --namespace $KUBE_NAMESPACE_QA
        --create-namespace
        --set image.repository=$ARTIFACTORY_URL/docker-staging-local/$IMAGE_NAME
        --set image.tag=$IMAGE_TAG
        --set image.pullSecret=artifactory-creds
        --set env=qa
        --set replicaCount=2
        --wait --timeout 5m --atomic
  needs:
    - test-dev
  rules:
    - if: '$CI_COMMIT_BRANCH == "main"'

# ── STAGE 4: Integration Tests QA ───────────────────────────────
test-qa:
  stage: test-qa
  image: maven:3.9-eclipse-temurin-17
  script:
    # Run full integration test suite against QA environment
    - mvn verify -Pintegration-tests
        -Dtest.base.url=https://qa.myapp.company.com
        -DskipUnitTests=true
  artifacts:
    when: always
    reports:
      junit: target/failsafe-reports/TEST-*.xml
    paths:
      - target/failsafe-reports/
    expire_in: 1 week
  rules:
    - if: '$CI_COMMIT_BRANCH == "main"'

# ── STAGE 5: Deploy to STAGING ───────────────────────────────────
deploy-staging:
  stage: deploy-staging
  image: dtzar/helm-kubectl:latest
  environment:
    name: staging
    url: https://staging.myapp.company.com
  before_script:
    - echo "$KUBE_CONFIG_STAGING" | base64 -d > ~/.kube/config
  script:
    - helm upgrade --install my-app $HELM_CHART_PATH
        --namespace $KUBE_NAMESPACE_STAGING
        --create-namespace
        --set image.repository=$ARTIFACTORY_URL/docker-staging-local/$IMAGE_NAME
        --set image.tag=$IMAGE_TAG
        --set env=staging
        --set replicaCount=3
        --wait --timeout 10m --atomic
  needs:
    - test-qa
  rules:
    - if: '$CI_COMMIT_BRANCH == "main"'

# ── STAGE 6: Staging Tests ───────────────────────────────────────
test-staging:
  stage: test-staging
  image: maven:3.9-eclipse-temurin-17
  script:
    # Performance + integration tests on staging
    - mvn verify -Pstaging-tests
        -Dtest.base.url=https://staging.myapp.company.com
    # Load test (optional)
    - echo "Run k6 / JMeter load tests here"
  artifacts:
    when: always
    reports:
      junit: target/failsafe-reports/TEST-*.xml
  rules:
    - if: '$CI_COMMIT_BRANCH == "main"'

# ── STAGE 7: Manual Approval Gate ───────────────────────────────
approve-production:
  stage: approve-production
  image: alpine:latest
  script:
    - echo "Awaiting manual approval for production deployment"
    - echo "Image: $ARTIFACTORY_URL/docker-staging-local/$IMAGE_NAME:$IMAGE_TAG"
  environment:
    name: production-approval
  when: manual                              # BLOCKS until a human clicks approve
  allow_failure: false
  needs:
    - test-staging
  rules:
    - if: '$CI_COMMIT_BRANCH == "main"'

# ── STAGE 8: Deploy to PRODUCTION ───────────────────────────────
deploy-production:
  stage: deploy-production
  image: dtzar/helm-kubectl:latest
  environment:
    name: production
    url: https://myapp.company.com
    on_stop: rollback-production            # linked rollback job
  before_script:
    - echo "$KUBE_CONFIG_PROD" | base64 -d > ~/.kube/config
    # Promote image to release repo in Artifactory
    - |
      curl -u $ARTIFACTORY_USER:$ARTIFACTORY_PASSWORD \
        -X POST "$ARTIFACTORY_URL/artifactory/api/docker/docker-staging-local/v2/promote" \
        -H "Content-Type: application/json" \
        -d "{\"targetRepo\":\"docker-release-local\",
             \"dockerRepository\":\"$IMAGE_NAME\",
             \"tag\":\"$IMAGE_TAG\",
             \"copy\":true}"
  script:
    # Blue/Green: deploy to inactive slot
    - helm upgrade --install my-app-green $HELM_CHART_PATH
        --namespace $KUBE_NAMESPACE_PROD
        --set image.repository=$ARTIFACTORY_URL/docker-release-local/$IMAGE_NAME
        --set image.tag=$IMAGE_TAG
        --set env=production
        --set replicaCount=5
        --set service.slot=green
        --wait --timeout 10m --atomic

    # Switch traffic to green
    - kubectl patch service my-app-lb
        -n $KUBE_NAMESPACE_PROD
        -p '{"spec":{"selector":{"slot":"green"}}}'

    - echo "Production deployment complete: $IMAGE_NAME:$IMAGE_TAG"
  needs:
    - approve-production
  rules:
    - if: '$CI_COMMIT_BRANCH == "main"'

# ── STAGE 9: Production Verification ────────────────────────────
verify-production:
  stage: verify-production
  image: curlimages/curl:latest
  script:
    - sleep 60
    - |
      for i in 1 2 3 4 5; do
        RESPONSE=$(curl -s -o /dev/null -w "%{http_code}" \
          https://myapp.company.com/actuator/health)
        if [ "$RESPONSE" = "200" ]; then
          echo "Production health check PASSED (attempt $i)"
          exit 0
        fi
        echo "Attempt $i failed (HTTP $RESPONSE), retrying in 30s..."
        sleep 30
      done
      echo "Production health check FAILED after 5 attempts"
      exit 1
  needs:
    - deploy-production
  rules:
    - if: '$CI_COMMIT_BRANCH == "main"'

# ── ROLLBACK JOB (linked to production environment) ─────────────
rollback-production:
  stage: deploy-production
  image: dtzar/helm-kubectl:latest
  environment:
    name: production
    action: stop
  before_script:
    - echo "$KUBE_CONFIG_PROD" | base64 -d > ~/.kube/config
  script:
    # Switch traffic back to blue (previous stable)
    - kubectl patch service my-app-lb
        -n $KUBE_NAMESPACE_PROD
        -p '{"spec":{"selector":{"slot":"blue"}}}'
    - helm rollback my-app-green --namespace $KUBE_NAMESPACE_PROD
    - echo "PRODUCTION ROLLED BACK"
  when: manual
  rules:
    - if: '$CI_COMMIT_BRANCH == "main"'
```

---

## 4. Helm Chart Structure

```
helm/
└── my-app/
    ├── Chart.yaml           ← Chart metadata, version
    ├── values.yaml          ← Default values
    ├── values-dev.yaml      ← Dev overrides
    ├── values-staging.yaml  ← Staging overrides
    ├── values-prod.yaml     ← Production overrides
    └── templates/
        ├── deployment.yaml  ← Pod spec
        ├── service.yaml     ← Service / LB
        ├── ingress.yaml     ← Ingress / route
        ├── hpa.yaml         ← Horizontal Pod Autoscaler
        ├── configmap.yaml   ← App config
        └── secret.yaml      ← Secrets reference (Vault)
```

### `values.yaml` (key section)
```yaml
image:
  repository: company.jfrog.io/docker-dev-local/my-app
  tag: latest                      # overridden by --set image.tag=$IMAGE_TAG
  pullPolicy: Always
  pullSecret: artifactory-creds

replicaCount: 2

resources:
  requests:
    cpu: "250m"
    memory: "512Mi"
  limits:
    cpu: "1000m"
    memory: "1Gi"

readinessProbe:
  httpGet:
    path: /actuator/health/readiness
    port: 8080
  initialDelaySeconds: 30
  periodSeconds: 10

livenessProbe:
  httpGet:
    path: /actuator/health/liveness
    port: 8080
  initialDelaySeconds: 60
  periodSeconds: 15
```

---

## 5. GitOps Alternative — ArgoCD

For teams using GitOps, ArgoCD replaces the Helm deploy stages in `.gitlab-ci.yml`:

```mermaid
flowchart TD
    A[CI pushes image to Artifactory] --> B[CI updates image tag in Git repo]
    B --> C[values.yaml or kustomization.yaml updated]
    C --> D[Git commit pushed to config repo]
    D --> E[ArgoCD detects Git change]
    E --> F[ArgoCD syncs cluster state]
    F --> G[kubectl apply generated manifests]
    G --> H[Pods rolling update with new image]
    H --> I[ArgoCD health check]
    I -->|Healthy| DONE[✅ Deployed]
    I -->|Degraded| ROLLBACK[ArgoCD auto-rollback]
```

### CI step to update image tag in GitOps repo
```yaml
update-gitops-repo:
  stage: artifactory-publish
  image: alpine/git:latest
  script:
    # Clone the GitOps/config repo
    - git clone https://gitlab-ci-token:$CI_JOB_TOKEN@gitlab.com/org/k8s-config.git
    - cd k8s-config

    # Update image tag in values file
    - sed -i "s|tag:.*|tag: $IMAGE_TAG|g" apps/my-app/values.yaml

    # Commit and push — ArgoCD picks this up automatically
    - git config user.email "ci@company.com"
    - git config user.name "GitLab CI"
    - git add apps/my-app/values.yaml
    - git commit -m "chore: update my-app image to $IMAGE_TAG [ci skip]"
    - git push
  rules:
    - if: '$CI_COMMIT_BRANCH == "main"'
```

---

## 6. Kubernetes Deployment Under the Hood

When `helm upgrade` runs, this is what Kubernetes does:

```
helm upgrade --install my-app ...
    ↓
Kubernetes API Server receives new Deployment spec
    ↓
Deployment Controller detects image tag change
    ↓
Rolling Update begins:
  ├── New Pod created with new image tag
  ├── Kubernetes pulls image from Artifactory
  ├── readinessProbe checked (app must be ready)
  ├── If ready: old Pod terminated
  └── Repeat until all replicas updated
    ↓
Service routes traffic to only READY pods
    ↓
Old pods cleaned up (terminationGracePeriodSeconds respected)
```

### Rolling Update Strategy
```yaml
# In deployment.yaml template
strategy:
  type: RollingUpdate
  rollingUpdate:
    maxSurge: 1          # 1 extra pod above desired count during update
    maxUnavailable: 0    # never take a pod down before new one is ready
```

---

## 7. Secrets Management in CD

```mermaid
flowchart LR
    A[HashiCorp Vault / AWS Secrets Manager] -->|inject at runtime| B[Pod Env Vars]
    C[Kubernetes Secrets] -->|mounted as env/volume| B
    D[GitLab CI Variables] -->|KUBE_CONFIG, registry creds| E[CI Runner]
    F[Artifactory] -->|image pull secret| G[Kubelet pulls image]
```

### External Secrets Operator pattern
```yaml
# ExternalSecret — pulls from Vault automatically
apiVersion: external-secrets.io/v1beta1
kind: ExternalSecret
metadata:
  name: my-app-secrets
  namespace: production
spec:
  refreshInterval: 1h
  secretStoreRef:
    name: vault-backend
    kind: ClusterSecretStore
  target:
    name: my-app-secret
  data:
    - secretKey: DB_PASSWORD
      remoteRef:
        key: secret/production/my-app
        property: db_password
```

**Never store secrets in:**
- Helm values files committed to Git
- Docker image layers
- Environment variables in `.gitlab-ci.yml` (use masked CI variables)

---

## 8. Deployment Strategies Explained

### Blue/Green (Zero Downtime)
```
Before deploy:
  BLUE  (v1.3.0) ← Live traffic (100%)
  GREEN (empty)

During deploy:
  BLUE  (v1.3.0) ← Live traffic (100%)
  GREEN (v1.4.0) ← Deploying + health checks

After health check passes:
  BLUE  (v1.3.0) ← Standby (instant rollback available)
  GREEN (v1.4.0) ← Live traffic (100%)
```

### Canary (Gradual Rollout)
```
Step 1:  v1.4.0 gets  5% traffic, v1.3.0 gets 95%
Step 2:  v1.4.0 gets 25% traffic, v1.3.0 gets 75%  → monitor errors
Step 3:  v1.4.0 gets 50% traffic, v1.3.0 gets 50%  → monitor errors
Step 4:  v1.4.0 gets 100% traffic → v1.3.0 scaled to 0
```

### Rolling Update (default Kubernetes)
```
Pods: [v1.3, v1.3, v1.3, v1.3, v1.3]
Step: [v1.4, v1.3, v1.3, v1.3, v1.3]
Step: [v1.4, v1.4, v1.3, v1.3, v1.3]
Step: [v1.4, v1.4, v1.4, v1.3, v1.3]
Done: [v1.4, v1.4, v1.4, v1.4, v1.4]
```

---

## 9. Post-Deployment Verification

```yaml
# Automated post-deploy tests
verify-production:
  script:
    # 1. Health endpoint
    - curl -f https://myapp.company.com/actuator/health

    # 2. Critical API endpoints
    - curl -f https://myapp.company.com/api/v1/status

    # 3. Check Kubernetes pod status
    - kubectl get pods -n production -l app=my-app
    - kubectl rollout status deployment/my-app -n production

    # 4. Check logs for startup errors
    - kubectl logs -n production -l app=my-app --tail=100 | grep -i error || true

    # 5. Verify correct image is running
    - |
      RUNNING_TAG=$(kubectl get deployment my-app -n production \
        -o jsonpath='{.spec.template.spec.containers[0].image}' \
        | cut -d: -f2)
      if [ "$RUNNING_TAG" != "$IMAGE_TAG" ]; then
        echo "Wrong image running! Expected $IMAGE_TAG got $RUNNING_TAG"
        exit 1
      fi
```

---

## 10. Full End-to-End Pipeline Summary

```mermaid
flowchart TD
    subgraph CI ["CI Pipeline (Automated)"]
        CI1[Build] --> CI2[Unit Tests + JaCoCo]
        CI2 --> CI3[SonarQube Analysis]
        CI3 --> CI4{Quality Gate}
        CI4 -->|Pass| CI5[Docker Build]
        CI5 --> CI6[Trivy Scan]
        CI6 --> CI7[Push to Artifactory]
        CI7 --> CI8[Build Info Published]
    end

    subgraph CD ["CD Pipeline"]
        CD1[Deploy DEV] --> CD2[Smoke Test DEV]
        CD2 --> CD3[Deploy QA]
        CD3 --> CD4[Integration Tests]
        CD4 --> CD5[Deploy Staging]
        CD5 --> CD6[Staging Tests]
        CD6 --> CD7{Manual Approval}
        CD7 -->|Approved| CD8[Promote Image\nto release repo]
        CD8 --> CD9[Deploy Production\nBlue/Green]
        CD9 --> CD10[Production Verify]
        CD10 --> LIVE[✅ LIVE]
    end

    CI8 --> CD1
    CD4 -->|Fail| R1[Rollback DEV]
    CD6 -->|Fail| R2[Rollback Staging]
    CD10 -->|Fail| R3[Auto Rollback Prod]
```

### Complete Stage Reference Table

| # | Stage | Environment | Tool | Trigger | Blocks On |
|---|---|---|---|---|---|
| 1 | Build | — | Maven/Gradle | Auto | Compile error |
| 2 | Unit Test | — | JUnit + JaCoCo | Auto | Test failure |
| 3 | SonarQube | — | sonar-scanner | Auto | — |
| 4 | Quality Gate | — | SonarQube API | Auto | Gate fails |
| 5 | Docker Build | — | Docker | Auto | Build error |
| 6 | Image Scan | — | Trivy | Auto | CRITICAL CVE |
| 7 | Artifactory Push | — | Docker + JFrog CLI | Auto | Push failure |
| 8 | Deploy DEV | dev namespace | Helm + kubectl | Auto | Deploy failure |
| 9 | Smoke Test DEV | dev | curl | Auto | HTTP != 200 |
| 10 | Deploy QA | qa namespace | Helm + kubectl | Auto | Deploy failure |
| 11 | Integration Tests | qa | JUnit/Postman | Auto | Test failure |
| 12 | Deploy Staging | staging namespace | Helm + kubectl | Auto | Deploy failure |
| 13 | Staging Tests | staging | JUnit/k6 | Auto | Test failure |
| 14 | Manual Approval | — | GitLab UI | **Human click** | Rejected |
| 15 | Promote Image | Artifactory | JFrog CLI | Auto | Promo failure |
| 16 | Deploy Production | production namespace | Helm Blue/Green | Auto | Deploy failure |
| 17 | Production Verify | production | curl + kubectl | Auto | Health fail → rollback |

---

## 11. Mandatory CD Checklist

```
KUBERNETES CLUSTER
  [ ] Separate namespaces per environment (dev / qa / staging / production)
  [ ] KUBE_CONFIG per environment stored as masked GitLab CI variable
  [ ] Artifactory image pull secret created in each namespace
  [ ] Resource requests and limits defined in Helm values
  [ ] readinessProbe and livenessProbe configured in deployment

HELM
  [ ] Helm chart exists with environment-specific values files
  [ ] --atomic flag used (auto-rollback on failure)
  [ ] --wait flag used (blocks until pods ready)
  [ ] Chart version bumped on changes
  [ ] Helm history retained (for rollback: helm rollback)

DEPLOYMENT STRATEGY
  [ ] Rolling update maxUnavailable: 0 (zero downtime)
  [ ] Blue/Green or Canary configured for production
  [ ] Rollback job defined and tested
  [ ] terminationGracePeriodSeconds set appropriately

SECRETS
  [ ] No secrets in Git (use Vault / K8s Secrets / External Secrets Operator)
  [ ] Image pull secret created per namespace
  [ ] Database credentials injected at runtime (not baked into image)
  [ ] TLS certificates managed (cert-manager or Vault)

PROMOTION GATES
  [ ] DEV deploy only on main branch commits
  [ ] PRODUCTION deploy requires manual approval
  [ ] Image promoted in Artifactory before production deploy
  [ ] Staging tests must pass before approval gate is offered

POST-DEPLOY
  [ ] Health check endpoint exists (/actuator/health or /healthz)
  [ ] Smoke tests run after every deploy
  [ ] Monitoring / alerting configured (Prometheus + Grafana or Datadog)
  [ ] Log aggregation in place (ELK / Loki / Splunk)
  [ ] Rollback procedure documented and tested
  [ ] Runbook linked in GitLab environment page
```

---

> **Golden Rule:** Production never pulls directly from CI. Always promote through: `docker-dev-local → docker-staging-local → docker-release-local`. Production should only ever run images from `docker-release-local`.
