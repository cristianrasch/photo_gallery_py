import pytest

from photo_gallery import create_app
from photo_gallery.models import Picture

@pytest.fixture
def client():
    app = create_app({'TESTING': True})
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
