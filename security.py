from datetime import datetime
import pytz
from config import PASSWORD_PREFIX, TIMEZONE

tz = pytz.timezone(TIMEZONE)

def encrypted_password():
    t = datetime.now(tz).strftime("%H%M")
    return f"{PASSWORD_PREFIX}{t}"
