import gspread
import requests
from dotenv import dotenv_values

config = dotenv_values('.env')

RA_API_KEY = config['RA_API_KEY']
GOOGLE_SHEET_KEY = config['GOOGLE_SHEET_KEY']

client = gspread.service_account()
sheet = client.open_by_key(GOOGLE_SHEET_KEY)

# Get all RA systems that are active and gaming (no hubs or events)
get_systems_url = requests.get(f"https://retroachievements.org/API/API_GetConsoleIDs.php?y={RA_API_KEY}&a=1&g=1")
systems = get_systems_url.json()

try:
    worksheet = sheet.worksheet('Active Systems')
except gspread.exceptions.WorksheetNotFound:
    worksheet = sheet.add_worksheet(title="Active Systems", rows="100", cols="20")

# Clear the worksheet before writing new data
worksheet.clear()

# Write the header
worksheet.append_row(['ID', 'System Name'])

# Write the data
for system in systems:
    worksheet.append_row([system['ID'], system['Name']])

print("Systems written to Google Sheets successfully.")

