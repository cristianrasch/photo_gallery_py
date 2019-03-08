from pathlib import Path

PICS_DIR = str(Path(__file__).with_name('photo_gallery').joinpath('tests', 'fixtures'))
PHOTO_EXTS = 'jpg,jpeg'.split(',')
BASIC_AUTH_USERNAME = 'root'
BASIC_AUTH_PASSWORD = 'changeme'
# If you would like to protect you entire site with basic access authentication,
# just set BASIC_AUTH_FORCE configuration variable to True:
BASIC_AUTH_FORCE = False
# ASSETS_DEBUG = True
