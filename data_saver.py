# data_saver.py
import csv
import json
import os

CSV_HEADERS = ["title", "address", "owner_info", "social_platforms", "start_date", "franchise_info", "owner_name", "owner_linkedin"]

def ensure_output_dirs(output_file):
    os.makedirs(os.path.dirname(output_file), exist_ok=True)

def row_to_csv_dict(record: dict, owner_name: str, owner_linkedin: dict):
    return {
        "title": record.get("title", ""),
        "address": record.get("address", ""),
        "owner_info": json.dumps(record.get("owner_info"), ensure_ascii=False),
        "social_platforms": json.dumps(record.get("social_platforms"), ensure_ascii=False),
        "start_date": json.dumps(record.get("start_date"), ensure_ascii=False),
        "franchise_info": json.dumps(record.get("franchise_info"), ensure_ascii=False),
        "owner_name": owner_name or "",
        "owner_linkedin": json.dumps(owner_linkedin, ensure_ascii=False) if owner_linkedin else ""
    }

def is_already_processed(title: str, address: str, output_file: str):
    """
    Check if (title,address) already present in output file.
    This reads the file once per check (ok for moderate sizes).
    """
    if not os.path.exists(output_file):
        return False
    try:
        with open(output_file, "r", encoding="utf-8", newline='') as f:
            reader = csv.DictReader(f)
            for row in reader:
                t = row.get("title", "")
                a = row.get("address", "")
                if t == str(title) and a == str(address):
                    return True
    except Exception as e:
        print("⚠️ is_already_processed read error:", e)
        return False
    return False

def append_row_to_csv(record: dict, owner_name: str, owner_linkedin: dict, output_file: str):
    """
    Append a single CSV row to output_file. Creates header if file not exists.
    """
    ensure_output_dirs(output_file)
    file_exists = os.path.exists(output_file)
    row = row_to_csv_dict(record, owner_name, owner_linkedin)
    try:
        with open(output_file, "a", encoding="utf-8", newline='') as f:
            writer = csv.DictWriter(f, fieldnames=CSV_HEADERS)
            if not file_exists:
                writer.writeheader()
            writer.writerow(row)
        return True
    except Exception as e:
        print("❌ append_row_to_csv error:", e)
        return False
