from functools import lru_cache
from pathlib import Path

from flask import url_for

class Picture:
    WEB_SUBDIR = 'web'
    THUMB_SUBDIR = 'thumb'

    def __init__(self, pics_dir=Path(__file__).with_name('tests').joinpath('fixtures'),
                       photo_exts=['jpg', 'jpeg'],
                       path=None):
        self.pics_dir = Path(pics_dir).expanduser().resolve()
        self.photo_exts = photo_exts
        self.path = path and Path(path)

    @lru_cache(maxsize=1)
    def folders(self):
        return sorted([f.name for f in self.pics_dir.iterdir() if f.is_dir() and
                                                                  f.name[0].isupper() and
                                                                  any(ext for ext in self.photo_exts if (f / self.WEB_SUBDIR).glob(f'*.{ext}')) and
                                                                  any(ext for ext in self.photo_exts if (f / self.THUMB_SUBDIR).glob(f'*.{ext}'))])

    # ~/Pictures/Personal/Berlin_I/p1080757_12566647374_o_opt.jpg =>
    #   /Berlin_I/web/p1080757_12566647374_o_opt.jpg
    def _strip_pics_dir(self, pic_path):
        return str(pic_path).replace(str(self.pics_dir), '')

    @lru_cache()
    def from_folder(self, folder):
        if folder not in self.folders(): return []

        pics = []
        folder_dir = self.pics_dir / folder / self.WEB_SUBDIR
        for ext in self.photo_exts:
            pics.extend(folder_dir.glob(f'*.{ext}'))

        pics.sort(key=lambda path: [path.stat().st_mtime, path.name])

        return [self.__class__(path=url_for('picture', picture=self._strip_pics_dir(pic))) for pic in pics]

    def thumb_fname(self):
        return self.path.parent.with_name(self.THUMB_SUBDIR) / self.path.name
