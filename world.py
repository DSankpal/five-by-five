from datetime import datetime
from google.cloud import datastore
import utility


class Capitals:

    def __init__(self):
        self.ds = datastore.Client(project=utility.project_id())
        self.kind = "world"

    def store_capital(self, city_id, city):
        key = self.ds.key(self.kind)
        entity = datastore.Entity(key)
        entity['id'] = int(city_id)
        entity['country'] = city['country']
        entity['name'] = city['name']
        entity['latitude'] = float(city['location']['latitude'])
        entity['longitude'] = float(city['location']['longitude'])
        entity['countryCode'] = city['countryCode']
        entity['continent'] = city['continent']
        # entity['timestamp'] = datetime.utcnow()
        return self.ds.put(entity)

    def fetch_capitals(self):
        query = self.ds.query(kind=self.kind)
        query.order = ['id']
        return self.get_query_results(query)

    def get_query_results(self, query):
        results = list()
        for entity in list(query.fetch()):
            results.append(dict(entity))
        return results

    def delete_capital(self, id):
        # entity = self.ds.Entity(id)
        key = self.ds.key(self.kind)
        entity = datastore.Entity(key)
        entity['id'] = int(id)
        return self.ds.delete(entity)

def parse_note_time(note):
    """converts a greeting to an object"""
    return {
        'text': note['text'],
        'timestamp': note['timestamp'].strftime('%Y-%m-%d %H:%M:%S')
    }
