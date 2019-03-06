photo_gallery
=============

dev setup instructions
----------------------

1. Clone the project

`git clone git@github.com:cristianrasch/photo_gallery_py.git`

2. Create a new virtual environment for it

`cd photo_gallery_py && python3 -m venv venv`

3. Install its dependencies

`pip install -r requirements.txt`

4. Install the app locally so that the Werkzeug dev server and the test runner
   can find the app pkg

`pip install -e .`

5. Run the test suite to make sure everything is set up OK

`pytest`

6. Configure your pictures path [OPTIONAL]

`mkdir instance && echo "PICS_DIR = '/path/to/pictures'" > instance/config.py`

(defaults to /path/to/app/tests/fixtures)

8. Run the dev server (listens on localhost:5000)

`FLASK_ENV=development FLASK_APP=photo_gallery flask run`

TODO
----

1. Deploy with Fabric
