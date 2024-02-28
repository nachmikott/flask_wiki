from flask.views import View
from flask import request
from datetime import datetime
from .utils import list_of_most_viewed_articles
from enum import Enum
from .exceptions import TimestampException, UnexpectedDownstreamResponse

class TOP_ARTICLE_FUNCTIONS(Enum):
    MOST_VIEWED_ARTICLES = 'most_viewed_articles'
    
class TopArticlesView(View):
    '''
    View that caters to API endpoints that need models that are by time intervals to aggregate article lists
    '''
    init_every_request = False

    def dispatch_request(self, func, timestamp):
        response = {}
        status_code = 200

        match func:
            case TOP_ARTICLE_FUNCTIONS.MOST_VIEWED_ARTICLES.value:
                try: 
                    list_of_articles = list_of_most_viewed_articles(timestamp=timestamp, limit=int(request.args.get('limit', '1000')))
                    response = {
                        'list_of_articles': list_of_articles,
                        'timestamp_given_by_request': timestamp 
                    }
                except TimestampException as exception:
                    print(f'TimestampException({exception})')
                    response = { 
                        'exception_message': str(exception)
                    }
                    status_code = 400  
                except UnexpectedDownstreamResponse as exception:
                    print(f'UnexpectedDownstreamResponse({exception})')
                    response = { 
                        'exception_message': str(exception) 
                    }
                    status_code = 502
                except Exception as exception:
                    print(f'Exception({exception})')
                    response = {
                        'exception_message': str(exception),
                    }
                    status_code = 500
            case _:
                list_of_functions = list(map(lambda x: x.value, TOP_ARTICLE_FUNCTIONS._member_map_.values()))
                response = {
                    'exception_message': (f'"{func}" is not valid, please choose one of the following {list_of_functions}'),
                }
                status_code = 404        
        response['response_timestamp'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        return (response, status_code)
