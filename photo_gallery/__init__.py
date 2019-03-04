import os
import itertools

from flask import Flask, render_template, url_for

from .models import Picture

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)

    app.config.from_object('settings')
    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route("/")
    def index():
        css_classses = itertools.cycle(['primary', 'secondary', 'success',
                                        'danger', 'warning', 'info', 'light',
                                        'dark'])
        folders_and_classes = zip(Picture.folders(), css_classses)

        return render_template('index.html',
                               folders_and_classes=folders_and_classes)

    @app.route("/<folder>")
    def folder(folder):
        return folder
        # return render_template('show.html', folder=folder)

    return app
