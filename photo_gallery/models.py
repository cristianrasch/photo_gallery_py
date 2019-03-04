from datetime import date
from functools import lru_cache
from pathlib import Path

from flask import current_app

class Picture:
    @classmethod
    @lru_cache(maxsize=1)
    def pics_dir(cls):
        return Path(current_app.config['PICS_DIR']).expanduser()

    @classmethod
    @lru_cache(maxsize=1)
    def photo_exts(cls):
        return current_app.config['PHOTO_EXTS']

    @classmethod
    @lru_cache(maxsize=1)
    def folders(cls):
        return sorted([f.name for f in cls.pics_dir().iterdir() if f.is_dir() and
                                                                   f.name[0].isupper() and
                                                                   any(ext for ext in cls.photo_exts() if f.glob(f'*.{ext}'))])
