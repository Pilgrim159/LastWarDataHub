# Building Data Schema

```text
Header:Begin
Name:Building Data Schema
Scope:Global
Version:1.1.0
Format:Table
Schema:BuildingData
FileType:Schema_Definition
Description:Defines the expected structure for building data tables.
LastModified:2026-10-27
Header:End

Data:Begin
Column | Type | Required | Description
BuildingName | String | Yes | Building identifier
TargetLevel | Integer | Yes | Building level target
OriginalTime | Duration | Yes | Base construction time
Food | ScaledInt | Yes | Food cost for the target level
Iron | ScaledInt | Yes | Iron cost for the target level
Coin | ScaledInt | Yes | Coin cost for the target level
Oil | ScaledInt | Yes | Oil cost for the target level
ResearchRequirements | String | No | Research dependencies as key/value pairs
BuildingRequirements | String | No | Building dependencies as key/value pairs
Notes | String | No | Additional notes
Data:End
```
