from flaskr.wikipedia_api import call_get_page_views_by_article
from tests.fixtures import proper_per_article_response_dict, SimpleRequestResponse
import pytest
import json

### call_get_page_views_by_article ###

def test_call_page_view_by_article(mocker, proper_per_article_response_dict):
    mocker.patch('flaskr.wikipedia_api.requests.get', return_value=SimpleRequestResponse(text=json.dumps(proper_per_article_response_dict)))
    assert call_get_page_views_by_article('123').raise_for_status() is None # No Error
    assert call_get_page_views_by_article('123').text == json.dumps(proper_per_article_response_dict)

def test_call_page_view_by_article_bad_timestamps(mocker):
    mocker.patch('flaskr.wikipedia_api.validate_timestamp', side_effect=Exception('Any Error'))
    with pytest.raises(Exception, match='Any Error'):
        call_get_page_views_by_article('123')

### call_get_top_viewed_articles_by_date ###
        
def test_call_get_top_viewed_articles_by_date(mocker, proper_per_article_response_dict):
    mocker.patch('flaskr.wikipedia_api.requests.get', return_value=SimpleRequestResponse(text=json.dumps(proper_per_article_response_dict)))
    assert call_get_page_views_by_article('2015100200').raise_for_status() is None # No Error
    assert call_get_page_views_by_article('2015100200').text == json.dumps(proper_per_article_response_dict)

def test_call_page_view_by_article_bad_timestamps(mocker):
    mocker.patch('flaskr.wikipedia_api.validate_timestamp', side_effect=Exception('Any Error'))
    with pytest.raises(Exception, match='Any Error'):
        call_get_page_views_by_article('123')