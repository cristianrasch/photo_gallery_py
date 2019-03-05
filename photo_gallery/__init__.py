import os
import itertools

from flask import Flask, render_template, url_for, abort, send_from_directory, request

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

    if app.config['ENV'] not in ['development', 'test']:
        from flask_basicauth import BasicAuth
        basic_auth = BasicAuth(app)

    @app.route("/")
    # @basic_auth.required
    def index():
        css_classses = itertools.cycle(['primary', 'secondary', 'success',
                                        'danger', 'warning', 'info', 'light',
                                        'dark'])
        folders_and_classes = zip(Picture.folders(), css_classses)

        return render_template('index.html',
                               folders_and_classes=folders_and_classes)

    @app.route("/<folder>")
    # @basic_auth.required
    def folder(folder):
        pictures = Picture.from_folder(folder)
        return_to = request.referrer or url_for('/')
        return render_template('show.html', pictures=pictures,
                                            return_to=return_to)

    # /pictures/Berlin_I/web/p1080757_12566647374_o_opt.jpg
    # /pictures/Berlin_I/thumb/p1080757_12566647374_o_opt.jpg
    @app.route("/pictures/<path:picture>")
    def picture(picture):
        if app.config['ENV'] == 'development':
            pics_dir = Picture.pics_dir()
            pic_path = pics_dir / picture

            if pic_path.exists():
                return send_from_directory(pics_dir, picture)
            else:
                abort(404)
        else:
            abort(404)

    return app
