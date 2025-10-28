# train_assistant/functions/datetime_parser.py

from datetime import datetime, timedelta
import re
from typing import Tuple, Optional
import pytz

# Victoria/Melbourne timezone (same as PTV app)
MELBOURNE_TZ = pytz.timezone('Australia/Melbourne')

def parse_natural_datetime(input_text: str) -> Tuple[Optional[str], Optional[str]]:
    """
    Parse natural language date/time expressions and return (date, time) tuple.
    Uses Australia/Melbourne timezone (same as PTV app).
    
    Args:
        input_text: User input containing date/time expressions
        
    Returns:
        Tuple of (date_str, time_str) where:
        - date_str: YYYY-MM-DD format (e.g., "2025-09-06") or None if no date mentioned
        - time_str: HH:MM AM/PM format (e.g., "10:00 PM") or None if no time mentioned
    """
    if not input_text:
        return None, None
    
    text = input_text.lower().strip()
    date_str = None
    time_str = None
    
    # Get current Melbourne time (same as PTV app)
    now_melbourne = datetime.now(MELBOURNE_TZ)
    
    # Parse date expressions - ONLY if explicitly mentioned
    if 'today' in text:
        date_str = now_melbourne.strftime('%Y-%m-%d')
    elif 'tomorrow' in text:
        tomorrow = now_melbourne + timedelta(days=1)
        date_str = tomorrow.strftime('%Y-%m-%d')
    elif 'yesterday' in text:
        yesterday = now_melbourne - timedelta(days=1)
        date_str = yesterday.strftime('%Y-%m-%d')
    
    # Check for specific date patterns (DD/MM/YYYY, DD-MM-YYYY, etc.)
    if not date_str:  # Only check if no date found yet
        date_patterns = [
            r'(\d{1,2})[/-](\d{1,2})[/-](\d{4})',  # DD/MM/YYYY or DD-MM-YYYY
            r'(\d{4})[/-](\d{1,2})[/-](\d{1,2})',  # YYYY/MM/DD or YYYY-MM-DD
        ]
        
        for pattern in date_patterns:
            match = re.search(pattern, text)
            if match:
                if pattern.startswith(r'(\d{4})'):  # YYYY-MM-DD format
                    year, month, day = match.groups()
                else:  # DD-MM-YYYY format
                    day, month, year = match.groups()
                
                try:
                    # Create date in Melbourne timezone
                    parsed_date = MELBOURNE_TZ.localize(datetime(int(year), int(month), int(day)))
                    date_str = parsed_date.strftime('%Y-%m-%d')
                    break
                except ValueError:
                    continue
    
    # Parse time expressions - ONLY if explicitly mentioned
    time_patterns = [
        # 12-hour format with AM/PM (already correct format)
        (r'(\d{1,2}):(\d{2})\s*(am|pm)', lambda h, m, period: f"{int(h):02d}:{int(m):02d} {period.upper()}"),
        (r'(\d{1,2})\s*(am|pm)', lambda h, period, _: f"{int(h):02d}:00 {period.upper()}"),
        
        # 24-hour format - convert to 12-hour format
        (r'(\d{1,2}):(\d{2})(?!\s*[ap]m)', lambda h, m: _convert_24_to_12(int(h), int(m))),
    ]
    
    for pattern, converter in time_patterns:
        match = re.search(pattern, text)
        if match:
            try:
                groups = match.groups()
                if len(groups) == 3:  # Hour, minute, AM/PM
                    time_str = converter(groups[0], groups[1], groups[2])
                elif len(groups) == 2 and groups[1] in ['am', 'pm']:  # Hour, AM/PM
                    time_str = converter(groups[0], groups[1], None)
                elif len(groups) == 2:  # Hour, minute (24-hour)
                    time_str = converter(groups[0], groups[1])
                break
            except (ValueError, IndexError):
                continue
    
    # Handle common time expressions - ONLY if explicitly mentioned
    if not time_str:  # Only check if no time found yet
        time_aliases = {
            'morning': '09:00 AM',
            'noon': '12:00 PM', 
            'afternoon': '03:00 PM',
            'evening': '06:00 PM',
            'night': '08:00 PM',
            'midnight': '12:00 AM'
        }
        
        for alias, time_value in time_aliases.items():
            if alias in text:
                time_str = time_value
                break
    
    return date_str, time_str

def _convert_24_to_12(hour: int, minute: int) -> str:
    """Convert 24-hour format to 12-hour format with AM/PM."""
    if hour == 0:
        return f"12:{minute:02d} AM"
    elif hour < 12:
        return f"{hour:02d}:{minute:02d} AM"
    elif hour == 12:
        return f"12:{minute:02d} PM"
    else:
        return f"{hour-12:02d}:{minute:02d} PM"

def _convert_12_to_24(hour: int, minute: int, period: str) -> str:
    """Convert 12-hour format to 24-hour format (for legacy support)."""
    if period.lower() == 'pm' and hour != 12:
        hour += 12
    elif period.lower() == 'am' and hour == 12:
        hour = 0
    
    return f"{hour:02d}:{minute:02d}"

def get_current_melbourne_time() -> datetime:
    """
    Get current time in Melbourne timezone (same as PTV app).
    Useful for debugging or logging.
    """
    return datetime.now(MELBOURNE_TZ)

def get_melbourne_date_string() -> str:
    """
    Get current date in Melbourne timezone as YYYY-MM-DD string.
    """
    return datetime.now(MELBOURNE_TZ).strftime('%Y-%m-%d')

def get_melbourne_time_string() -> str:
    """
    Get current time in Melbourne timezone as HH:MM AM/PM string.
    """
    now = datetime.now(MELBOURNE_TZ)
    return _convert_24_to_12(now.hour, now.minute)



