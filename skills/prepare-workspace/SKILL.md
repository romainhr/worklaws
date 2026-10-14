---
name: prepare-workspace
description: Cross-cutting step T0. Before any recipe writes to the vault or the tracker, checks that the user configuration, the scope's vault, the project folder and the tracker exist, and creates them with approval if they are missing.
when_to_use: A recipe needs to write to the vault or the tracker and it is unknown whether they exist, SessionStart warns that configuration is missing, or it is the first time the plugin is used.
---

# T0 · Workspace preparation

1. **◇ Does `~/.claude/worklaws-user.json` exist?**
   - No → [U] ask where the vaults live. There must be **one per confidentiality scope** (personal and work). [D] Create the file from the template `../worklaws/templates/worklaws-user.json`.
2. **◇ Does the vault for this work's scope exist?**
   - No → [U] propose a location and structure:
     - Folders: `00_Inbox/`, `projects/`, `knowledge/`, `harness/` (explorations, audits), `_archive/`.
     - Files: a short `CLAUDE.md` with the conventions and an `index.md`.
   - **◇ Approved?**
     - Yes → [S] create the vault. If the vault is synced (iCloud, Obsidian Sync), **do not put binary databases inside it**, such as the Beads one.
     - No → use `docs/` inside the project as a fallback, note it in the handoff, and migrate to the vault once it exists.
3. **◇ Does `vault/projects/<project>/` exist?**
   - No → [S] create `index.md`, with a link to the repo, and add the back-link in the repo's README.
4. **◇ Is the tracker initialized?**
   - No → [S] initialize it **with approval**:
     - Repo with git → Beads (`bd init`).
     - Vault or folder without git → Backlog.md (`backlog init --no-git`), or Markdown tasks if that is not approved.
     - Beads without git only with `BEADS_DIR` and `bd init --stealth`, and outside synced folders.
5. **Workspace ready:** return to the recipe that called you.

**Rule:** never create structure without approval. No recipe writes to a place that does not exist: if it is missing, it goes through here.
