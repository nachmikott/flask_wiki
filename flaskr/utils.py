from flaskr.wikipedia_api import call_get_page_views_by_article, call_get_top_viewed_articles_by_date
import json
from flaskr.response_model_class import response_per_article_decoder, response_top_decoder
from flaskr.exceptions import UnexpectedDownstreamResponse

def list_of_most_viewed_articles(timestamp, limit=1000):
    '''
    Given a timestamp and limit, will retrieve the list of top viewed articles for a given day or month.

    Parameters:
    timestamp (string): the timestamp to determine the article view dates in format YYYYMMDD or YYYYMM.
    limit (int): number of articles to return from 0 - 1000. Default - 1000

    Returns:
    int[string]: a list of article names.

    Raises:
    TimestampException --> parameter timestamp was not in format YYYYMMDD or YYYYMM
    HTTPError --> a downstream service did not respond with a HTTP Status 200
    UnexpectedDownstreamResponse --> a downstream service did respond with a HTTP Status 200 but with an unexpected data model.
    '''
    api_response = call_get_top_viewed_articles_by_date(timestamp)
    api_response.raise_for_status() # Will Throw HTTPError if not 200
    try:
        response = json.loads(api_response.text, object_hook=response_top_decoder)
        list_of_articles = list(map(lambda x: x.article, response.items))[:limit]
        return list_of_articles
    except Exception as e: # Mapping a HTTP 200 Request from WikiMedia Didnt Work.
        raise UnexpectedDownstreamResponse(api_response.text)
    

def get_date_of_most_views(article, start_timestamp, end_timestamp):
    '''
    Given an article and start/end timestamp in YYYMMDDHH format, will return a timestamp in YYYYMMDD format
    of the date that the article recieved the most views within the start/end timestamp interval.

    Parameters:
    article (string): the name of the Wikipedia article.
    start_timestamp (string): the timestamp to determine the article view dates in format YYYYMMDDHH.
    end_timestamp (string): the timestamp to determine the article view dates in format YYYYMMDDHH.

    Returns:
    string: a YYYYMMDD formatted timestamp of the date with the most views in the start/end timestamp interval.

    Raises:
    TimestampException --> parameter timestamp was not in format YYYYMMDD or YYYYMM
    HTTPError --> a downstream service did not respond with a HTTP Status 200
    UnexpectedDownstreamResponse --> a downstream service did respond with a HTTP Status 200 but with an unexpected data model.
    '''
    api_response = call_get_page_views_by_article(article, options={ 'start_timestamp': start_timestamp, 'end_timestamp': end_timestamp })
    api_response.raise_for_status() # Will Throw HTTPError if not 200
    try:
        response = json.loads(api_response.text, object_hook=response_per_article_decoder)
        items = response.items
        sorted_items = sorted(items, key=lambda item: item.views, reverse=True)
        result_timestamp = sorted_items[0].timestamp
        return result_timestamp
    except Exception as e: # Mapping a HTTP 200 Request from WikiMedia Didnt Work.
        raise UnexpectedDownstreamResponse(api_response.text)

def get_view_count(article, start_timestamp, end_timestamp):
    '''
    Given an article and start/end timestamp in YYYMMDDHH format, returns the view count within the start/end timestamp interval.

    Parameters:
    article (string): the name of the Wikipedia article.
    start_timestamp (string): the timestamp to determine the article view dates in format YYYYMMDDHH.
    end_timestamp (string): the timestamp to determine the article view dates in format YYYYMMDDHH.

    Returns:
    int: the number of article views within the start/end timestamp

    Raises:
    TimestampException --> parameter timestamp was not in format YYYYMMDD or YYYYMM
    HTTPError --> a downstream service did not respond with a HTTP Status 200
    UnexpectedDownstreamResponse --> a downstream service did respond with a HTTP Status 200 but with an unexpected data model.
    '''
    api_response = call_get_page_views_by_article(article, options={ 'start_timestamp': start_timestamp, 'end_timestamp': end_timestamp })
    api_response.raise_for_status() # Will Throw HTTPError if not 200
    try:
        response = json.loads(api_response.text, object_hook=response_per_article_decoder)
        total_count = 0

        for item in response.items:
            total_count += item.views
        return total_count
    except Exception as e: # Mapping a HTTP 200 Request from WikiMedia Didnt Work.
        raise UnexpectedDownstreamResponse(api_response.text)