from typing import Union, Tuple

import requests


class Inspiro:
    def __init__(self):
        self.__author__ = "https://github.com/GodSaveTheDoge"
        self._SCHEMA = "https"
        self._HOST = "inspirobot.me"
        self.base_url = "{}://{}".format(self._SCHEMA, self._HOST)

        self.image_url = self.base_url + "/api?generate=true"
        self.audio_url = self.base_url + "/api?generateFlow=1"

    def generate_image(self) -> str:
        """Return url to an image."""
        return requests.get(self.image_url).text

    def generate_audio(self, text: bool = False, joiner: str = "\n") -> Union[str, Tuple[str, str]]:
        """
        Return url to audio if text is False.
        Return tuple like (url, subtitles) if text is True.
        """
        if text:
            r_json = requests.get(self.audio_url).json()
            return (
                r_json["mp3"], joiner.join(
                    [segment['text'].replace('[pause 1]', '').replace('[pause 2]', '') for segment in r_json['data'] if
                     'text' in segment.keys()]))
        else:
            return requests.get(self.audio_url).json()['mp3']

    def generate_video(self):
        """Work in progress."""
        pass  # TODO do this


Inspiro = Inspiro()
