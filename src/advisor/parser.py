from __future__ import annotations

from dataclasses import dataclass, field
import re
from pathlib import Path
from typing import Any, Dict, List, Tuple


@dataclass
class ParsedFile:
    path: Path
    metadata: Dict[str, str] = field(default_factory=dict)
    columns: List[str] = field(default_factory=list)
    rows: List[Dict[str, Any]] = field(default_factory=list)


class FileParser:
    """Parse repository data files that follow the Header:Begin/Data:Begin/Data:End convention."""

    @staticmethod
    def strip_comment(line: str) -> str:
        if line.lstrip().startswith("#"):
            return ""
        return line

    @staticmethod
    def parse_header(text: str) -> Dict[str, str]:
        header: Dict[str, str] = {}
        in_header = False
        for raw_line in text.splitlines():
            line = raw_line.rstrip()
            if line == "Header:Begin":
                in_header = True
                continue
            if line == "Header:End":
                in_header = False
                continue
            if in_header:
                stripped = line.strip()
                if not stripped or stripped.startswith("#"):
                    continue
                if ":" not in stripped:
                    continue
                key, value = stripped.split(":", 1)
                header[key.strip()] = value.strip()
        return header

    @staticmethod
    def _split_row(line: str) -> List[str]:
        if "|" in line:
            return [part.strip() for part in line.split("|")]
        return re.split(r"\s+", line.strip())

    @staticmethod
    def parse_file(path: str | Path) -> ParsedFile:
        file_path = Path(path)
        text = file_path.read_text(encoding="utf-8")
        metadata = FileParser.parse_header(text)

        lines = text.splitlines()
        in_data = False
        column_names: List[str] = []
        rows: List[Dict[str, Any]] = []

        for raw_line in lines:
            line = raw_line.strip()
            if not line:
                continue
            if line == "Data:Begin":
                in_data = True
                continue
            if line == "Data:End":
                break
            if not in_data:
                continue

            if line.startswith("#"):
                continue

            if not column_names:
                column_names = FileParser._split_row(line)
                continue

            values = FileParser._split_row(line)
            if len(values) != len(column_names):
                continue

            row = {column_names[idx]: values[idx] for idx in range(len(column_names))}
            rows.append(row)

        return ParsedFile(path=file_path, metadata=metadata, columns=column_names, rows=rows)

    @staticmethod
    def parse_directory(directory: str | Path) -> List[ParsedFile]:
        directory_path = Path(directory)
        return [FileParser.parse_file(path) for path in sorted(directory_path.glob("*.txt"))]
