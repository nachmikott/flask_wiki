
import requests
from enum import Enum
from flaskr.validators import validate_timestamp

url = 'https://wikimedia.org'
base_endpoint = '/api/rest_v1/metrics/pageviews'

# according to Wikimedia, all agent requests (i.e this Flask App) must have the User-Agent header key-value pair
# https://meta.wikimedia.org/wiki/User-Agent_policy
headers = {'User-Agent': 'FlaskWiki/0.0 (https://example.org/flaskwiki/; flaskwiki@example.org)'}

class endpoint_type(Enum):
    AGGREGATE = 'aggregate'
    PER_ARTICLE = 'per-article'
    TOP = 'top'
    TOP_BY_COUNTRY = 'top-by-country'
    TOP_PER_COUNTRY = 'top-per-country'

class aggregation_timeperiods(Enum):
    MONTHLY = 'monthly'
    DAILY = 'daily'
    HOURLY = 'hourly'

class access_types(Enum):
    ALL_ACCESS = 'all-access'

class agent_types(Enum):
    ALL_AGENTS = 'all-agents'

def call_get_page_views_by_article(article, options={}):
    '''
    Calls the Per-Article endpoints of WikiTech. Options allow for calling different Per-Article endpoint types

    Parameters:
    article (string): The article to get data about.
   
    Returns:
    request.Response object

    Raises:
    TimestampException --> parameter options.start_timestamp op options.end_timestamp was not in format YYYYMMDD or YYYYMM
    '''
    start_timestamp = options.get('start_timestamp', '2015100100')
    end_timestamp = options.get('end_timestamp', '2015103100')
    access_type = options.get('access_type', access_types.ALL_ACCESS.value)
    agent_type = options.get('agent_type', agent_types.ALL_AGENTS.value)
    aggregation_timeperiod = options.get('aggregation_timeperiod', aggregation_timeperiods.DAILY.value)

    validate_timestamp(start_timestamp)
    validate_timestamp(end_timestamp)

    api_url = f'{url}{base_endpoint}/{endpoint_type.PER_ARTICLE.value}/en.wikipedia/{access_type}/{agent_type}/{article}/{aggregation_timeperiod}/{start_timestamp}/{end_timestamp}'
    print(f'calling: {api_url}')
    return requests.get(api_url, headers=headers)


def call_get_top_viewed_articles_by_date(timestamp, access_type=access_types.ALL_ACCESS.value):
    '''
    Calls the Top-Articles endpoints of WikiTech. Options allow for calling different Top-Articles endpoint types

    Parameters:
    timestamp (string): the timestamp of interest.
   
    Returns:
    request.Response object

    Raises:
    TimestampException --> parameter options.start_timestamp op options.end_timestamp was not in format YYYYMMDD or YYYYMM
    '''
    no_day = True if len(timestamp) != 8 else False
    validate_timestamp(timestamp, no_day=no_day, no_hour=True)

    day = 'all-days' if len(timestamp) != 8 else timestamp[6:]
    formatted_timestamp = timestamp[:4] + '/' + timestamp[4:6] + '/' + day

    api_url = f'{url}{base_endpoint}/{endpoint_type.TOP.value}/en.wikipedia/{access_type}/{formatted_timestamp}'
    print(f'calling: {api_url}')
    return requests.get(api_url, headers=headers)