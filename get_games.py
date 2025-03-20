import gspread
import requests
import time
from dotenv import dotenv_values

config = dotenv_values('.env')

RA_API_KEY = config['RA_API_KEY']
GOOGLE_SHEET_KEY = config['GOOGLE_SHEET_KEY']

client = gspread.service_account()
sheet = client.open_by_key(GOOGLE_SHEET_KEY)

def get_supported_files(game_id):
    url = f"https://retroachievements.org/API/API_GetGameHashes.php?i={game_id}&y={RA_API_KEY}"
    r = requests.get(url).json()
    
    if not r:
        return None
    else:
        return r['Results']

def add_worksheet(system_name, wait=0):
    wait = wait * 2  # Double the wait time for each retry - first time is 0 wait
    if wait > 60: # Cap the wait time to 60 seconds
        wait = 60
    time.sleep(wait) # Wait for the specified time

    try:
        worksheet = sheet.worksheet(system_name)
    except gspread.exceptions.WorksheetNotFound:
        try:
            worksheet = sheet.add_worksheet(title=system_name, rows="100", cols="20")
        except gspread.exceptions.APIError as e:
            worksheet = add_worksheet(system_name, wait + 1)
    return worksheet


# Open or Create a worksheet for each system by name
def get_games(system):
    system_name = system['System Name']
    print(f"Getting games for {system_name}...")

    console_worksheet = add_worksheet(system_name)

    # Write the header
    write_header(console_worksheet)

    # Get all games for the system
    get_games_url = requests.get(f"https://retroachievements.org/API/API_GetGameList.php?i={system['ID']}&h=1&f=1&y={RA_API_KEY}&o=0&c=0")
    
    # count number games returned
    num_games = len(get_games_url.json())
    print(f"Number of games returned: {num_games}")

    games = get_games_url.json()

    # Write the data
    for game in games:
        files = get_supported_files(game['ID'])
        if not files:
            # just add ID and Title, then move on
            new_row(console_worksheet, [game['ID'], game['Title']])
            continue

        num_files = len(files)
        print(f"Number of files returned: {num_files}")

        # ID, Name, File FileName, MD5, Labels, Patch URL
        for file in files:
            new_row(console_worksheet, [game['ID'], game['Title'], file['Name'], file['MD5'], ",".join(file.get('Labels', '')), file['PatchUrl']])

        # Pause for a short time to avoid hitting the API rate limit
        time.sleep(.5) # 0.5 second pause

    print(f"Games for {system_name} written to Google Sheets successfully.")

def write_header(worksheet):
    try:
        # Clear the worksheet before writing new data
        worksheet.clear()
        worksheet.append_row(['ID', 'Game Name', 'File Name', 'MD5', 'Labels', 'Patch URL'])
    except gspread.exceptions.APIError as e:
        write_header(worksheet)

def new_row(worksheet, data, wait_time=0):
    wait = wait_time * 2  # Double the wait time for each retry - first time is 0 wait
    if wait > 60: # Cap the wait time to 60 seconds
        wait = 60
    time.sleep(wait) # Wait for the specified time

    # Create a new row with the provided data
    try:
        worksheet.append_row(data)  # Append the new row to the worksheet
        print(f"Row added: {data}")
    except gspread.exceptions.APIError as e:
        print(e)
        print(f"API Error, trying again in {(wait_time + 1 * 2)} seconds")
        new_row(worksheet, data, wait_time + 1)

def main():
    # Open the Active Systems sheet
    systems_sheet = sheet.worksheet('Active Systems')

    # Get all systems from the Active Systems sheet
    systems = systems_sheet.get_all_records()

    # Print the systems for the user to choose from
    print("Available systems:")
    for i, system in enumerate(systems):
        print(f"{i}: {system['System Name']}")

    print("-1: All")
    # Which system to get games for?
    system_index = int(input("Enter the index of the system you want to use: "))
    system = systems[system_index]

    if system_index == -1:
        for system in systems:
            get_games(system)
    else:
        get_games(system)

main()