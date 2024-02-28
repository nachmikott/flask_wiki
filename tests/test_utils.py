import pytest
from flaskr.utils import *
from flaskr.response_model_class import response_per_article_decoder
from flaskr.wikipedia_api import *
from tests.fixtures import proper_top_response_dict, proper_per_article_response_dict, SimpleRequestResponse

#### list_of_most_viewed_articles ####

# Happy Path
def test_list_of_most_viewed_articles(mocker, proper_top_response_dict):
    mocker.patch('flaskr.utils.call_get_top_viewed_articles_by_date', return_value=SimpleRequestResponse(text=json.dumps(proper_top_response_dict)))
    assert len(list_of_most_viewed_articles('20151001')) == len(proper_top_response_dict['items'][0]['articles'])

# Raised Exception
def test_raised_exception(mocker):
    mocker.patch('flaskr.utils.call_get_top_viewed_articles_by_date', side_effect=Exception('Any Error'))
    with pytest.raises(Exception, match='Any Error'):
        list_of_most_viewed_articles('20151001')

# Malformed API Response
def test_list_of_most_viewed_articles_malformed_api_response(mocker):
    mocker.patch('flaskr.utils.call_get_top_viewed_articles_by_date', return_value=SimpleRequestResponse(text='THIS IS SO NOT WHAT I WAS EXPECTING.'))
    with pytest.raises(Exception):
        list_of_most_viewed_articles('20151001')

#### get_date_of_most_views ####

# # Happy Path
def test_get_date_of_most_views_proper_article_start_end_timestamp(mocker, proper_per_article_response_dict):
   mocker.patch('flaskr.utils.call_get_page_views_by_article', return_value=SimpleRequestResponse(text=json.dumps(proper_per_article_response_dict)))
   sorted_items = sorted(proper_per_article_response_dict['items'], reverse=True, key=lambda item: item['views'])

   assert get_date_of_most_views('article1', '2015100100', '2015103100') == sorted_items[0]['timestamp']

# Raised Exception
def test_raised_exception_get_date_of_most_view(mocker):
    mocker.patch('flaskr.utils.call_get_page_views_by_article', side_effect=Exception('Any Error'))
    with pytest.raises(Exception, match='Any Error'):
        get_date_of_most_views('article1', '2015100100', '2015103100')

# Malformed API Response
def test_get_date_of_most_view_malformed_api_response(mocker):
    mocker.patch('flaskr.utils.call_get_page_views_by_article', return_value=SimpleRequestResponse(text='THIS IS SO NOT WHAT I WAS EXPECTING.'))
    with pytest.raises(Exception):
        get_date_of_most_views('article1', '2015100100', '2015103100')

#### get_view_count ###

# Happy Path
def test_get_view_count(mocker, proper_per_article_response_dict):
    mocker.patch('flaskr.utils.call_get_page_views_by_article', return_value=SimpleRequestResponse(text=json.dumps(proper_per_article_response_dict)))

    expected_total_count = 0
    for item in proper_per_article_response_dict['items']:
        expected_total_count += item['views']

    assert get_view_count('anyArticle', '2015100100', '2015103100') == expected_total_count

# Raised Exception
def test_raised_exception_get_view_count(mocker):
    mocker.patch('flaskr.utils.call_get_page_views_by_article', side_effect=Exception('Any Error'))
    with pytest.raises(Exception, match='Any Error'):
        get_view_count('anyArticle', '2015100100', '2015103100')

# Malformed API Response
def test_get_view_count_malformed_api_response(mocker):
    mocker.patch('flaskr.utils.call_get_page_views_by_article', return_value=SimpleRequestResponse(text='THIS IS SO NOT WHAT I WAS EXPECTING.'))
    with pytest.raises(Exception):
        get_view_count('anyArticle', '2015100100', '2015103100')
