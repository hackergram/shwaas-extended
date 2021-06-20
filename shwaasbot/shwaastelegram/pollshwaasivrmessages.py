
import os
from shwaastg.shwaastgbot import *
import time

if __name__ == "__main__":
    while True:
        shwaastgbot.logger.info("Cycle")
        activecalls = os.popen("asterisk -x 'core show channels verbose' | grep 'active calls'").read().strip()
        if activecalls != "0 active calls":
            shwaastgbot.logger.info("Skipping cycle since call in progress")
            time.sleep(180)
            continue
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
                            os.path.join("/opt/voiceofhimalaya/calls", call, fn), "rb"), caption=call, timeout=300)
                        with open(os.path.join(os.path.join("/opt/voiceofhimalaya/calls", call, "telegramed")), "w") as f:
                            f.write("Telegramed")
                        shwaastgbot.logger.info(
                            "Successfully uploaded {}".format(call))
        except Exception as e:
            shwaastgbot.logger.error("{} {}".format(str(e), repr(e)))
        time.sleep(180)
