from photo_gallery import create_app

app = create_app()

# uwsgi --socket 0.0.0.0:5000 --protocol=http -w wsgi:app
if __name__ == '__main__':
    app.run()
