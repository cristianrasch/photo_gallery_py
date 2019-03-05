import logging
from logging.handlers import TimedRotatingFileHandler
import itertools
from pathlib import Path

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
    Path(app.instance_path).mkdir(parents=True, exist_ok=True)

    log_dir = Path(__file__).parent.parent / 'log'
    log_dir.mkdir(exist_ok=True)
    fname = log_dir / 'photo_gallery.log'
    log_handler = TimedRotatingFileHandler(filename=fname, when='d',
                                          backupCount=7)
    app.logger.setLevel(logging.ERROR)
    app.logger.addHandler(log_handler)

    if app.config['ENV'] not in ['development', 'test']:
        from flask_basicauth import BasicAuth
        basic_auth = BasicAuth(app)

    @app.errorhandler(500)
    def internal_server_error(error):
        app.logger.error(error, error.__traceback__)
        return str(error), 500

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
        return_to = request.referrer or url_for('index')
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
