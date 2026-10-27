from __future__ import annotations

from pathlib import Path
import re
from typing import Dict, Iterable, List, Optional


class SchemaRegistry:
    """Resolve schema names to authoritative Markdown schema paths."""

    def __init__(self, repo_root: str | Path):
        self.repo_root = Path(repo_root).resolve()
        self.schema_dir = self.repo_root / "schema"
        self.index_path = self.schema_dir / "schema_index.md"
        self._schema_map: Optional[Dict[str, str]] = None

    def load(self) -> Dict[str, str]:
        if self._schema_map is not None:
            return self._schema_map

        if not self.index_path.exists():
            raise FileNotFoundError(f"Schema index not found: {self.index_path}")

        data = self.index_path.read_text(encoding="utf-8")
        schema_map: Dict[str, str] = {}

        in_data = False
        for raw_line in data.splitlines():
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

            if "SchemaDefinition" in line:
                match = re.split(r"\s*\|\s*", line)
                if len(match) >= 3:
                    schema_name = match[1].strip()
                    schema_path = match[2].strip()
                    schema_map[schema_name] = str(Path(schema_path).as_posix())

        self._schema_map = schema_map
        return schema_map

    def resolve(self, schema_name: str) -> Path:
        mapping = self.load()
        if schema_name not in mapping:
            raise KeyError(f"Unknown schema: {schema_name}")
        return self.repo_root / mapping[schema_name]

    def all_schemas(self) -> Iterable[str]:
        return self.load().keys()
