"""
Luke Marshall's Flask API.
"""

from flask import Flask, abort, send_from_directory

app = Flask(__name__)


import os
import configparser

# config parser to find the port and debug mode from the config file
def parse_config(config_paths):
    """From project 0"""
    config_path = None
    for file in config_paths:
        if os.path.isfile(file):
            config_path = file
            break

    if config_path is None:
        raise RuntimeError("Configuration file not found!")

    config = configparser.ConfigParser()
    config.read(config_path)
    return config

# collect port and debug mode from the config file
config = parse_config(["credentials.ini", "default.ini"])
PORT = config["SERVER"]["PORT"]
DEBUG = config["SERVER"]["DEBUG"]


@app.route("/<string:filename>")
def serve(filename):
    if '~' in filename or '..' in filename: # check for illegal characters
        abort(403)
    path = f"pages/{filename}"
    if path != "pages/" and os.path.exists(path):
        # check the path exits and that is not just the directory 'pages' 
        return send_from_directory('pages/', filename)
    elif path == "pages/" or not os.path.exists(path):
        # check for nonexistent path or empty filename
        abort(404)
    return "This should not be shown, something went wrong during file checking\n"

@app.errorhandler(403)
def handle_illegal_characters(e):
    return send_from_directory('pages/', '403.html'), 403

@app.errorhandler(404)
def handle_nonexistent_page(e):
    return send_from_directory('pages/', '404.html'), 404

if __name__ == "__main__":
    app.run(debug=DEBUG, host='0.0.0.0', port=PORT)
