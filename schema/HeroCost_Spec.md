Header:Begin
Name:Hero Cost Schema
Scope:Global
Version:1.1
Format:Table
Schema:HeroLevelCostTable
FileType:Schema_Definition
Description:Defines the structure for hero level cost tables.
LastModified:2026-10-27
Header:End

Data:Begin
Column | Type | Required | Description
Level | Integer | Yes | Hero level
Cost | ScaledInt | Yes | Cost to advance to this level
Notes | String | No | Additional notes
Data:End
