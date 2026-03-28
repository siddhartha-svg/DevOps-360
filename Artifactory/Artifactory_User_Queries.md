# Artifactory User Queries — Complete Troubleshooting Guide

> **Author:** Rajagopal, Vijayakumar  
> **Last Updated:** Feb 22, 2025  
> **Read Time:** ~6 minutes

---

## Table of Contents

1. [HTTP Status Code Issues (General)](#1-http-status-code-issues-general)
2. [HTTP Status Code Issues in NPM](#2-http-status-code-issues-in-npm)
3. [HTTP Status Code Issues in Maven](#3-http-status-code-issues-in-maven)
4. [Docker Error Response Codes](#4-docker-error-response-codes)
5. [Access Issues](#5-access-issues)
6. [Code Promotion & Replication](#6-code-promotion--replication)
7. [Binary Version Upgrade](#7-binary-version-upgrade)
8. [Spring 5 Support](#8-spring-5-support)

---

## 1. HTTP Status Code Issues (General)

### 401 — Unauthorized

- Verify you have the correct **permissions** on the target repository for the action you're performing (deploy/push).
- 401 is caused by **missing credentials** or an **expired token**.
- Refer to the respective Package type Confluence pages for steps to add credentials or regenerate a token.
- For **Docker**, perform a fresh login:
  ```bash
  docker login gyqv-docker-np.oneartifactoryci.horizon.com
  ```
- For access issues, reach out to the **repo admin** and refer to **OneArtifactory FAQ #11**.

---

### 403 — Forbidden

- Credentials exist but **do not have sufficient privileges** on the repository.
- Reach out to the **repo admin** to request access — refer to **OneArtifactory FAQ #11** to find the admins.
- For Docker specifically:
  > `failed with status code [manifests latest]: 403 Forbidden`  
  This means insufficient privileges on the repository. Contact the repo admin.

---

### 404 — File or Folder Not Found

- **Remove any proxy** configuration that may be redirecting your request incorrectly.
- Verify the artifact exists by **searching in the OneArtifactory CI UI**.
- For **Docker 404**: The image tag does not exist — it was either never published or was deleted.  
  Use the **restore from trash** feature to recover deleted artifacts (refer to OneArtifactory FAQ **Q21**).

---

### 503 — Service Unavailable

503 errors are typically caused by one of two things:

#### Firewall Block
Validate connectivity from your server/slave node:
```bash
telnet oneartifactoryci.horizon.com 443
```
If unable to connect → raise a firewall request:  
🔗 https://firewallrequests.nss.vzwnet.com/far_ui/myrequests/requests

#### Proxy Enabled
Check if proxy is active on your server:
```bash
env | grep proxy
env | grep PROXY
```
If proxy is enabled, disable it:
```bash
unset http_proxy https_proxy no_proxy NO_PROXY
```

---

## 2. HTTP Status Code Issues in NPM

| Error Code | Root Cause | How to Diagnose | Fix |
|------------|-----------|-----------------|-----|
| **401** | No authentication or expired token | `npm config ls` | Regenerate `.npmrc` using "Set me up" in Artifactory UI → [NPM Guide](https://oneconfluence.horizon.com/display/DevOpsWiki/npm) |
| **403** | No access to the package in that repo | Search for package in Artifactory UI | Contact repo admin — refer [OneArtifactory FAQ #11](https://oneconfluence.horizon.com/display/DevOpsWiki/OneArtifactory+FAQ) |
| **404** | Package not available in Artifactory | Search in Artifactory UI | Request Artifactory team to mirror the source or publish to your own repo |
| **404*** | Incorrect `package.json` metadata | Check `npm info` tab in UI | Fix `package.json` and republish the package |
| **404*** | Rare bug with virtual repo as registry | Search in Artifactory UI | Contact repo admin — refer [OneArtifactory FAQ #11](https://oneconfluence.horizon.com/display/DevOpsWiki/OneArtifactory+FAQ) |
| **503** | Proxy enabled (env vars or npm config) | `env \| grep proxy` / `npm config ls` | `unset http_proxy https_proxy NO_PROXY` then `npm config rm https_proxy; npm config rm proxy` |
| **409** | Incorrect registry URL (missing `/api/npm/<repo_name>`) | `npm config ls` | Regenerate `.npmrc` with correct URL using "Set me up" → [npm Guide](https://oneconfluence.horizon.com/display/DevOpsWiki/npm) |

---

## 3. HTTP Status Code Issues in Maven

> For full Maven setup instructions, refer to the [Maven Confluence Page](https://oneconfluence.horizon.com/display/DevOpsWiki/Maven).

| Error Code | Root Cause | How to Diagnose | Fix |
|------------|-----------|-----------------|-----|
| **401** | No `<server>` entry in `settings.xml` for a `<repository>` | Check that every `<repository>` in `settings.xml`/`pom.xml` has a matching `<server>` block | Follow steps to generate correct `settings.xml` from Artifactory UI |
| **403** | No access to the file/repo in virtual repo | Login with the ID from `settings.xml` and search in Artifactory UI | Contact repo admin — refer OneArtifactory FAQ #11 |
| **404** | Package not in Artifactory or repo not declared in `settings.xml` | Search in Artifactory UI | Post in `#artifactorysupport` Slack channel — team will mirror the source or add the repo to your virtual repo |
| **503** | Proxy enabled in env or `settings.xml` | `env \| grep proxy` / check `<proxies>` in `settings.xml` | `unset http_proxy https_proxy NO_PROXY` and comment/delete `<proxies>` block from `settings.xml` |
| **409** | Incorrect `<repository>` URL in `settings.xml` | Check all `<url>` declarations in `settings.xml` | Correct format: `<url>https://oneartifactoryci.horizon.com/artifactory/SAMPLE_REPO/</url>` |

---

## 4. Docker Error Response Codes

### 401 — Unauthorized
**Full Error:**
```
failed to resolve reference "SAMPLE_REPO.oneartifactoryci.horizon.com/dmdaf-flink:de579327":
failed to authorize: failed to fetch oauth token: unexpected status: 401 Unauthorized
```
**Cause:** Docker login not performed, or password changed after login.

**Fix:**
```bash
docker logout SAMPLE_REPO.oneartifactoryci.horizon.com
docker login SAMPLE_REPO.oneartifactoryci.horizon.com
```
Also perform a manual `docker pull` from the build server to validate credentials.

---

### 403 — Forbidden
**Full Error:**
```
#3 ERROR: pulling from host SAMPLE_REPO.oneartifactoryci.horizon.com 
failed with status code [manifests latest]: 403 Forbidden
```
**Cause:** Stored credentials do not have access or have expired.

**Fix:**
- Login with your credentials and search in Artifactory UI.
- Perform a manual `docker pull` from the build server.
- Contact repo admin — refer **OneArtifactory FAQ #11**.

---

### 404 — Image Not Found
**Cause:** The image tag does not exist in Artifactory — either never published or deleted.

**Fix:**
- Search for the image in Artifactory UI.
- Use the **restore from trash** job — refer **OneArtifactory FAQ Q21**.
- Post in `#artifactorysupport` for engineer assistance.

---

### 503 — Service Unavailable
**Cause:** Proxy enabled at system level or in Docker config.

**Diagnose:**
```bash
env | grep proxy
docker pull ubuntu   # test connectivity via DockerHub
```

**Fix:**
```bash
unset http_proxy https_proxy NO_PROXY
```

---

## 5. Access Issues

### Artifactory CI or Artifactory Prod
Test connectivity from the instance where you are accessing Artifactory:
```bash
telnet oneartifactoryprod.horizon.com 443
telnet oneartifactoryci.horizon.com 443
```
If not connected → raise a firewall request and refer [OneArtifactory FAQ #6](https://oneconfluence.horizon.com/display/DevOpsWiki/OneArtifactory+FAQ).

---

### Onboarding Portal
- If you can access Artifactory but **not** the Onboarding Portal → create a **TOOLS ticket in Jira**.
- Refer to **OneArtifactory FAQ Q2** for guidance.

---

### Repository Access
- Contact the repo admin — refer [OneArtifactory FAQ #11](https://oneconfluence.horizon.com/display/DevOpsWiki/OneArtifactory+FAQ) to find admins.
- **If the repo has no admins** (all have left the org):
  1. Email the **Application Custodian** (get details from VAST), CC `oneartifactory-support`.
  2. Create a **TOOLS ticket in Jira**.
  3. Artifactory admin will grant repo admin access to **one user** — that user then manages permissions going forward.

---

## 6. Code Promotion & Replication

### Data Replication Not Happening from Artifactory CI to Prod

> **Important:** `oneartifactoryprod` is **READ ONLY** — it is meant exclusively for production deployments. Direct builds and deploys are **RESTRICTED**.

**How replication works:**
- Artifactory admins create a `-prod` repository for every local repository.
- Data flows: **Artifactory CI** → (via `-prod` repos) → **Artifactory Prod**
- Replication only happens through `-prod` repos — make sure you're deploying to the `-prod` repo on CI.

**Can't see the `-prod` repo?**  
Access is restricted by default. Create a **TOOLS ticket in Jira** to request access.

For more details, see the **OneArtifactory CI & Prod** documentation.

---

## 7. Binary Version Upgrade

### How do I find the latest binary version in Artifactory to fix a vulnerability?

Refer to the **Artifactory Security Maven Queries** documentation for steps to identify the latest patched version of a binary available in Artifactory.

---

## 8. Spring 5 Support

- Refer to the **Spring 5 Support FAQ** for detailed guidance.
- To consume **Spring 5 (CapGemini) packages**, refer to the **Base Virtual Repo** documentation.

---

## Quick Reference — Who to Contact

| Situation | Action |
|-----------|--------|
| Access to a repo | Contact **Repo Admin** (find via FAQ #11) |
| Repo has no admins | Email App Custodian (VAST) + CC `oneartifactory-support` + TOOLS Jira ticket |
| Firewall/connectivity issue | Raise request at https://firewallrequests.nss.vzwnet.com |
| Onboarding Portal issue | TOOLS Jira ticket |
| Package not in Artifactory | Post in `#artifactorysupport` Slack channel |
| Deleted Docker image | Restore from trash — FAQ Q21 |

---

> **OneArtifactory FAQ:** https://oneconfluence.horizon.com/display/DevOpsWiki/OneArtifactory+FAQ
