# Last War Data File Specification

## 1. Purpose

This specification defines the required structure, validation rules, and semantic behavior for all Last War data files used in this repository.

Its purpose is to ensure that:

- files are structurally valid
- parsers produce deterministic results
- data can be validated uniformly
- global and account-scoped data are handled correctly
- schema-specific rules are enforced consistently
- advisors and tools can read the repository as a connected data model

A compliant parser, validator, or advisor must treat this document as the authoritative reference for reading, validating, and interpreting file contents.

---

## 2. Scope

This specification applies to all files in the repository, including:

- global reference data
- account-specific player data
- schema definition files
- index files
- registry files
- future data files added to the project

The specification defines:

- file skeleton
- header metadata
- table parsing rules
- type enforcement
- semantic validation
- scope rules
- error reporting
- validation order

---

## 3. File Skeleton

Every file in this format must contain the following structural markers, in this order:

```text
Header:Begin
... header content ...
Header:End
Data:Begin
... data content ...
Data:End
```

These tags define the outer boundaries of the file.

Rules:

- The tags are case-sensitive.
- They must appear exactly as written.
- The header block may be empty.
- The data block may be empty.
- Content outside the markers is treated as documentation or non-functional metadata.

### 3.1 Minimum Valid File

```text
Header:Begin
Header:End
Data:Begin
Data:End
```

This is a structurally valid empty file.

---

## 4. Header Block

The header block is the section between `Header:Begin` and `Header:End`.

### 4.1 Header Format

Each header field must use the generic form:

```text
Tag:Value
```

Examples:

```text
Name:Main Account Hero Data
Scope:Global
Version:1.0
Format:Table
Schema:BuildingData
```

Rules:

- Header fields may appear in any order.
- Values may contain spaces but not line breaks.
- Tags must not be duplicated unless explicitly marked as repeatable.
- Empty lines within the header are allowed and must be ignored.

### 4.2 Standard Header Fields

The following fields are standardized and may appear in any file unless otherwise specified:

#### Name

```text
Name:<text>
```

Human-readable identifier for the file.

#### Scope

```text
Scope:<Global|Account:<AccountIdentifier>>
```

Declares whether the data is global or account-specific.

#### Version

```text
Version:<text>
```

Version or revision of the file.

#### Format

```text
Format:<Table|Index|Node-Block>
```

Defines how the Data Block must be parsed.

#### Schema

```text
Schema:<text>
```

Identifiers the schema or semantic domain for the file.

#### FileType

```text
FileType:<Data_Table|Schema_Definition>
```

Optional tag identifying whether the file contains primary data or schema metadata.

#### Description

```text
Description:<text>
```

Human-readable description of the file purpose or content.

#### Type

```text
Type:<Target> = <DataType>
```

Used primarily in schema definition files to declare the type for a named field or property.

#### Rule

```text
Rule:<text>
```

Defines a semantic rule local to the file. This tag is repeatable.

#### Delimiter

```text
Delimiter:<Pipe|Whitespace>
```

Optional override for delimiter detection.

### 4.3 Comment and Blank Lines

- A line whose first non-whitespace character is `#` is a comment and must be ignored.
- Blank lines are allowed anywhere in the file.
- Inline comments are not allowed.

---

## 5. Data Block

The data block is the section between `Data:Begin` and `Data:End`.

Rules:

- The data block may be empty.
- All data content must appear inside the Data Block.
- The structure of the data content depends on the declared `Format`.

### 5.1 Table Format

If `Format:Table` is declared, the Data Block must contain a columnar table:

- one label row
- one or more data rows

The first non-empty, non-comment line after `Data:Begin` is treated as the label row.

Rules:

- The label row defines the columns.
- Every data row must have the same number of fields as the label row.
- Empty rows are ignored.
- Comment lines are ignored.

### 5.2 Index Format

If `Format:Index` is declared, the Data Block is interpreted as a list or registry of entries.

Typical examples:

- file lists
- schema references
- player indexes
- active registry entries

Rules:

- The Data Block is not required to contain a label row.
- The content must still respect outer file boundaries.

### 5.3 Node-Block Format

If `Format:Node-Block` is declared, the Data Block is interpreted as a hierarchical or nested structure.

Rules:

- The structure is defined by the schema or file-specific rules.
- It may contain nested sections or grouped values.
- It must still obey the same outer file skeleton.

---

## 6. Delimiter Rules

Unless overridden by a `Delimiter:` tag, parsers must detect the delimiter automatically.

### 6.1 Pipe Delimiter

If any row contains a pipe character (`|`), that row is treated as pipe-delimited.

