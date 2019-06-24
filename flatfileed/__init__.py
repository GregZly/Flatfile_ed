import os

from flask import Flask

def create_app(test_config=None):
    #create and configure application
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY = 'dev'
    )

    if test_config is None:
        #Load instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        #Load the test config if passed in
        app.config.from_mapping(test_config)
    
    #ensure the instantce folder exist
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    
    #hello page for test
    @app.route('/hello')
    def hello():
        return "Hello World"
    
    from . import flatfile_operations
    with app.app_context():
        app.register_blueprint(flatfile_operations.bp)

    return app