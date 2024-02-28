import json

class Item:
  def __init__(self, article, views, timestamp='na'):
    self.article = article
    self.timestamp = timestamp
    self.views = views

  def __repr__(self):
    return('Item(article={self.article!r}, timestamp={self.timestamp!r} views={self.views!r}'.format(self=self))
  
  def toJSON(self):
    return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)

class Response:
  '''
  A model of the API Response from WikiTech
  '''
  def __init__(self, items):
    self.items = items

  def __repr__(self):
    return('Response(items={self.items!r}'.format(self=self))

  def toJSON(self):
    return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)

# Decoders for json.load()

def response_top_decoder(response_dict):
    if 'items' not in response_dict:
      return response_dict
    else:
      def convert_item_dict_to_Item(item):
          return Item(article=item.get('article'), timestamp=item.get('timestamp'), views=item.get('views'))
      items = list(map(convert_item_dict_to_Item, response_dict.get('items')[0].get('articles')))
      return Response(items=items)

def response_per_article_decoder(response_dict):
    if 'items' not in response_dict:
      return response_dict
    else:
      def convert_item_dict_to_Item(item):
          return Item(article=item.get('article'), timestamp=item.get('timestamp'), views=item.get('views'))
      items = list(map(convert_item_dict_to_Item, response_dict.get('items')))
      return Response(items=items)