#!/usr/bin/env python3
"""
Last War DataHub - Resource Inventory Auditor
Compliant with File Format Specification v1.1.0 (Sections 4 & 5)
"""

import sys
import os
import re
from typing import List, Dict, Tuple, Optional

class DataHubParser:
    """Handles core structural and formatting logic defined in the Specification."""
    
    def __init__(self):
        self.explicit_delimiter: Optional[str] = None
        self.in_data_block: bool = False
        self.label_row_passed: bool = False

    def parse_header_tag(self, line: str) -> None:
        """Extracts optional overrides from the Header block (Section 4.6)."""
        if line.startswith("Delimiter:"):
            val = line.split(":", 1)[1].strip().lower()
            if val == "pipe":
                self.explicit_delimiter = "|"
            elif val == "whitespace":
                self.explicit_delimiter = "space"

    def process_data_row(self, row: str) -> Optional[List[str]]:
        """
        Applies structural and delimiter logic to a single row.
        Returns a list of trimmed fields, or None if the row is skipped.
        """
        # Section 5.5: Internal/External tag stripping and whitespace normalization
        clean_row = re.sub(r'<.*?>', '', row).strip()

        # Section 4.4 (Blank Lines) and Section 4.5 (Comments)
        if not clean_row or clean_row.startswith('#'):
            return None
            
        # Section 5.2 (The Label Row) - Skip the first valid line after Data:Begin
        if not self.label_row_passed:
            self.label_row_passed = True
            return None

        # Section 5.4 & 4.6: Delimiter Precedence and Overrides
        if self.explicit_delimiter == "|":
            return [p.strip() for p in clean_row.split('|')]
        elif self.explicit_delimiter == "space":
            return clean_row.split()
        else:
            # Auto-Detection Fallback
            if '|' in clean_row:
                return [p.strip() for p in clean_row.split('|')]
            else:
                return clean_row.split()

class ResourceAuditor:
    """Handles the business logic of calculating Last War resource totals."""

    @staticmethod
    def parse_scaled_int(val_str: str) -> float:
        """Converts game-type ScaledInt (Section 6.3) to a raw float."""
        val_str = val_str.upper()
        multiplier = 1.0
        if val_str.endswith('K'):
            multiplier = 1_000.0
            val_str = val_str[:-1]
        elif val_str.endswith('M'):
            multiplier = 1_000_000.0
            val_str = val_str[:-1]
        elif val_str.endswith('G'):
            multiplier = 1_000_000_000.0
            val_str = val_str[:-1]
        
        try:
            return float(val_str) * multiplier
        except ValueError:
            return 0.0

    @staticmethod
    def format_scaled_int(val: float) -> str:
        """Converts a raw float back to a readable game-type ScaledInt."""
        if val >= 1_000_000_000:
            return f"{val / 1_000_000_000:.2f}G"
        elif val >= 1_000_000:
            return f"{val / 1_000_000:.2f}M"
        elif val >= 1_000:
            return f"{val / 1_000:.2f}K"
        return str(int(val))

    def run_audit(self, filepath: str):
        """Executes the delta analysis on the specified inventory file."""
        if not os.path.exists(filepath):
            print(f"Error: File '{filepath}' not found.")
            return

        parser = DataHubParser()
        totals: Dict[str, float] = {"Food": 0.0, "Iron": 0.0, "Coin": 0.0}

        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    
                    # Structural Boundaries (Section 4.1)
                    if line == "Header:Begin":
                        continue
                    elif line == "Header:End":
                        continue
                    elif line == "Data:Begin":
                        parser.in_data_block = True
                        continue
                    elif line == "Data:End":
                        parser.in_data_block = False
                        break

                    # Route line to correct processor
                    if not parser.in_data_block:
                        parser.parse_header_tag(line)
                    else:
                        fields = parser.process_data_row(line)
                        if fields:
                            self._accumulate_resources(fields, totals)

            self._print_summary(totals)

        except Exception as e:
            print(f"Audit Failed: {str(e)}")

    def _accumulate_resources(self, fields: List[str], totals: Dict[str, float]):
        """Maps parsed fields to resource accumulation logic."""
        # Depending on your F1NE_Resource_Inventory.txt schema, you may need to 
        # adjust the index mappings below. Assuming [Source, Resource, Amount, ...]
        try:
            # We look for keywords in the fields to safely extract values
            # regardless of whether it is the old or new format.
            res_type = None
            amount_str = None
            
            for field in fields:
                field_upper = field.upper()
                if field_upper in ["FOOD", "IRON", "COIN"]:
                    res_type = field.capitalize()
                elif any(char.isdigit() for char in field) and any(suffix in field_upper for suffix in ['K', 'M', 'G']):
                    amount_str = field
                    
            if res_type and amount_str:
                totals[res_type] += self.parse_scaled_int(amount_str)
        except IndexError:
            pass # Malformed row safely ignored

    def _print_summary(self, totals: Dict[str, float]):
        """Outputs the strategic briefing."""
        print("=" * 50)
        print(" COMMANDER F1NE - RESOURCE AUDIT ".center(50, "="))
        print("=" * 50)
        for res, amount in totals.items():
            formatted_amount = self.format_scaled_int(amount)
            # Add strategic context based on our current goals
            status = ""
            if res == "Iron":
                target = 1_000_000_000 # 1.0G target for Tank Center 31
                if amount >= target:
                    status = " [TARGET ACHIEVED: TANK CENTER 31 READY]"
                else:
                    deficit = self.format_scaled_int(target - amount)
                    status = f" [FARMING: {deficit} Deficit]"
            elif res == "Coin":
                target = 215_000_000
                if amount >= target:
                    status = " [TARGET ACHIEVED]"
                    
            print(f" {res:<10} | {formatted_amount:>10} {status}")
        print("=" * 50)


if __name__ == "__main__":
    # Point this to your actual file path
    target_file = os.path.join("players", "F1NE_Resource_Inventory.txt")
    
    # Allow command line override
    if len(sys.argv) > 1:
        target_file = sys.argv[1]
        
    auditor = ResourceAuditor()
    auditor.run_audit(target_file)
