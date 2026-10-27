# Tech Data V2 Schema

```text
Header:Begin
Name:Tech Data V2 Schema
Scope:Global
Version:2.0
Format:Table
Schema:TechDataV2
FileType:Schema_Definition
Description:Defines the structure for technology data tables.
LastModified:2026-10-27
Header:End

Data:Begin
Column | Type | Required | Description
TechName | String | Yes | Technology identifier
Level | Integer | Yes | Technology level
Cost | ScaledInt | Yes | Cost for the level
Time | Duration | Yes | Required completion time
Data:End
```
