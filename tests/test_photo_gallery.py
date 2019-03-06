from pathlib import Path
import pytest
import sys

sys.path.insert(0, str(Path(__file__).parent.parent))
from photo_gallery import create_app
from photo_gallery.models import Picture

@pytest.fixture
def client():
    # the TESTING config flag is activated. What this does is disable error
    # catching during request handling, so that you get better error reports
    # when performing test requests against the application
    pics_dir = str(Path(__file__).parent / 'fixtures')
    app = create_app({'TESTING': True, 'PICS_DIR': pics_dir})
    client = app.test_client()

    yield client


def test_get_root(client):
    rv = client.get('/')
    assert b'Oxford' in rv.data
    assert b'Cambridge' in rv.data


def test_get_oxford(client):
    rv = client.get('/Oxford')
    fname = b'p1060100_8840721601_o_opt.jpg'
    assert Picture.WEB_SUBDIR.encode('utf-8') + b'/%s' % fname in rv.data
    assert Picture.THUMB_SUBDIR.encode('utf-8') + b'/%s' % fname in rv.data


def test_get_cambridge(client):
    rv = client.get('/Cambridge')
    fname = b'p1060119_8831916022_o_opt.jpg'
    assert Picture.WEB_SUBDIR.encode('utf-8') + b'/%s' % fname in rv.data
    assert Picture.THUMB_SUBDIR.encode('utf-8') + b'/%s' % fname in rv.data
