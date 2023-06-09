from flask import Flask
from storage.bucket import bucket_blueprint

# FMF
from helpers.middleware import setup_metrics

app = Flask(__name__, static_url_path="", static_folder="../static")
app.config.from_object(__name__)
app.register_blueprint(bucket_blueprint, url_prefix="/api")

# FMF
setup_metrics(app)