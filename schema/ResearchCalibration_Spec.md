Header:Begin
Name:Research Calibration Schema
Scope:Global
Version:1.0
Format:Table
Schema:ResearchCalibration
FileType:Schema_Definition
Description:Defines the structure for research calibration tables.
LastModified:2026-10-27
Header:End

Data:Begin
Column | Type | Required | Description
ResearchName | String | Yes | Research identifier
Level | Integer | Yes | Research level
Time | Duration | Yes | Research duration
Cost | ScaledInt | Yes | Research cost
Data:End
