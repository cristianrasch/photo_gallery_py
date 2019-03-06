photo_gallery
=============

dev setup instructions
----------------------

1. Install dependencies

`pip install -r requirements.txt`

2. Configure your pictures path (defaults to ~/Pictures)

`mkdir instance && echo "PICS_DIR = '/path/to/pictures'" > instance/config.py`

3. Install the app locally so that the tests can find the app pkg

`pip install -e .`

4. Run the test suite to verify everything is OK

`pytest`

5. Run the dev server (listens on localhost:5000)

`FLASK_ENV=development FLASK_APP=photo_gallery flask run`

TODO
----

1. Deploy with Fabric
