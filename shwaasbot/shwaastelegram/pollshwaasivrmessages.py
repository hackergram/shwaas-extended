
import os
from shwaastg.shwaastgbot import *


if __name__ == "__main__":
    while True:
        call_list = os.listdir("/opt/voiceofhimalaya/calls")
        call_list.remove("calllog")
        for call in call_list:
            files = os.listdir(os.path.join("/opt/voiceofhimalaya/calls", call))
            if "telegramed" in files:
                continue
            for fn in files:
                if ".wav" in fn:
                    shwaastgbot.updater.bot.send_audio(-456601244, open(
                        os.path.join("/opt/voiceofhimalaya/calls", call, fn), "rb"), caption=call)
                    with open(os.path.join(os.path.join("/opt/voiceofhimalaya/calls", call, "telegramed")), "w") as f:
                        f.write("Telegramed")
        xpal.shwaastgbotxpal.wait()
