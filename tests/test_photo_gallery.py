from pathlib import Path
import pytest
import sys

sys.path.insert(0, str(Path(__file__).parent.parent))
from photo_gallery import create_app
from photo_gallery.models import Picture

@pytest.fixture
def client():
    pics_dir = str(Path(__file__).parent / 'fixtures')
    # the TESTING config flag is activated. What this does is disable error
    # catching during request handling, so that you get better error reports
    # when performing test requests against the application
    app = create_app({'TESTING': True, 'PICS_DIR': pics_dir})

    yield app.test_client()


def test_get_root(client):
    res = client.get('/')

    assert res.status_code == 200
    assert b'Oxford' in res.data
    assert b'Cambridge' in res.data


def test_get_oxford(client):
    res = client.get('/Oxford')

    assert res.status_code == 200
    fname = b'p1060100_8840721601_o_opt.jpg'
    assert Picture.WEB_SUBDIR.encode('utf-8') + b'/%s' % fname in res.data
    assert Picture.THUMB_SUBDIR.encode('utf-8') + b'/%s' % fname in res.data


def test_get_cambridge(client):
    res = client.get('/Cambridge')

    assert res.status_code == 200
    fname = b'p1060119_8831916022_o_opt.jpg'
    assert Picture.WEB_SUBDIR.encode('utf-8') + b'/%s' % fname in res.data
    assert Picture.THUMB_SUBDIR.encode('utf-8') + b'/%s' % fname in res.data
