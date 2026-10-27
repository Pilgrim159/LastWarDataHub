Header:Begin
Name:Building Status Schema
Scope:Global
Version:1.0
Format:Table
Schema:BuildingStatus
FileType:Schema_Definition
Description:Defines the expected structure for building status tables.
LastModified:2026-10-27
Header:End

Data:Begin
Column | Type | Required | Description
BuildingName | String | Yes | Building identifier
Status | String | Yes | Current state of the building
Level | Integer | Yes | Current level
Notes | String | No | Additional commentary
Data:End
