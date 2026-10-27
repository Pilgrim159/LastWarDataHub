# Research Calibration Schema

```text
Header:Begin
Name: Research Calibration Schema
Version: 1.0
Scope: Global
Format: Specification
Schema: ResearchCalibration
FileType: Schema_Definition
Description: Tracks and verifies player-specific research time reduction multipliers.
Header:End

Data:Begin
# Declared Data Model
Column | Type | Required | Description
TreeID | String | Yes | Research tree identifier
NodeID | String | Yes | Research node identifier
NodeLevel | Integer | Yes | Research node level
OriginalTime | Duration | Yes | Original research duration
UpgradeTime | Duration | Yes | Actual reduced completion time

# Required File-Level Header Declarations
Rule: Target files must declare Format: Table
Rule: Target files must declare Schema: ResearchCalibration
Rule: Target files must include Header Field [ResearchID: Research_Calibration]
Rule: Target files must include Header Field [Rule: Multiplier = Float]
Rule: Target files must include Header Field [Rule: UpgradeTime = Floor(OriginalTime / Multiplier)]

# Column Type Declarations
Type: TreeID = String
Type: NodeID = String
Type: NodeLevel = Integer
Type: OriginalTime = Duration
Type: UpgradeTime = Duration

# Semantic Rules
Rule: UpgradeTime must be mathematically less than or equal to OriginalTime.
Rule: The declared Multiplier must cleanly resolve the UpgradeTime using the formula defined in the header.
Data:End
```
