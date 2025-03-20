# RA-Game-List
A script to get a list of supported game file names and hashes from RetroAchievements. This script does not provide access to any copyrighted game files. 

## Prerequisites 

Install the following packages: 

- `pip install gspread`
- `pip install dotenv`

Add your RetroAchievements API key and your Google Sheets key to the .env file. View the [gspread docs](https://docs.gspread.org/en/latest/oauth2.html) for more information about settings up Google Sheets. Refer to the [RetroAchievements API documentation](https://api-docs.retroachievements.org/) for more information on obtaining your API key. 

## Instructions

First, run the `get_systems.py` script. This will be a good test to ensure you have your API keys and Google account set up properly. This script will populate a sheet with the IDs and Names of each console that is considered "Active" on RetroAchievements. 

Next, run the `get_games.py` script. This can take significantly longer, depending on which console you want to get game information for. If getting information for all games, you should probably expect to leave your computer running overnight. 

## Limitations

The Google Sheet API has strict API rate-limits in place. You can only make 60 reads and 60 writes per minute. The script has some built-in `time.sleep()` calls to help slow it down but it will still occasionally get rate limited. When that happens, the script has an additional `time.sleep()` pause that waits longer each time it gets called. 

The `get_games.py` does not handle updates. Each time it runs, it will clear the sheet and re-import all games from RetroAchievements. 

## Roadmap

- I plan to update the script so it can handle adding new games without deleting everything first. 
- I also plan to add a version that writes to a local spreadsheet instead of using Google Sheets. Google's rate limiting slows this down significantly.  