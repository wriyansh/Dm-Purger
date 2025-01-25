# Discord Selfbot DM Purger

This is a Discord selfbot script written in Python using the `discord.py-self` library. The bot allows you to clear direct messages (DMs) with users or group DMs, with the option to set a custom delay between message deletions.

## Features
- **Clear all DMs:** Purge messages in all your DMs with other users or group DMs.
- **Clear a specific DM:** Choose a specific DM or group DM to purge.
- **Custom Delay:** Set a custom delay (in seconds) between message deletions to prevent rate-limiting issues.

## Requirements

To run this bot, you need the following Python libraries:

- `discord.py-self` (for interacting with the Discord API)
- `colorama` (for colored terminal output)

Install the dependencies with:

pip install -r requirements.txt

## Setup

1. Clone the repository or download the script.


2. Replace the placeholder YOUR_TOKEN_HERE with your own Discord selfbot token.


3. Install the required dependencies:



```pip install -r requirements.txt```

4. Run the bot using the following command:

```python bot.py```

## Usage

Once the bot is running:

You will be prompted to choose between clearing all DMs or selecting a specific DM.

For each option, you will be asked if you want to set a custom delay between message deletions.

If you choose all DMs, the bot will iterate through all DMs and delete messages from each user or group DM, based on your confirmation.

If you choose a specific DM, you can select the DM you wish to purge by choosing its number from the list of DMs.


The bot will print logs of its actions in the terminal, showing which messages were deleted and any errors that occurred.

## Credits 

**Discord**

  [@wriyansh](https://discord.com/users/333703596803883018)
  
  [@riyansh.96](https://discord.com/users/642321844170653729)
