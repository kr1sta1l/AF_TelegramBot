import os
import json
from pathlib import Path
from src.config import config


class Localizer:
    def __init__(self, path: Path):
        self.localizations = {}
        self.available_languages = config.AVAILABLE_LANGUAGES.split("|")
        self.default_language = config.DEFAULT_LANGUAGE

        self._load_localizations(path)

    def _load_localizations(self, path: Path):
        # прочитать все паки в папке
        for lang in self.available_languages:
            with open(path / f"{lang}.json", "r") as f:
                self.localizations[lang] = json.load(f)


localizer = Localizer(Path(os.path.realpath(Path(os.path.dirname(os.path.realpath(__file__))) / config.LOCALIZER_PATH)))
