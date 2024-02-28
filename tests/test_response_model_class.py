import pytest
from flaskr.response_model_class import response_per_article_decoder, response_top_decoder
from tests.fixtures import proper_top_response_dict, proper_per_article_response_dict, improper_response_dict, expected_top_response_object, expected_per_article_response_object

# Test response_top_decoder, when given a proper response_dict returns Response object
def test_proper_top_response_dict(proper_top_response_dict, expected_top_response_object):
    response_object = response_top_decoder(proper_top_response_dict)
    for index_item, item in enumerate(response_object.items):
        assert expected_top_response_object.items[index_item].article == item.article
        assert expected_top_response_object.items[index_item].views == item.views

# Test response_top_decoder, when given a improper response_dict returns Empty Response
def test_improper_top_response_dict(improper_response_dict):
    assert response_top_decoder(improper_response_dict) == improper_response_dict

# Test response_per_article_decoder, when given a proper response_dict returns Response object
def test_proper_per_article_response_dict(proper_per_article_response_dict, expected_per_article_response_object):
    response_object = response_per_article_decoder(proper_per_article_response_dict)
    for index_item, item in enumerate(response_object.items):
        assert expected_per_article_response_object.items[index_item].article == item.article
        assert expected_per_article_response_object.items[index_item].views == item.views

# Test response_per_article_decoder, when given a improper response_dict returns Empty Response
def test_improper_per_article_response_dict(improper_response_dict):
    assert response_per_article_decoder(improper_response_dict) == improper_response_dict
