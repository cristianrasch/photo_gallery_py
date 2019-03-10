import logging
from logging.handlers import TimedRotatingFileHandler
import itertools
from pathlib import Path
import os

from flask import Flask, render_template, url_for, abort, send_from_directory, request
from flask_assets import Environment, Bundle

from .models import Picture

# A handler for “500 Internal Server Error” will not be used when running
# in debug mode. Instead, the interactive debugger will be shown
def internal_server_error(error):
    return str(error), 500


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object('settings')
    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    Path(app.instance_path).mkdir(parents=True, exist_ok=True)

    app_pkg_dir = Path(__file__).parent
    pids_dir = app_pkg_dir.with_name('tmp') / 'pids'
    pids_dir.mkdir(parents=True, exist_ok=True)
    pids_dir.joinpath(f'{__name__}.pid').write_text(str(os.getpid()))


    def pic():
        return Picture(app.config['PICS_DIR'], app.config['PHOTO_EXTS'])


    log_dir = app_pkg_dir.with_name('log')
    log_dir.mkdir(exist_ok=True)
    fname = log_dir / 'photo_gallery.log'
    log_handler = TimedRotatingFileHandler(filename=fname, when='d',
                                          backupCount=7)
    app.logger.setLevel(logging.ERROR)
    app.logger.addHandler(log_handler)
    app.register_error_handler(500, internal_server_error)


    if app.config['ENV'] not in ['development', 'test']:
        from flask_basicauth import BasicAuth
        basic_auth = BasicAuth(app)


    assets = Environment()
    js_libs = ['jquery', 'popper', 'bootstrap', 'unitegallery', 'ug-theme-tiles']
    js_libs = [f'js/{js_lib}.js' for js_lib in js_libs]
    js = Bundle(*js_libs, filters='jsmin', output='js/js_all.js')
    assets.register('js_all', js)
    css_libs = ['bootstrap', 'style', 'unite-gallery']
    css_libs = [f'css/{css_lib}.css' for css_lib in css_libs]
    css = Bundle(*css_libs, filters='cssmin', output='css/css_all.css')
    assets.register('css_all', css)
    assets.init_app(app)


    @app.route("/")
    # @basic_auth.required
    def index():
        return render_template('index.html', folders=pic().folders())

    @app.route("/<folder>")
    # @basic_auth.required
    def folder(folder):
        pictures = pic().from_folder(folder)
        return_to = request.referrer or url_for('index')
        return render_template('show.html', pictures=pictures,
                                            return_to=return_to)

    # /pictures/Berlin_I/web/p1080757_12566647374_o_opt.jpg
    # /pictures/Berlin_I/thumb/p1080757_12566647374_o_opt.jpg
    @app.route("/pictures/<path:picture>")
    def picture(picture):
        if app.config['ENV'] == 'development':
            pics_dir = pic().pics_dir
            pic_path = pics_dir / picture

            if pic_path.exists():
                return send_from_directory(pics_dir, picture)
            else:
                abort(404)
        else:
            abort(404)

    return app
