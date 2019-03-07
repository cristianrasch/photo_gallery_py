import unittest
from pathlib import Path

from photo_gallery import create_app
from photo_gallery.models import Picture

class ViewsTest(unittest.TestCase):
    def setUp(self):
        pics_dir = str(Path(__file__).parent / 'fixtures')
        app = create_app({'TESTING': True, 'PICS_DIR': pics_dir})
        self.app = app.test_client()

    def test_get_root(self):
        res = self.app.get('/')

        self.assertEqual(res.status_code, 200)
        self.assertIn(b'Oxford', res.data)
        self.assertIn(b'Cambridge', res.data)

    def test_get_oxford(self):
        res = self.app.get('/Oxford')

        self.assertEqual(res.status_code, 200)
        fname = b'p1060100_8840721601_o_opt.jpg'
        self.assertIn(Picture.WEB_SUBDIR.encode('utf-8') + b'/%s' % fname, res.data)
        self.assertIn(Picture.THUMB_SUBDIR.encode('utf-8') + b'/%s' % fname, res.data)


    def test_get_cambridge(self):
        res = self.app.get('/Cambridge')

        self.assertEqual(res.status_code, 200)
        fname = b'p1060119_8831916022_o_opt.jpg'
        self.assertIn(Picture.WEB_SUBDIR.encode('utf-8') + b'/%s' % fname, res.data)
        self.assertIn(Picture.THUMB_SUBDIR.encode('utf-8') + b'/%s' % fname, res.data)
