# Copilot Instructions for Last War Data Hub

## Canonical source of truth
- The authoritative hero upgrade table is:
  - `global/HeroLevelCostTable.txt`
- The canonical schema/spec is:
  - `schema/HeroCost_Spec.md`
  - `LastWarDataFileSpecification.md`

## Hero upgrade cost rule
- The table stores step costs, not cumulative totals.
- A row like `Level 153 Cost 230000000` means:
  - the cost to upgrade from level 152 to level 153
- Total cost from start level to end level is:
  - sum of all step costs for levels start+1 through end

## Preferred calculation method
- Use:
  - `python tools/hero_level_cost_calculator.py --start <START> --end <END> --heroes <COUNT>`
- Do not infer a total by subtracting adjacent rows unless the file explicitly defines cumulative cost.
- When a user asks a hero leveling cost question, prefer the script and the canonical table over manual arithmetic.

## Current-branch data source rule
- When answering resource, player, or account questions, always prefer files from the current branch HEAD (default: `main`) over archived or historical files.
- Only use archive or older log files when the user explicitly asks for historical context, a previous snapshot, or a comparison against older data.
- If a file exists in both the active tree and archive folders, the active-tree version is the authoritative source unless the user requests historical analysis.

## Repository structure
- `global/` = canonical data tables
- `schema/` = schema/spec files
- `tools/` = utility scripts and calculators
- `players/` = account-specific active data, including current resource inventory
- `logs/` = current logs and operational summaries
- `archive/` = historical data only; do not use for current-state answers unless asked
- `src/` = advisor/core logic
