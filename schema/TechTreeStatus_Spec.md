Header:Begin
Name:Tech Tree Status Schema
Scope:Global
Version:1.0
Format:Table
Schema:TechTreeStatus
FileType:Schema_Definition
Description:Defines the structure for technology tree status tables.
LastModified:2026-10-27
Header:End

Data:Begin
Column | Type | Required | Description
TechName | String | Yes | Technology identifier
NodeStatus | String | Yes | Current node state
Level | Integer | Yes | Current level
Data:End
