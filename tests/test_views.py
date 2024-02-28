import pytest
from tests.fixtures import client, app

# Note = These are not mocked, meant to act as a E2E tests.
def test_request_example_most_viewed_articles(client):
    response = client.get("/top/most_viewed_articles/201710?limit=10")
    assert response.status_code == 200
    
def test_request_example_view_count_by_article(client):
    response = client.get("/by-article/view_count/Rome?start_timestamp=2015100100&end_timestamp=2015103100")
    assert response.status_code == 200

def test_request_example_date_of_most_views_by_article(client):
    response = client.get("/by-article/date_of_most_views/Nyesom_Wike?start_timestamp=2015100100&end_timestamp=2015103100")
    assert response.status_code == 200

def test_request_example_bad_endpoint(client):
    response = client.get("/top/most_viewed_RANDOM/201710?limit=10")
    assert response.status_code == 404
    response = client.get("/by-article/date_of_moaskjdfh_views/Nyesom_Wike?start_timestamp=2015100100&end_timestamp=2015103100")
    assert response.status_code == 404

def test_request_example_bad_timestamp(client):
    response = client.get("/top/most_viewed_articles/20110?limit=10")
    assert response.status_code == 400
    response = client.get("/by-article/date_of_most_views/Nyesom_Wike?start_timestamp=2011100&end_timestamp=2015100")
    assert response.status_code == 400
    response = client.get("/by-article/view_count/Rome?start_timestamp=2010100&end_timestamp=2015103100")
    assert response.status_code == 400
    