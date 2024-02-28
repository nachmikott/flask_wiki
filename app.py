from flask import Flask, jsonify, request
from flaskr.utils import *
from flaskr.per_article_view import PartArticleView
from flaskr.top_articles_view import TopArticlesView
from flask_swagger_ui import get_swaggerui_blueprint


def create_app():
    app = Flask(__name__)

    @app.route("/")
    def root():
        return "Hello, This is the Root Route"

    # Ex/ http://127.0.0.1:5000/by-article/date_of_most_views/Nyesom_Wike?start_timestamp=2015100100&end_timestamp=2015103100
    # Ex/ http://127.0.0.1:5000/by-article/view_count/Nyesom_Wike?start_timestamp=2015100100&end_timestamp=2015103100
    app.add_url_rule("/by-article/<string:func>/<string:article>", view_func=PartArticleView.as_view("per_article"))

    # Ex/ http://127.0.0.1:5000/top/most_viewed_articles/201510?limit=10
    app.add_url_rule("/top/<string:func>/<string:timestamp>", view_func=TopArticlesView.as_view("per_top"))

    SWAGGER_URL="/swagger"
    API_URL="/static/swagger.json"
    swagger_ui_blueprint = get_swaggerui_blueprint(
        SWAGGER_URL,
        API_URL,
        config={
            'app_name': 'FlaskWiki API'
        }
    )
    app.register_blueprint(swagger_ui_blueprint, url_prefix=SWAGGER_URL)

    return app

create_app()