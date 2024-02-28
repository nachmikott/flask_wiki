import pytest
from flaskr.response_model_class import Response, Item
from flask import Flask
from app import create_app


class SimpleRequestResponse:
    def raise_for_status(self):
        if self.throw_exception:
            raise Exception()
        else:
            return None

    def __init__(self, text, throw_exception=False):
        self.text = text
        self.throw_exception=throw_exception

@pytest.fixture()
def app():
    app = create_app()
    app.config.update({
        "TESTING": True,
    })

    # other setup can go here

    yield app

    # clean up / reset resources here

@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def runner(app):
    return app.test_cli_runner()

@pytest.fixture
def proper_top_response_dict():
    return {
        "items": [
            {
                "project": "en.wikisource",
                "access": "all-access",
                "year": "2015",
                "month": "10",
                "day": "01",
                "articles": [
                    {
                        "article": "Main_Page",
                        "views": 2787,
                        "rank": 1
                    },
                    {
                        "article": "Special:Search",
                        "views": 1361,
                        "rank": 2
                    },
                    {
                        "article": "Dictionary_of_Spoken_Russian/English-Russian",
                        "views": 1087,
                        "rank": 3
                    }
                ]
            }
        ]
    }

@pytest.fixture
def proper_per_article_response_dict():
    return {
        "items": [
            {
                "project": "en.wikipedia",
                "article": "Albert_Einstein",
                "granularity": "daily",
                "timestamp": "2015100100",
                "access": "all-access",
                "agent": "all-agents",
                "views": 18860
            },
            {
                "project": "en.wikipedia",
                "article": "Albert_Einstein",
                "granularity": "daily",
                "timestamp": "2015100200",
                "access": "all-access",
                "agent": "all-agents",
                "views": 20816
            }
        ]
    }

@pytest.fixture
def improper_response_dict():
    return { "This": "Is Not A Response!" }

@pytest.fixture
def expected_top_response_object(proper_top_response_dict):
    articles = proper_top_response_dict['items'][0]['articles']
    items=[]
    for article_item in articles:
        items.append(Item(article=article_item['article'], views=article_item['views']))
    return Response(items=items)


@pytest.fixture
def expected_per_article_response_object(proper_per_article_response_dict):
    articles = proper_per_article_response_dict['items']
    items=[]
    for article_item in articles:
        items.append(Item(article=article_item['article'], views=article_item['views']))
    return Response(items=items)