import requests


def getPhoto():
    with requests.get("https://inspirobot.me/api?generate=true") as r:
        if not r.ok:
            raise Exception("Invalid Response: Something went wrong")
        return r.text


def getMindfulness():
    with requests.get("https://inspirobot.me/api?generateFlow=1") as r:
        if not r.ok:
            raise Exception("Invalid Response: Something went wrong")
        j = r.json()
        res = {"images": [], "quotes": [],
               "audio": "http://yt.checker.in/utubebot/Censor_BEEP_Sound_Effect_TV_Error_Clip.hd.mp3"}
        for media in j["data"]:
            if not media["type"] == "stop":
                if media["type"] == "transition":
                    res["images"].append("https://source.unsplash.com/{}/1600x900".format(media["image"]))
                elif media["type"] == "quote":
                    res["quotes"].append(
                        media["text"].replace("[pause 1].", "\n").replace("[pause 2].", "\n").replace("[pause 3].",
                                                                                                      "\n"))
        res["audio"] = j["mp3"]
        return res
