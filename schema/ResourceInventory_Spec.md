# Resource Inventory Schema

```text
Header:Begin
Name:Resource Inventory Schema
Scope:Global
Version:1.0
Format:Table
Schema:ResourceInventory
FileType:Schema_Definition
Description:Defines the structure for resource inventory tables.
LastModified:2026-10-27
Header:End

Data:Begin
Column | Type | Required | Description
ResourceName | String | Yes | Resource identifier
Amount | ScaledInt | Yes | Quantity in inventory
Type | String | Yes | Resource type
Data:End
```
