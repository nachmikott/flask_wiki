from flask.views import View
from flask import request, make_response
from datetime import datetime
from enum import Enum
from .utils import get_date_of_most_views, get_view_count
from requests.exceptions import HTTPError
from .exceptions import TimestampException, UnexpectedDownstreamResponse

class PER_ARTICLE_FUNCTIONS(Enum):
    DATE_OF_MOST_VIEWS = 'date_of_most_views'
    VIEW_COUNT = 'view_count'

class PartArticleView(View):
    '''
    View that caters to API endpoints that need models that are by article
    '''
    init_every_request = False

    def dispatch_request(self, func, article):
        response = {}
        status_code = 200
        try:
            match func:
                case PER_ARTICLE_FUNCTIONS.DATE_OF_MOST_VIEWS.value:
                    response = {
                        'article': article,
                        'most_views_timestamp': get_date_of_most_views(article, request.args.get('start_timestamp'), request.args.get('end_timestamp')),
                        'start_timestamp': request.args.get('start_timestamp'),
                        'end_timestamp': request.args.get('end_timestamp')}
                case PER_ARTICLE_FUNCTIONS.VIEW_COUNT.value:
                    response = {
                        'article': article,
                        'view_count': get_view_count(article, request.args.get('start_timestamp'), request.args.get('end_timestamp')),
                        'start_timestamp': request.args.get('start_timestamp'),
                        'end_timestamp': request.args.get('end_timestamp')}
                case _:
                    list_of_functions = list(map(lambda x: x.value, PER_ARTICLE_FUNCTIONS._member_map_.values()))
                    response = {
                        'exception_message': (f'"{func}" is not valid, please choose one of the following {list_of_functions}'),
                    }
                    status_code = 404
        except TimestampException as exception:
            print(f'TimestampException({exception})')
            response = {
                'exception_message': str(exception)
            }
            status_code = 400
        except (UnexpectedDownstreamResponse) as exception:
            print(f'UnexpectedDownstreamResponse({exception})')
            response = {
                'exception_message': str(exception)
            }
            status_code = 502
        except Exception as exception:
            response = {
                'exception_message': str(exception),
            }
            status_code = 500
        finally:
            response['response_timestamp'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            return (response, status_code)
