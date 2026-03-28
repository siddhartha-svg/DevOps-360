# OneArtifactory CI & Prod — Complete Guide

> **Author:** May, Bryan Robert  
> **Last Updated:** May 29, 2025  
> **Read Time:** ~4 minutes

---

## Table of Contents

1. [Important Announcement — Bosun 7.0](#1-important-announcement--bosun-70)
2. [Overview](#2-overview)
3. [Instance URLs & Connectivity](#3-instance-urls--connectivity)
4. [Code Promotion — Non-Docker Repositories](#4-code-promotion--non-docker-repositories)
5. [Code Promotion — Docker Repositories](#5-code-promotion--docker-repositories)
6. [Portfolio Responsibilities](#6-portfolio-responsibilities)
7. [Best Practices](#7-best-practices)
8. [Generic Repo Type — Restructuring Guide](#8-generic-repo-type--restructuring-guide)

---

## 1. Important Announcement — Bosun 7.0

> Cloud Security has implemented a new rule in **Bosun 7.0** that restricts Docker repo access in Artifactory.

| Cluster Type | Allowed Artifactory Instance |
|---|---|
| **Production** clusters (EKS / K8s) | `oneartifactoryProd` **only** |
| **Non-Prod** clusters | `oneartifactoryCI` **only** |

**Impact:**
- All **non-prod builds and deployments** → use `oneartifactoryCI`
- **Production deployments** → use `oneartifactoryProd`

---

## 2. Overview

Artifactory is more than just a Binary Repository Manager — it is part of your portfolio's **binary lifecycle** and **container runtime lifecycle**. Its availability is **business critical**.

A **multi-layer approach** has been introduced to help portfolio teams:
- Segregate **Prod** and **Non-Prod** workloads
- Apply granular **access control** based on team roles and responsibilities

---

## 3. Instance URLs & Connectivity

| Environment | URL | Purpose |
|---|---|---|
| **Production** | https://oneartifactoryprod.horizon.com | Production deployments only. Direct builds are **RESTRICTED**. |
| **Dev / CI** | https://oneartifactoryci.horizon.com | Build environment for all portfolio teams. Promote releases from CI → Prod via code promotion (`-prod` repo). |

---

### Verify Connectivity

Run the following from your server to test connectivity to the CI instance:

```bash
telnet oneartifactoryci.horizon.com 443
```

#### Troubleshooting Connectivity

```
❌ Cannot connect?
```

1. **Check your IP** — Verify your IP is in the approved Subnet range.
   - If **not** in the subnet → raise a TOOLS ticket in Jira and report in `#artifactorysupport`.
   - If **in the subnet** → raise a **Firewall request**.

#### Known CI IP Addresses

| Node | IP Addresses |
|---|---|
| CI West — Active (Green) | `144.70.113.107` & `144.70.119.144` |
| CI East — Blue | `144.70.103.54` & `144.70.98.150` |
| CI West — Blue | `144.70.114.22` & `144.70.119.77` |

---

## 4. Code Promotion — Non-Docker Repositories

### How it works (Option 1 — Default)

```
Artifactory CI
├── OS4V_LANG-virtual
│   ├── OS4V_LANG  (Non-Prod repo)
│   └── Maven1-All-Virtual
│       └── repo1, spring-milestones, maven-oracle-com-remote, etc.
└── OS4V_LANG-prod  ──────────────────────────────────────────────►  Artifactory Prod
                         (Prod deploy bundle auto-replicated)             └── OS4V_LANG-prod (Read Only)
```

- App team deploys their **production release bundle** to the `-prod` repo in **Artifactory CI**.
- It is **automatically replicated** to the `-prod` repo in **Artifactory Prod**.
- Artifactory Prod is **Read Only** — no direct builds or deployments are allowed.

---

### How it works (Option 2 — Based on App Team Request)

```
Artifactory CI
├── OS4V_LANG-virtual
│   ├── OS4V_LANG  (Non-Prod repo)
│   └── Maven1-All-Virtual
│       └── repo1, spring-milestones, maven-oracle-com-remote, etc.
└── OS4V_LANG-prod  ──────────────────────────────────────────────►  Artifactory Prod
                         (Prod deploy bundle auto-replicated)             └── OS4V_LANG (Non-Prod repo, Read Only)
```

### Process to opt into Option 2

1. The App team contacts the Artifactory team to request this method.
2. The App team **clears all data** from their non-production repository in `oneartifactoryprod` (it's already present in CI).
3. The App team uploads the production deployment release bundle or image to the `-prod` repository in CI — it will be **automatically synchronized** to either the non-production or `-prod` repository in `oneartifactoryprod` depending on the selected option.

---

## 5. Code Promotion — Docker Repositories

```
Artifactory CI                                           Artifactory Prod (Read Only)
├── b6vv-docker-np   (non-prod builds)                  └── b6vv-docker-prod
├── b6vv-docker-dev  (dev builds)                             ▲
└── b6vv-docker-prod ─────────────────────────────────────────┘
        (Prod deploy image auto-replicated from CI to Prod)
```

**Workflow:**
1. **Build & non-prod deploys** → use `b6vv-docker-np` in Artifactory CI.
2. **Promote** the prod-ready image from `b6vv-docker-np` → `b6vv-docker-prod` in Artifactory CI.
3. The image in `b6vv-docker-prod` is **automatically replicated** to `b6vv-docker-prod` in Artifactory Prod.
4. **Production clusters** pull images from your `-prod` repo in Artifactory Prod.

> Environment segregation is enforced by Cloud Security (Bosun 7): Non-Prod clusters → AF CI only. Prod clusters → AF Prod only.

---

## 6. Portfolio Responsibilities

### 1. Update URLs in All Build Jobs & Scripts

Replace `oneartifactoryprod.horizon.com` with `oneartifactoryci.horizon.com` in **all Jenkins jobs and scripts**.

```
Before: oneartifactoryprod.horizon.com
After:  oneartifactoryci.horizon.com
```

---

### 2. Update ServerId in Jenkins Pipeline Jobs

| Artifactory URL | ServerId |
|---|---|
| `oneartifactoryprod.horizon.com` | `oneartifactoryprod` |
| `oneartifactoryci.horizon.com` | `oneartifactoryci` |

---

### 3. Use the Base Virtual Repo (Not Local Repo Directly)

Every repo has a `-virtual` variant. **All build jobs, pipelines, and config files must use `<reponame>-virtual`**.

```
Local repo:   b6vv_cxp
Virtual repo: b6vv_cxp-virtual   ← use this
```

The virtual repo automatically includes:
- All remote repos for the appropriate package type  
  *(e.g., Maven virtual includes repo1, jcenter, etc.)*
- Common virtual repos (`libs-release`, `libs-snapshot`, etc.)

---

### 4. Use Common Virtual Repo for Shared Repositories

Do **not** access common repos directly. Always route through the **Common Virtual Repo**.

---

### 5. Artifact / Image Promotion from AF CI → AF Prod

- A `-prod` repo was created for every local repo during migration.  
  Example: `b6vv_cxp` → `b6vv_cxp-prod`
- Move your production release bundles to the `-prod` repo in CI → they will **auto-replicate** to `-prod` in `oneartifactoryprod`.
- **Option B:** To use your existing local repo (e.g., `b6vv_cxp`) for prod deployment in `oneartifactoryprod`:
  1. Delete all data from that local repo in CI (it was already migrated).
  2. Artifactory team will then enable replication from `-prod` in CI → your local repo in `oneartifactoryprod`.

---

### 6. Docker Repo Workflow

| Step | Action |
|---|---|
| 1 | Build image and deploy to non-prod using `b6vv-docker-np` in AF CI |
| 2 | Move the prod-ready image: `b6vv-docker-np` → `b6vv-docker-prod` in AF CI |
| 3 | Image auto-replicates to `b6vv-docker-prod` in AF Prod |
| 4 | Production clusters pull from `-prod` repo in AF Prod |

---

### 7. Reduce Blast Radius — Split Large Repos

- Split large repositories into **smaller, scoped repos**.
- **Clean up artifacts periodically** to manage repo size.

---

### 8. Refine Permissions Based on Roles

| Instance | What to Manage |
|---|---|
| `oneartifactoryci.horizon.com` | All **Non-Prod** access |
| `oneartifactoryprod.horizon.com` | All **Prod** access |

- Create a **separate ADOM group for CI** — do not reuse prod ADOM groups in CI environments.
- **Publish Build Info** for granular traceability.
- For migration queries → reach out in the `#blm-migration-support` Slack channel.

---

## 7. Best Practices

| # | Best Practice |
|---|---|
| 1 | Keep the AF URL **configurable** in your pipelines to adapt quickly to changes |
| 2 | **Never store credentials** in Artifactory — use **CyberArk** |
| 3 | Use a **dedicated service account** for every Artifactory layer for efficient permission management |
| 4 | **Don't use common repos** (`libs-release`, `plugin-release`, etc.) directly — use virtual repos |
| 5 | **Don't use** `Anonymous` or `Jenkins` user accounts — these are internal accounts and may be removed at any time for security reasons |

---

## 8. Generic Repo Type — Restructuring Guide

Generic repo types need to be restructured to fit the new multi-layer architecture.

```
Is your Generic repo used for build purposes?
│
├── NO  → No changes needed. Continue using as-is.
│
└── YES → Action Required:
          1. Create a new repo with the APPROPRIATE PACKAGE TYPE
             (Maven, npm, Docker, etc.)
          2. Migrate the data to the new typed repo
          3. This lets you leverage:
             - The new architecture
             - Associated virtual repos
             - Remote repo aggregation
             - Proper package metadata and search
```

> Typed repos give you full access to Artifactory's package intelligence, security scanning, and replication features — generic repos miss out on these capabilities.

---

## Quick Reference

| Task | Action |
|---|---|
| Connectivity issue | `telnet oneartifactoryci.horizon.com 443` → check subnet → raise firewall request |
| Can't see `-prod` repo | Create a TOOLS ticket in Jira |
| Build failures after URL change | Update to `oneartifactoryci.horizon.com` + use `-virtual` repos |
| Promote image to prod | Move image to `-prod` repo in AF CI → auto-replicates to AF Prod |
| Access issues | `#artifactorysupport` Slack channel |
| Migration queries | `#blm-migration-support` Slack channel |

---

> **Artifactory CI:** https://oneartifactoryci.horizon.com  
> **Artifactory Prod:** https://oneartifactoryprod.horizon.com