Rules:

- The pipe character acts as the field separator.
- Surrounding whitespace is trimmed from each field.
- All rows in the same file should use the same delimiter when possible.

### 6.2 Whitespace Delimiter

If no pipe character is detected, the parser treats the row as whitespace-delimited.

Rules:

- One or more spaces or tabs are treated as separators.
- Leading and trailing whitespace are trimmed from each field.
- Fields containing spaces must be quoted or handled according to the field type definition.

### 6.3 Delimiter Precedence

1. `Delimiter:` tag override, if present
2. pipe detection, if any row contains `|`
3. whitespace-delimited parsing

---

## 7. Data Types

Column types are determined by the declared schema, not by the file itself.

The file contains column labels and values, not type annotations.

Examples:

```text
Level Cost Time
30 1200 111d 18:21:40
```

The parser must look up the schema to determine the expected types for `Level`, `Cost`, and `Time`.

### 7.1 Primitive Types

#### Integer

A whole number.

Rules:

- may be negative
- must not contain commas
- must not contain decimal points

Examples:

- `10`
- `-3`

#### Float

A numeric value with a decimal point.

Rules:

- may be negative
- must contain a single decimal point

Examples:

- `1.5`
- `0.99`
- `-2.5`

#### String

Text value.

Rules:

- if a value contains spaces in a whitespace-delimited table, it must be quoted
- examples: `"Headquarters Level 5"`

#### Boolean

Must be exactly:

- `True`
- `False`

Case-insensitive matching is allowed.

### 7.2 Game-Specific Custom Types

#### ScaledInt

A large integer or decimal with a scale suffix.

Supported suffixes:

- `K` = thousand
- `M` = million
- `B` = billion

Examples:

- `10K`
- `1.5M`
- `2B`

#### Duration

Time-string format:

```text
[Days]d [Hours]:[Minutes]:[Seconds]
```

Examples:

- `111d 18:21:40`
- `18:21:40`
- `21:40`

Rules:

- If the day count is zero, it may be omitted.
- If both days and hours are zero, they may also be omitted.
- Because the value contains spaces, the parser must treat the entire duration as a single field value.

---

## 8. Schema and File Type Binding

### 8.1 Format Binding

The `Format` tag controls the structural validation of the Data Block.

- `Format:Table` = table rules apply
- `Format:Index` = index rules apply
- `Format:Node-Block` = hierarchical rules apply

### 8.2 Schema Binding

The `Schema` tag identifies the business logic and required data model for the file.

Examples:

- `Schema:BuildingData`
- `Schema:BuffCalibration`
- `Schema:TechDataV2`
- `Schema:HeroLevelCostTable`

Rules:

- a file must pass the generic structural checks and the schema-specific checks
- the schema defines required columns, data types, and optional rules
- a file that declares a schema but does not conform to it is invalid

### 8.3 FileType Binding

`FileType` is optional but recommended.

Allowed values:

- `Data_Table`
- `Schema_Definition`

Rules:

- `Data_Table` files contain primary data
- `Schema_Definition` files define schema contracts or validation rules

---

## 9. Scope Rules

Scope defines which account or group of accounts a file applies to.

### 9.1 Scope Categories

#### Global

```text
Scope:Global
```

The data applies to all accounts in scope for the user or environment.

#### Account

```text
Scope:Account:<AccountIdentifier>
```

The data applies only to a specific account.

### 9.2 Scope Validation

A file fails validation if:

- the `Scope:` field is missing
- the scope value is malformed
- an account-scoped file references another account
- a global file references account-specific identifiers

Rules:

- Scope does not change the file structure.
- Scope only determines interpretation and data usage.

---

## 10. Semantic Rules

Semantic validation occurs after structural and type validation.

### 10.1 Categories of Semantic Rules

#### Monotonicity

A column may be required to be:

- strictly increasing
- strictly decreasing
- non-decreasing
- non-increasing

#### Uniqueness

A column or key combination may be required to contain unique values.

#### Cross-Column Constraints

Rules may define relationships between columns, such as:

- `Cost >= BaseCost`
- `MaxValue > MinValue`

#### Row-to-Row Constraints

Rules may define relationships between adjacent rows, such as:

- `Cost[n] >= Cost[n-1]`

#### Domain-Specific Constraints

Rules tied to a business domain or game mechanic, such as:

- levels must begin at 1 or 0
- upgrade time must be positive

### 10.2 File-Declared Rules

Header block rules may be declared as:

```text
Rule:<rule text>
```

Examples:

```text
Rule:Level must be strictly increasing
Rule:Cost must be non-negative
Rule:UpgradeTime must be greater than zero
```

