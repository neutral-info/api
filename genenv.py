import os
import socket
import subprocess
from configparser import ConfigParser

label = str(subprocess.check_output(["git", "tag", "-l"]).strip())
label = label.split("\\n")[-1].replace("'", "")

HOST_NAME = socket.gethostname()

local_config = ConfigParser()
local_config.read("local.ini")
if os.environ.get("VERSION", ""):
    section = local_config[os.environ.get("VERSION", "")]
elif HOST_NAME in local_config:
    section = local_config[HOST_NAME]
else:
    section = local_config["DEFAULT"]

env_content = "HOSTNAME={}\nVERSION={}\n".format(
    HOST_NAME, label
    )
for sec in section:
    env_content += "{}={}\n".format(sec.upper(), section[sec])

with open(".env", "w", encoding="utf8") as env:
    env.write(env_content)
