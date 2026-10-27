# Buff Calibration Schema

```text
Header:Begin
Name:Buff Calibration Schema
Scope:Global
Version:1.1.0
Format:Table
Schema:BuffCalibration
FileType:Schema_Definition
Description:Defines the expected structure for buff calibration files.
LastModified:2026-10-27
Header:End

Data:Begin
Column | Type | Required | Description
BuildingName | String | Yes | Building name or system
Level | Integer | Yes | Building level
OriginalTime | Duration | Yes | Original time before calibration
UpgradeTime | Duration | Yes | Calibrated time after any multiplier
Data:End
```