Rules:

- `Rule:` tags are repeatable.
- Each tag defines one semantic rule.
- The rule text is free-form but must be consistent with this specification.

### 10.3 Rule Precedence

Semantic rules may come from three sources:

1. file-declared rules
2. schema-required rules
3. universal rules

Priority order:

1. file-declared rules
2. schema-defined rules
3. universal rules

Rules at the same precedence level must not conflict. If rules at different levels conflict, the higher precedence rule governs.

---

## 11. Validation Order

A compliant validation process must occur in this order:

1. Structural validation
   - confirm file boundaries
   - confirm required blocks exist
   - confirm tag placement

2. Header validation
   - confirm tag syntax
   - confirm duplicate rule handling
   - confirm scope validity

3. Data parsing
   - detect delimiter
   - parse label row and data rows
   - ensure row consistency

4. Type validation
   - validate all values against the schema-required types

5. Semantic validation
   - monotonicity
   - uniqueness
   - cross-column checks
   - file rules

6. Advisor interpretation
   - normalize the data into a model
   - compare to global references
   - produce recommendations

---

## 12. Error Reporting

A validator must report validation errors in a standardized, machine-readable way.

Required structure:

```text
ErrorType: <Structural|Type|Semantic>
Section: <section number>
Code: <error code>
Message: <human-readable description>
Line: <line number or N/A>
Column: <column number or N/A>
```

### 12.1 Error Code Format

- Structural errors: `S###`
- Type errors: `T###`
- Semantic errors: `SEM###`

Examples:

- `S001`: Missing `Header:Begin`
- `T003`: Invalid integer value
- `SEM007`: Column must be strictly increasing

### 12.2 Validation Behavior

A validator may:

- stop on the first error, or
- report all errors it finds

The process must be deterministic and non-probabilistic.

---

## 13. Extensibility

This specification is designed to grow over time.

Future changes may include:

- new standard tags
- new data types
- new validation rules
- additional file formats
- new schema definitions

Rules for extension:

- additions must preserve compatibility with current valid files
- breaking changes must be clearly versioned
- new tags must not silently invalidate existing files

---

## 14. Recommended Repository Standard

For this repository, the most practical standard is:

- keep all files in the same structural pattern
- prefer pipe-delimited tables for new files
- keep whitespace parsing for legacy compatibility
- define schemas explicitly for each table family
- use index files for registry/list data
- keep advisor-facing interpretation separate from raw file parsing

This creates a repository that is:

- human readable
- machine readable
- advisor friendly
- easy to validate
- easy to extend

---

## 15. Example: Canonical Data File

```text
Header:Begin
Name:F1NE Buff Calibration
Scope:Account:F1NE
Version:1.4
Format:Table
Schema:BuffCalibration
FileType:Data_Table
Description:Calibration constants for upgrade timing.
Rule:Multiplier = 2.375
Header:End

Data:Begin
BuildingName | Level | OriginalTime | UpgradeTime
Headquarters | 30 | 111d 18:21:40 | 47d 01:24:55
Headquarters | 31 | 122d 22:35:50 | 51d 18:21:35
Wall | 29 | 101d 14:30:37 | 42d 18:44:29
Data:End
```

This layout is recommended for all future data files.

---

## 16. Example: Canonical Schema File

```text
Header:Begin
Name:Buff Calibration Schema
Scope:Global
Version:1.0
Format:Table
Schema:BuffCalibration
FileType:Schema_Definition
Description:Defines the expected structure for buff calibration files.
Header:End

Data:Begin
Column | Type | Required | Description
BuildingName | String | Yes | Name of the building or system
Level | Integer | Yes | Building level
OriginalTime | Duration | Yes | Original time before calibration
UpgradeTime | Duration | Yes | Calibrated time after applying multiplier
Data:End
```

---

## 17. Summary

This specification keeps the original intent of the repository but makes it cleaner, more consistent, and easier for both humans and advisors to work with.

The core ideas are straightforward:

- one file skeleton for all files
- a clear header/data split
- a deterministic validation sequence
- schema-driven typing
- explicit semantic rules
- consistent scope handling
- standard error reporting

This makes the repository suitable not just for storage, but for structured reasoning and recommendation-building.

---

## 18. Recommended Next Action

The next step should be to:

1. adopt this as the project standard
2. review current files for compatibility
3. normalize older files to the same layout where feasible
4. create schema definition files for each major file family
5. build a parser that validates files against this specification before using them in the advisor

This ensures that the advisor is built on a trustworthy data model rather than assumptions about file structure.
