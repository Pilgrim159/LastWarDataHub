# Master Schema Registry

This document is the repository’s canonical schema registry in the repository’s v2 file format. It defines the authoritative mapping between schema names and the schema definition files that govern their validation and semantics.

```text
Header:Begin
Name:Master Schema Registry
Scope:Global
Version:1.0
Format:Index
Schema:MasterIndex
FileType:Schema_Definition
Description:Master index of schema files. Maps schema tags to their authoritative definition files.
LastModified:2026-10-27
Header:End

Data:Begin
SchemaDefinition|BuffCalibration|schema/BuffCalibration_Spec.txt
SchemaDefinition|BuildingData|schema/BuildingData_Spec.txt
SchemaDefinition|BuildingStatus|schema/Building_Status_Spec.txt
SchemaDefinition|HeroLevelCostTable|schema/HeroCost_Spec.txt
SchemaDefinition|ResourceInventory|schema/ResourceInventory_Spec.txt
SchemaDefinition|ResearchCalibration|schema/ResearchCalibration_Spec.txt
SchemaDefinition|HeroMasterRegistry|schema/HeroMasterRegistry_Spec.txt
SchemaDefinition|HeroSkillRegistry|schema/Hero_Skill_Registry_Spec.txt
SchemaDefinition|TechDataV2|schema/TechData_V2_Spec.txt
SchemaDefinition|TechTreeStatus|schema/TechTreeStatus_Spec.txt
SchemaDefinition|FileFormatSpecification|schema/File Format Specification.txt
Data:End
```

## Notes

- This index is the authoritative lookup table for schema definitions.
- Validation tools should read this index before loading any schema file.
- New schemas must be added here in the same `SchemaDefinition|Name|Path` format.
- The legacy `schema_index.txt` file remains as historical reference material until full migration is complete.
