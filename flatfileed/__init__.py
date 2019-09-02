import os
from pathlib import Path

from flask import Flask

def create_app(test_config=None):
    #create and configure application
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY = 'devvvv'
    )
    
    config_file = Path(app.root_path) / "config.py"

    if test_config is None:
        #Load instance config, if it exists, when not testing
        app.config.from_pyfile(config_file,silent=True)
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
    from . import backup_operations
    from . import scp_interface
    with app.app_context():
        app.register_blueprint(flatfile_operations.bp)
        app.register_blueprint(backup_operations.bp)
        app.register_blueprint(scp_interface.bp)

    return app