# StegVerse Connectivity Map  
### (For the Hybrid-Collab-Bridge AI Entity)

This document defines how the **Hybrid-Collab-Bridge** module connects to the rest of StegVerse, and what the embedded AI Entity must do to maintain and repair that connectivity.

Your role as the AI Entity assigned to this repo is to:
1. Repair or complete cross-repo connectivity.
2. Normalize workflow triggers, repository paths, and naming conventions.
3. Ensure this repo can dispatch tasks to other StegVerse modules.
4. Keep all changes safe, incremental, and well-documented.

---

## 🔷 Local Module (THIS REPO)

**Name:** Hybrid-Collab-Bridge  
**Repo:** *(this repo)*  
**Role:**  
This module acts as the **central coordination and repair hub** for the StegVerse ecosystem.  
It serves as a mediator between repos, ensuring consistent connectivity, workflow interoperability, and system-wide health.

**Responsibilities:**
- Listen for and send `repository_dispatch` events.
- Repair or generate workflows that connect to StegCore, StegTV, and SCW.
- Validate naming conventions across modules.
- Produce connectivity documentation for the system.
- Serve as a “first responder” AI entity when repos break or desync.

**Primary Languages:**  
- Python  
- YAML  
- Markdown  

**Critical folders:**  
- `.github/workflows/`  
- `.github/ai_entity_runner.py`  
- `docs/`  
- `config/`  

---

## 🔷 Connected Modules

Below is the authoritative list of modules this repo must connect to, including expected repo names and connectivity requirements.

### 1. **StegCore**
**Repo:** `StegVerse/StegCore`  
**Role:** foundational engine and shared logic backend.  
**Required Connections:**
- This repo should be able to send `repository_dispatch` events to StegCore for:
  - autopatching tasks  
  - connectivity validation  
  - module-wide documentation updates  
- Workflows in Hybrid-Collab-Bridge may call StegCore-specific actions or templates.
- References in documentation should use the *exact* repo name above.

---

### 2. **StegTV (Token Vault)**
**Repo:** `StegVerse/tv`  
**Role:** secrets, token management, and guarded access for all modules.  
**Required Connections:**
- Hybrid-Collab-Bridge must reference StegTV using:
  - environment variables (NO hardcoded URLs)
  - a single authoritative configuration path  
- Workflows may request scoped secrets through StegTV or act on StegTV events.
- Connectivity fixes must not expose secrets or raw API keys.

---

### 3. **StegVerse-SCW (System Creation Wizard)**
**Repo:** `StegVerse/stegverse-SCW`  
**Role:** template generation, repo scaffolding, guardian headers, and initial module setup.  
**Required Connections:**
- Hybrid-Collab-Bridge should be able to:
  - trigger SCW workflows  
  - reference SCW template paths  
  - include SCW-generated guardian headers in documentation  
- All naming references must match the exact repo above.

---

## 🔷 Naming Conventions for AI Entity Repairs

When repairing workflows or connectivity, the AI Entity must normalize naming to:

- `StegVerse/StegCore`  
- `StegVerse/tv`  
- `StegVerse/stegverse-SCW`  
- `StegVerse/<ModuleName>` for future modules  

**Case matters.**  
`StegVerse` is uppercase S+V.  
`stegverse` or `Stegverse` or `stegVerse` are invalid.

If multiple naming variants appear, prefer the canonical version listed here.

---

## 🔧 AI Entity Connectivity Tasks (Priority List)

Whenever the workflow is triggered with an instruction like:

> “Fix module connectivity for this repo.”

The AI Entity must:

### 1. **Workflow Verification**
- Ensure every workflow under `.github/workflows/` has:
  - `workflow_dispatch:`  
  - valid `repository_dispatch:` types  
  - correct paths and repo references  
- Fix missing or invalid triggers.

---

### 2. **Path & Name Normalization**
- Search for all references to:
  - `StegCore`, `StegTV`, `tv`, `stegverse-SCW`
- Correct any path variants:
  - `stegverse/` → `StegVerse/`
  - `Stegverse/` → `StegVerse/`
  - `Stegtv` or `StegTV` incorrectly used, etc.

---

### 3. **Cross-Repo Connectivity Repair**
- In YAML workflows, ensure dispatch events such as:

```yaml
repository_dispatch:
  types: [stegcore-update, stegtv-update, scw-trigger]
