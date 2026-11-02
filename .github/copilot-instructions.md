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
- When creating or updating a log, use the relevant `players/` files for current resource values and the latest active log for other account-state details. If the sources conflict, prefer `players/` for resources, mention the discrepancy, and identify the source of the values used.

## Repository structure
- `global/` = canonical data tables
- `schema/` = schema/spec files
- `tools/` = utility scripts and calculators
- `players/` = account-specific active data, including current resource inventory
- `logs/` = current logs and operational summaries
- `archive/` = historical data only; do not use for current-state answers unless asked
- `src/` = advisor/core logic

## Advisor behavior

### Repository-first reasoning

- Treat repository data as authoritative.
- Prefer repository facts over model assumptions.
- If repository data conflicts with remembered information, use repository data.
- Distinguish clearly between:
  - verified repository data
  - calculated results
  - advisor recommendations
  - assumptions

### Discovery procedure

When locating information:

1. Start with the repository root index.
2. Follow index references to child indexes.
3. Follow child indexes to source files.
4. Prefer canonical files identified in these instructions.
5. Prefer active-tree files over archive files.

### Source reporting

- Identify source file paths used in calculations.
- Report authoritative source files when answering questions.
- If multiple files contribute to an answer, list the significant sources.
- Document conflicts between sources.

### Current-state questions

For current account status, resources, heroes, buildings, or technology:

1. Use `players/` as the authoritative source.
2. Use `logs/` for current operational context.
3. Use `global/` for game mechanics and requirements.
4. Ignore `archive/` unless historical analysis is requested.

### Historical analysis

- Use `archive/` only when historical context, trends, snapshots, or comparisons are requested.
- Clearly distinguish current values from historical values.
- Identify the files and dates used for historical comparisons.

### Calculations

- Prefer calculators and utilities in `tools/` when available.
- Prefer canonical tables in `global/` over manual estimation.
- Show formulas or calculation methods when practical.
- Distinguish source values from calculated values.

### Missing data

- Do not invent values.
- State which file is expected.
- State which source was searched.
- Request the missing file when required.

### Authority order

When sources conflict, use the following precedence:

1. Canonical schema/specification files.
2. Canonical global data tables.
3. Active player files.
4. Current logs.
5. Archive files.

Document any conflicts encountered.