
import os
from shwaastg.shwaastgbot import *
import time

if __name__ == "__main__":
    while True:
        shwaastgbot.logger.info("Cycle")
        try:
            call_list = os.listdir("/opt/voiceofhimalaya/calls")
            call_list.remove("calllog")
            for call in call_list:
                files = os.listdir(os.path.join(
                    "/opt/voiceofhimalaya/calls", call))
                if "telegramed" in files:
                    shwaastgbot.logger.info("Ignoring {}".format(call))
                    continue
                for fn in files:
                    if ".wav" in fn:
                        shwaastgbot.logger.info(
                            "Trying to upload {}".format(call))
                        shwaastgbot.updater.bot.send_audio(-456601244, open(
                            os.path.join("/opt/voiceofhimalaya/calls", call, fn), "rb"), caption=call)
                        with open(os.path.join(os.path.join("/opt/voiceofhimalaya/calls", call, "telegramed")), "w") as f:
                            f.write("Telegramed")
                        shwaastgbot.logger.info(
                            "Successfully uploaded {}".format(call))
        except Exception as e:
            shwaastgbot.logger.error("{} {}".format(str(e), repr(e)))
        time.sleep(600)
