# Artifactory Repository Types - Simple Guide

## What is Artifactory?
Artifactory is a tool that **stores and manages software packages/artifacts** (like JAR files, Docker images, npm packages, etc.) used during software development and deployment.

---

## The 4 Repository Types

### 1. Local Repository (Now Federated)
> Think of it as **your own storage shelf** at home.

- Stores **your team's own artifacts** (internal builds, releases, 3rd party files not available publicly).
- You can directly upload and download from it.
- **Access URL format:**
  ```
  https://<artifactory-host>/artifactory/<repo-name>/
  ```
- **Example:**
  ```
  https://oneartifactoryci.horizon.com/artifactory/ev6v-cxp-browsing-services-maven-dev/
  ```

---

### 2. Federated Repository ⭐ (Currently in Use)
> Think of it as **the same shelf, but synced across multiple warehouses globally**.

- Works exactly like a Local repository **but is replicated across multiple Artifactory instances/regions**.
- Uses **bi-directional replication** — changes in one region automatically sync to all other regions.
- Perfect for **active-active setups** where multiple teams/regions need the same artifacts.
- All local repositories have already been **migrated to Federated** repositories.

**Naming Standard:**
```
<VSAD>-<Project/Service>-<PackageType>-<Environment>
```
**Example:**
```
ev6v-cxp-browsing-services-maven-dev
│    │                   │     │
│    │                   │     └── Environment  : dev
│    │                   └──────── Package Type : maven
│    └──────────────────────────── Project/Service : cxp-browsing-services
└───────────────────────────────── VSAD : ev6v
```

---

### 3. Remote Repository
> Think of it as a **smart cache/proxy** — like a local copy of the internet.

- Acts as a **proxy** for external/public repositories (e.g., Maven Central, npm registry, ConanCenter).
- When you request an artifact:
  - First time → Artifactory **downloads it from the internet** and **caches it locally**.
  - Next time → Artifactory serves it **from the cache** (faster, no internet needed).
- Supports **HTTP and HTTPS** URLs only.

**Why use it?**
- Faster builds (cache avoids repeated downloads).
- Works even if the external source goes down temporarily.
- Central control over what external packages your team can use.

---

### 4. Virtual Repository
> Think of it as a **single front door to multiple warehouses**.

- **Combines** multiple Local/Federated + Remote repositories into **one single URL**.
- Developers don't need to know which underlying repo has the artifact — they just request it and Artifactory finds it.
- Admins can **control the search order**:
  1. Look in **Local/Federated** repos first
  2. Then check **Remote repo caches**
  3. Finally **go to the internet** if not found anywhere

**Why use it?**
- Simplifies developer experience — one URL for everything.
- Full control over what packages/versions are accessible.
- Easy to add/remove underlying repositories without changing developer configurations.

---

## Quick Comparison Table

| Feature | Federated | Remote | Virtual |
|---|---|---|---|
| Stores your own artifacts | ✅ Yes | ❌ No | ❌ No |
| Caches external artifacts | ❌ No | ✅ Yes | ❌ No |
| Aggregates other repos | ❌ No | ❌ No | ✅ Yes |
| Multi-region sync | ✅ Yes | ❌ No | ❌ No |
| Developer uses directly | ✅ Yes | ✅ Yes | ✅ Yes (recommended) |
| Single URL for everything | ❌ No | ❌ No | ✅ Yes |

---

## How They Work Together (Real-World Flow)

```
Developer requests a package
         │
         ▼
  [ Virtual Repository ]  ← Single URL for developers
         │
    ┌────┴────┐
    ▼         ▼
[Federated] [Remote]
(your own)  (cached from internet)
    │         │
    │         ▼
    │   [External Source]
    │   (Maven Central, npm, etc.)
    │
    ▼
[Replicated across all regions via Bi-directional sync]
```

---

## Key Takeaway

| Repo Type | Simple Definition |
|---|---|
| **Federated** | Your own artifact storage, synced globally |
| **Remote** | Smart cache for external/public packages |
| **Virtual** | One URL that searches across all repos |
