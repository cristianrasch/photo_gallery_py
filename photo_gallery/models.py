from datetime import date
from functools import lru_cache
from pathlib import Path

from flask import current_app, url_for

class Picture:
    WEB_SUBDIR = 'web'
    THUMB_SUBDIR = 'thumb'

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

    # /Berlin_I/p1080757_12566647374_o_opt.jpg =>
    #   /Berlin_I/web/p1080757_12566647374_o_opt.jpg
    @classmethod
    def web_pic_path(cls, pic_path):
        path = Path(str(pic_path).replace(str(cls.pics_dir()), ''))
        return path.parent / cls.WEB_SUBDIR / path.name

    @classmethod
    @lru_cache(maxsize=1)
    def from_folder(cls, folder):
        if folder not in cls.folders(): return []

        pics = []
        pics_dir = cls.pics_dir()
        folder_dir = pics_dir / folder
        for ext in cls.photo_exts():
            pics.extend(folder_dir.glob(f'*.{ext}'))

        pics.sort(key=lambda path: [path.stat().st_mtime, path.name])

        return [cls(url_for('picture', picture=cls.web_pic_path(pic))) for pic in pics]

    def __init__(self, path):
        self.path = Path(path)

    def thumb_fname(self):
        return self.path.parent.with_name(self.THUMB_SUBDIR) / self.path.name
