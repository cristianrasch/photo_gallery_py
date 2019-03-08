import unittest

from photo_gallery import models
from photo_gallery import create_app

class ModelsTest(unittest.TestCase):
    def setUp(self):
        self.picture = models.Picture()

    def test_folder_listing(self):
        folders = self.picture.folders()

        self.assertEqual(len(folders), 2)
        self.assertIn('Oxford', folders)
        self.assertIn('Cambridge', folders)

    def test_picture_listing(self):
        srv_name = 'localhost:5000'
        app = create_app({'SERVER_NAME': srv_name})
        folder = 'Oxford'

        with app.app_context():
            pictures = self.picture.from_folder(folder)

        self.assertEqual(len(pictures), 3)
        pic_urls = [str(pic.path) for pic in pictures]
        pics_dir = self.picture.pics_dir
        web_subdir = self.picture.WEB_SUBDIR
        pic_paths = [f'/pictures{self.picture._Picture__strip_pics_dir(path)}' for path in pics_dir.joinpath(folder, web_subdir).glob('*.jpg')]
        # TODO: figure out why URLs gen by url_for start with http:/ instead of
        # http://
        url_prefix = f'http:/{srv_name}'
        for pic_path in pic_paths:
            self.assertIn(f'{url_prefix}{pic_path}', pic_urls)

    def test_thumb_fname_gen(self):
        web_subdir = self.picture.WEB_SUBDIR
        pic = models.Picture(path=self.picture.pics_dir / web_subdir / 'does-not-exist.jpg')

        fname = str(pic.thumb_fname())

        self.assertIn(self.picture.THUMB_SUBDIR, fname)
        self.assertNotIn(web_subdir, fname)
