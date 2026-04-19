import re

def parse_scaled_val(val_str):
    """Converts Hub-scaled strings (e.g., 723.3M, 150.9K) to floats."""
    if not val_str or val_str == "":
        return 0.0
    val_str = val_str.upper().strip()
    multipliers = {'K': 1_000, 'M': 1_000_000, 'G': 1_000_000_000}
    
    if val_str[-1] in multipliers:
        return float(val_str[:-1]) * multipliers[val_str[-1]]
    try:
        return float(val_str)
    except ValueError:
        return 0.0

def format_value(total):
    """Standardizes large number formatting for reports."""
    if total >= 1_000_000_000:
        return f"{total/1_000_000_000:>12.2f}G"
    if total >= 1_000_000:
        return f"{total/1_000_000:>12.2f}M"
    if total >= 1_000:
        return f"{total/1_000:>12.2f}K"
    return f"{total:>13.2f}"

def run_master_summary(file_content):
    """
    Parses a LastWarDataHub resource inventory file and provides:
    1. Individual item breakdowns (Source, Total, Unit)
    2. Category-level totals with Minutes, Hours, and Days for Speedups.
    """
    # 1. Extract Data Block using Hub Specification delimiters
    data_match = re.search(r'Data:Begin\n(.*?)\nData:End', file_content, re.DOTALL)
    if not data_match:
        print("Error: No 'Data:Begin'/'Data:End' block found.")
        return
    
    data_rows = data_match.group(1).strip().split('\n')
    
    individual_items = [] 
    category_totals = {}

    for row in data_rows:
        # Clean row: remove tags and normalize whitespace
        clean_row = re.sub(r'<.*?>', '', row).strip()
        if not clean_row or clean_row.startswith('Source'):
            continue
        
        parts = clean_row.split()
        if len(parts) < 5:
            continue

        source = parts[0]
        category = parts[1]
        item = parts[2]
        size_val = parts[3]
        count_val = parts[4]
        unit = parts[5] if len(parts) > 5 else "Points"
        
        # Calculation: GrandTotal = UnitSize * PacketCount
        val = parse_scaled_val(size_val) * parse_scaled_val(count_val)
        
        if category == "Speedup":
            if unit == "Hours":
                val *= 60
            unit = "Minutes" # Standardize unit name for aggregation
        
        # Track for Section 1 (Individual entries)
        individual_items.append({
            "item": item,
            "source": source,
            "total": val,
            "unit": unit
        })
        
        # Track for Section 2 (Aggregated totals)
        if category not in category_totals:
            category_totals[category] = {}
        if item not in category_totals[category]:
            category_totals[category][item] = {"total": 0.0, "unit": unit}
        category_totals[category][item]["total"] += val

    # SECTION 1: Individual Item Summary (Row-by-Row breakdown)
    print(f"{'Item Name':<20} | {'Source':<12} | {'Total Holding':<15} | {'Unit'}")
    print("-" * 65)
    for entry in individual_items:
        print(f"{entry['item']:<20} | {entry['source']:<12} | {format_value(entry['total'])} | {entry['unit']}")

    print("\n" + "="*75 + "\n")

    # SECTION 2: Category Totals (Aggregated with Time Conversions)
    print(f"{'Category/Item':<25} | {'Total Holding (m / h / d)':<40}")
    print("-" * 75)

    for cat, items in sorted(category_totals.items()):
        print(f"[{cat.upper()}]")
        cat_min_total = 0.0
        
        for item, data in sorted(items.items()):
            total = data["total"]
            unit = data["unit"]
            
            if cat == "Speedup":
                mins = total if unit == "Minutes" else total * 60
                cat_min_total += mins
                h, d = mins/60, mins/1440
                print(f"  {item:<23} | {mins:,.0f}m / {h:,.1f}h / {d:,.2f}d")
            else:
                print(f"  {item:<23} | {format_value(total)} {unit}")
        
        if cat == "Speedup":
            h_total = cat_min_total/60
            d_total = cat_min_total/1440
            print(f"  {'-- Category Total --':<23} | {cat_min_total:,.0f}m / {h_total:,.1f}h / {d_total:,.2f}d")
        print("")

# Example usage for local execution:
# if __name__ == "__main__":
#     with open('players/F1NE_Resource_Inventory.txt', 'r') as f:
#         run_master_summary(f.read())
