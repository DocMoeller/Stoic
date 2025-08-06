import json
import os
import csv
from datetime import datetime
from io import StringIO
from fpdf import FPDF
from typing import List, Dict, Any, Tuple
from pathlib import Path

# Default storage path - can be overridden by configuration
DEFAULT_STORAGE_PATH = Path(__file__).parent / 'storage' / 'reflections.json'

# Field names for consistent access
ENTRY_FIELDS = [
    'morning_control', 'morning_challenges', 'morning_virtue',
    'evening_good', 'evening_better', 'evening_learning'
]

def get_storage_path() -> Path:
    """Get the storage path, allowing for configuration override."""
    try:
        from flask import current_app
        return current_app.config.get('REFLECTIONS_FILE', DEFAULT_STORAGE_PATH)
    except (ImportError, RuntimeError):
        # Fallback when not in Flask context
        return DEFAULT_STORAGE_PATH

def ensure_rating(entry: Dict[str, Any]) -> Dict[str, Any]:
    """Ensure entry has a rating field with default value."""
    if 'rating' not in entry:
        entry['rating'] = 0
    return entry

def sort_entries_with_index(entries: List[Dict[str, Any]], sort_order: str = 'desc') -> List[Tuple[int, Dict[str, Any]]]:
    """Sort entries with their original indices for consistent handling."""
    return sorted(enumerate(entries), key=lambda x: x[1]['timestamp'], reverse=(sort_order != 'asc'))

def create_entry_from_form(form_data: Dict[str, str]) -> Dict[str, Any]:
    """Create a new entry from form data with consistent structure."""
    return {
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'morning_control': form_data.get('morning_control', ''),
        'morning_challenges': form_data.get('morning_challenges', ''),
        'morning_virtue': form_data.get('morning_virtue', ''),
        'evening_good': form_data.get('evening_good', ''),
        'evening_better': form_data.get('evening_better', ''),
        'evening_learning': form_data.get('evening_learning', ''),
        'rating': int(form_data.get('rating', 3)),
    }

def update_entry_from_form(entry: Dict[str, Any], form_data: Dict[str, str]) -> Dict[str, Any]:
    """Update an existing entry from form data."""
    entry['morning_control'] = form_data.get('morning_control', '')
    entry['morning_challenges'] = form_data.get('morning_challenges', '')
    entry['morning_virtue'] = form_data.get('morning_virtue', '')
    entry['evening_good'] = form_data.get('evening_good', '')
    entry['evening_better'] = form_data.get('evening_better', '')
    entry['evening_learning'] = form_data.get('evening_learning', '')
    entry['rating'] = int(form_data.get('rating', 3))
    return entry

def validate_index(index: int, entries: List[Dict[str, Any]]) -> bool:
    """Validate that an index is within bounds for the entries list."""
    return 0 <= index < len(entries)

def generate_csv_export(entries: List[Dict[str, Any]]) -> str:
    """Generate CSV content from entries."""
    si = StringIO()
    cw = csv.writer(si)
    cw.writerow(['Timestamp', 'Morning Control', 'Morning Challenges', 'Morning Virtue', 
                'Evening Good', 'Evening Better', 'Evening Learning', 'Rating'])
    for entry in entries:
        cw.writerow([
            entry['timestamp'],
            entry['morning_control'],
            entry['morning_challenges'],
            entry['morning_virtue'],
            entry['evening_good'],
            entry['evening_better'],
            entry['evening_learning'],
            entry['rating']
        ])
    return si.getvalue()

def generate_pdf_export(entries: List[Dict[str, Any]]) -> bytes:
    """Generate PDF content from entries."""
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("helvetica", size=12)
    for entry in entries:
        pdf.cell(200, 10, txt=f"Dato: {entry['timestamp']}", ln=True)
        pdf.cell(200, 10, txt=f"Vurdering: {entry['rating']}/5", ln=True)
        pdf.multi_cell(0, 10, txt=f"Morgen\n- Kontrol: {entry['morning_control']}\n- Udfordringer: {entry['morning_challenges']}\n- Dyd: {entry['morning_virtue']}\nAften\n- Godt: {entry['evening_good']}\n- Bedre: {entry['evening_better']}\n- Læring: {entry['evening_learning']}\n", border=0)
        pdf.ln(5)
    return pdf.output(dest='S').encode('latin1')

def load_entries() -> List[Dict[str, Any]]:
    """Load all journal entries from the JSON file."""
    storage_path = get_storage_path()
    if not storage_path.exists():
        return []
    with open(storage_path, 'r', encoding='utf-8') as f:
        try:
            entries = json.load(f)
            # Ensure all entries have rating field
            return [ensure_rating(entry) for entry in entries]
        except json.JSONDecodeError:
            return []

def save_entries(entries: List[Dict[str, Any]]) -> None:
    """Save all journal entries to the JSON file."""
    storage_path = get_storage_path()
    storage_path.parent.mkdir(parents=True, exist_ok=True)
    # Ensure all entries have rating field before saving
    entries_with_rating = [ensure_rating(entry) for entry in entries]
    with open(storage_path, 'w', encoding='utf-8') as f:
        json.dump(entries_with_rating, f, ensure_ascii=False, indent=2)
