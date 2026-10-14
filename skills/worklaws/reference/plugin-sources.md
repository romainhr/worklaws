# Plugin and connector sources (verified on 2026-10-13)

They are used to **recommend** plugins or connectors based on the roles and tools detected. **Nothing is installed without approval [U].**

## Order of preference
1. **Official Anthropic marketplaces** (the marketplace name goes after `@`):

   | Repo | Marketplace | Contents |
   |---|---|---|
   | `anthropics/claude-plugins-official` | `claude-plugins-official` | Official plugins (Claude Code adds it automatically in interactive sessions) |
   | `anthropics/knowledge-work-plugins` | `knowledge-work-plugins` | Plugins by role: productivity, enterprise-search, sales, finance, data, legal, marketing, customer-support, product-management, bio-research, engineering, human-resources, design, operations, small-business, among others. Also includes partner entries in external repos |
   | `anthropics/financial-services` | `claude-for-financial-services` | Financial services |
   | `anthropics/skills` | `anthropic-agent-skills` | Document skills and examples |
   | `anthropics/claude-plugins-community` | `claude-community` | Community: **not official**, review more carefully |

2. **Official tool vendor**, for example Microsoft:
   - **Fabric MCP:** `@microsoft/fabric-mcp`, repo `microsoft/mcp`. In preview.
   - **Azure MCP:** `@azure/mcp`. GA.
   - **Azure DevOps MCP:** remote `https://mcp.dev.azure.com/{org}`, in preview; also local with `npx -y @azure-devops/mcp`.
   - **Power BI Modeling MCP:** `@microsoft/powerbi-modeling-mcp`. Sources disagree on whether it is in preview or GA.

3. **Official MCP Registry:** `GET https://registry.modelcontextprotocol.io/v0.1/servers?search=<text>&version=latest&limit=10`. It accepts servers from any author: **being listed there does not mean being verified**.

4. **Claude connectors directory:** https://claude.com/connectors (no API; for manual review or in the browser).

## How to search from Claude Code
- `claude plugin marketplace list --json`: configured marketplaces.
- `claude plugin list --json --available`: installed and available plugins, with description and installs.
- `claude plugin details <name>`: components and token cost.
- Install (only with approval): `claude plugin install <plugin>@<marketplace> --scope user|project|local`.

## Mandatory security review before recommending
According to the official documentation, *"A Claude Code plugin you install can execute arbitrary code on your machine with your user privileges"*. For each candidate, review and report:
- **Origin:** `github.com/anthropics/*` or an official vendor. Being in an official marketplace does not guarantee a plugin's contents, because many are from partners.
- **What it runs:**
  - Hooks: shell commands outside the sandbox.
  - MCP or LSP servers: local processes.
  - `bin/`: added to the PATH.
  - Auto-update.
- **Context cost:** skill and agent descriptions loaded on every turn (`claude plugin details`).
- **Approved tools only:** if your organization keeps a list of approved tools and the candidate is not on it, recommend it as "requires approval from your governance/security team" and do not install it. Respect the managed settings (`strictKnownMarketplaces`, `blockedMarketplaces`, `enabledPlugins`) defined by your organization.

## If a source does not respond
Report it as "unverified". Do not invent plugin or package names.
