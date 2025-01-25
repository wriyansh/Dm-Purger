import discord
from discord.ext import commands
import asyncio
import time
from colorama import Fore, Style, init

init(autoreset=True)

TOKEN = ''

client = discord.Client()

DEFAULT_DELAY = 0.5


def current_timestamp():
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())


def print_message(message, color=Fore.WHITE):
    print(f"{color}[{current_timestamp()}] {message}{Style.RESET_ALL}")


@client.event
async def on_ready():
    print_message(f"Logged in as {client.user}", Fore.GREEN)
    print_message("Choose an option:", Fore.CYAN)
    print_message("1. Clear all DMs", Fore.YELLOW)
    print_message("2. Clear a specific DM (dynamic selection)", Fore.YELLOW)
    
    choice = input(f"{Fore.GREEN}Enter your choice (1/2): ").strip()

    if choice == "1":
        await clear_all_dms()
    elif choice == "2":
        await select_specific_dm()
    else:
        print_message("Invalid choice. Exiting...", Fore.RED)
        await client.close()


async def clear_all_dms():
    print_message("Fetching all DM channels...", Fore.CYAN)
    dms = client.private_channels

    custom_delay_input = input(f"{Fore.GREEN}Do you want to set a custom delay for message deletions? (y/n): ").strip().lower()

    if custom_delay_input == "y":
        delay = input(f"{Fore.GREEN}Enter the delay (in seconds): ").strip()
        try:
            delay = float(delay)
            if delay <= 0:
                print_message("Invalid delay value. Using default delay.", Fore.YELLOW)
                delay = DEFAULT_DELAY
        except ValueError:
            print_message("Invalid delay input. Using default delay.", Fore.YELLOW)
            delay = DEFAULT_DELAY
    else:
        delay = DEFAULT_DELAY

    print_message(f"Using a delay of {delay} seconds between deletions.", Fore.GREEN)

    tasks = []
    for dm in dms:
        if isinstance(dm, discord.DMChannel):  # Personal DM
            confirm = input(f"{Fore.YELLOW}Do you want to purge DM with {dm.recipient}? (y/n): ").strip().lower()
            if confirm == 'y':
                tasks.append(purge_user_dm(dm, delay))
        elif isinstance(dm, discord.GroupChannel):  # Group DM
            confirm = input(f"{Fore.YELLOW}Do you want to purge Group DM: {dm.name}? (y/n): ").strip().lower()
            if confirm == 'y':
                tasks.append(purge_group_dm(dm, delay))

    if tasks:
        await asyncio.gather(*tasks)
    else:
        print_message("No DMs selected for purging.", Fore.RED)

    print_message("All selected DMs have been purged.", Fore.GREEN)
    await client.close()


async def select_specific_dm():
    print_message("Fetching all DM channels...", Fore.CYAN)
    dms = client.private_channels

    for index, dm in enumerate(dms, start=1):
        dm_name = dm.name if isinstance(dm, discord.GroupChannel) else dm.recipient
        print_message(f"{index}. {dm_name} (ID: {dm.id})", Fore.YELLOW)

    choice = input(f"{Fore.GREEN}Enter the number corresponding to the DM you want to clear: ").strip()

    try:
        choice = int(choice)
        selected_dm = dms[choice - 1]

        custom_delay_input = input(f"{Fore.GREEN}Do you want to set a custom delay for message deletions? (y/n): ").strip().lower()
        if custom_delay_input == "y":
            delay = input(f"{Fore.GREEN}Enter the delay (in seconds): ").strip()
            try:
                delay = float(delay)
                if delay <= 0:
                    print_message("Invalid delay value. Using default delay.", Fore.YELLOW)
                    delay = DEFAULT_DELAY
            except ValueError:
                print_message("Invalid delay input. Using default delay.", Fore.YELLOW)
                delay = DEFAULT_DELAY
        else:
            delay = DEFAULT_DELAY

        print_message(f"Using a delay of {delay} seconds for the selected DM.", Fore.GREEN)

        if isinstance(selected_dm, discord.DMChannel):
            await purge_user_dm(selected_dm, delay)
        elif isinstance(selected_dm, discord.GroupChannel):
            await purge_group_dm(selected_dm, delay)
        else:
            print_message("Invalid choice.", Fore.RED)
    except (IndexError, ValueError):
        print_message("Invalid input. Please enter a valid number.", Fore.RED)

    await client.close()


async def purge_user_dm(dm, delay):
    try:
        print_message(f"Purging messages in DM with {dm.recipient}...", Fore.CYAN)
        async for message in dm.history(limit=None):
            if message.author == client.user:
                try:
                    await message.delete()
                    print_message("Deleted a message.", Fore.GREEN)
                except Exception as e:
                    print_message(f"Failed to delete a message: {e}", Fore.RED)
                await asyncio.sleep(delay)  # Customizable delay

        await dm.delete()
        print_message(f"Closed DM with {dm.recipient}.", Fore.GREEN)
    except Exception as e:
        print_message(f"Failed to process DM with {dm.recipient}: {e}", Fore.RED)


async def purge_group_dm(dm, delay):
    try:
        print_message(f"Purging messages in Group DM: {dm.name}...", Fore.CYAN)
        async for message in dm.history(limit=None):
            if message.author == client.user:
                try:
                    await message.delete()
                    print_message("Deleted a message.", Fore.GREEN)
                except Exception as e:
                    print_message(f"Failed to delete a message: {e}", Fore.RED)
                await asyncio.sleep(delay)  # Customizable delay

        await dm.leave()
        print_message(f"Left Group DM: {dm.name}.", Fore.GREEN)
    except Exception as e:
        print_message(f"Failed to process Group DM: {e}", Fore.RED)


client.run(TOKEN)
