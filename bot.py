import discord
import os
import webbrowser
import subprocess
from pathlib import Path

# Enable intents for message content
intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

current_directory = Path.home()  # Start with user's home directory


@client.event
async def on_ready():
    print(f'Bot logged in as {client.user}')


@client.event
async def on_message(message):
    global current_directory

    # Ignore messages from the bot itself
    if message.author == client.user:
        return

    # Command: !open <app>
    if message.content.startswith('!open '):
        app_name = message.content[len('!open '):].strip()
        try:
            os.system(f'start {app_name}')
            await message.channel.send(f'Attempting to open {app_name}...')
        except Exception as e:
            await message.channel.send(f'Error opening {app_name}: {e}')

    # Command: !cmd <command>
    elif message.content.startswith('!cmd '):
        cmd_command = message.content[len('!cmd '):].strip()
        try:
            # Open a new Command Prompt window and run the command
            subprocess.Popen(f'start cmd /k {cmd_command}', shell=True)
            await message.channel.send(f'Opening Command Prompt to execute: `{cmd_command}`')
        except Exception as e:
            await message.channel.send(f'Error executing command: {e}')

    # Command: !search <query>
    elif message.content.startswith('!search '):
        query = message.content[len('!search '):].strip()
        try:
            webbrowser.open(f'https://www.google.com/search?q={query}')
            await message.channel.send(f'Searching for "{query}"...')
        except Exception as e:
            await message.channel.send(f'Error performing search: {e}')

    # Command: !files
    elif message.content == '!files':
        try:
            files = list(current_directory.iterdir())
            response = "\n".join(
                [f"{i}. {'(FOLDER) ' if f.is_dir() else ''}{f.name}" for i, f in enumerate(files)]
            )
            await message.channel.send(f'Files in `{current_directory}`:\n```{response}```\n'
                                       f'Type `!file <number>` to open a file or folder.')
        except Exception as e:
            await message.channel.send(f'Error listing files: {e}')

    # Command: !file <number>
    elif message.content.startswith('!file '):
        try:
            index = int(message.content[len('!file '):].strip())
            files = list(current_directory.iterdir())
            selected = files[index]
            if selected.is_dir():
                current_directory = selected  # Change directory
                files = list(current_directory.iterdir())
                response = "\n".join(
                    [f"{i}. {'(FOLDER) ' if f.is_dir() else ''}{f.name}" for i, f in enumerate(files)]
                )
                await message.channel.send(f'Files in `{current_directory}`:\n```{response}```\n'
                                           f'Type `!file <number>` to open a file or folder.')
            else:
                os.startfile(selected)
                await message.channel.send(f'Opening file: {selected.name}')
        except Exception as e:
            await message.channel.send(f'Error accessing file or folder: {e}')


TOKEN = 'ENTER_TOKEN_HERE'
client.run(TOKEN)




