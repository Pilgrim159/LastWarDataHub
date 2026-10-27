# Last War Data Hub

This repository stores and organizes Last War data files in a format governed by the canonical specification:

- `LastWarDataFileSpecification.md`

Use this specification as the authoritative reference for file structure, validation rules, scope semantics, schema binding, and parser behavior.

## Repository Purpose

The project is designed to keep Last War data in a consistent, machine-readable, and advisor-friendly form. The repository may contain:

- global reference data
- account-scoped player data
- schema definition files
- registry or index files
- parser and validation tooling

## Recommended Reading Order

When onboarding or working with the repository, read in this order:

1. `README.md`
2. `LastWarDataFileSpecification.md`
3. schema files in `schema/`
4. index and registry files in root or related directories
5. data tables and account-specific files
6. parsing or validation tools in `tools/`

This order ensures that file structure and semantic rules are understood before raw data is interpreted.

## Canonical File Format

All files in this repository should follow the standard skeleton:

```text
Header:Begin
... header content ...
Header:End
Data:Begin
... data content ...
Data:End
```

Important rules:

- `Header:Begin` and `Data:Begin` markers are required in order
- `Header:End` and `Data:End` close each section
- header fields use `Tag:Value` syntax
- data format depends on the declared `Format` value
- `Schema` must align with the file structure and data model
- scopes must be valid and consistent with file intent

## Standard Header Fields

Common fields include:

- `Name`
- `Scope`
- `Version`
- `Format`
- `Schema`
- `FileType`
- `Description`
- `Rule`
- `Delimiter`
- `LastModified`

For complete rules, validation requirements, and schema semantics, see `LastWarDataFileSpecification.md`.

## Data Interpretation Rules

- Tables are validated according to declared columns and row consistency
- Index files are treated as registry/list records, not labeled tables
- Node-block files are hierarchical and schema-defined
- Data types are determined by the schema, not by the file itself
- Error reporting should follow the canonical validation format defined in the specification

## Working Convention

When adding or editing files:

- keep the document structure aligned with the canonical specification
- prefer explicit, deterministic parsing rules
- avoid creating new structural regions outside the standard format
- use the header fields for metadata, not ad hoc text blocks
- validate files against the canonical spec before using them in tools or advisors

## Repository Layout

- `global/` — global or shared data files
- `players/` — account-specific player data
- `schema/` — schema definitions and type contracts
- `tools/` — parser, validation, or conversion utilities
- `test/` — validation or example test cases
- `logs/` — operational or processing logs
- `archive/` — historical or legacy files

## Important Note

This README is a project guide. The specification file is the source of truth for file format, validation, and semantic interpretation.

If a rule in this README appears to conflict with the canonical specification, the specification wins.
