import json
import utility
import cloudstorage

from google.cloud import datastore


class Capitals:

    def __init__(self):
        self.ds = datastore.Client(project=utility.project_id())
        self.kind = "newworld"


    def store_capital_gcs(self, city_id, bucketname):
        # Check if the id exists in datastore
        # raises TypeError if city_id not in DataStore
        city = self.fetch_capital(city_id)
        if city is not None:
            cloudstore = cloudstorage.Storage()
            created = cloudstore.create_bucket(bucketname)
            if created is not None and created:
                cloudstore.store_json_to_gcs(bucketname, city)
            else:
                raise TypeError
        return True


    def store_capital(self, city_id, city):
        key = self.ds.key(self.kind, int(city_id))
        entity = datastore.Entity(key)
        entity['id'] = int(city_id)
        entity['country'] = city['country']
        entity['name'] = city['name']
        # entity['location'] = datastore.Entity(key=self.ds.key('EmbeddedKind'))
        # entity['location']['latitude'] = float(city['location']['latitude'])
        # entity['location']['longitude'] = float(city['location']['longitude'])
        entity['latitude'] = float(city['location']['latitude'])
        entity['longitude'] = float(city['location']['longitude'])
        entity['countryCode'] = city['countryCode']
        entity['continent'] = city['continent']
        return self.ds.put(entity)

    def fetch_capitals(self):
        query = self.ds.query(kind=self.kind)
        query.order = ['id']
        return self.get_query_results(query)


    def fetch_capital(self, city_id):
        key = self.ds.key(self.kind, int(city_id))
        return Capitals.change_location(self.ds.get(key))

    @staticmethod
    def change_location(city):
        new_city = {}
        new_city['id'] =  city['id']
        new_city['country'] = city['country']
        new_city['name'] = city['name']
        x = { 'latitude' : city['latitude'],
              'longitude' : city['longitude']}
        new_city['location'] = x
        new_city['countryCode'] = city['countryCode']
        new_city['continent'] = city['continent']
        return new_city


    def get_query_results(self, query):
        results = list()
        for entity in list(query.fetch()):
            x = Capitals.change_location(dict(entity))
            results.append(x)
        return results

    def delete_capital(self, city_id):
        key = self.ds.key(self.kind, int(city_id))
        # TODO - Check why delete itself is not throwing
        # exception when key does not exist in DS
        if self.ds.get(key) is None:
            raise AttributeError
        return self.ds.delete(key)


def parse_note_time(note):
    """converts a greeting to an object"""
    return {
        'text': note['text'],
        'timestamp': note['timestamp'].strftime('%Y-%m-%d %H:%M:%S')
    }
