import json

from google.cloud import storage, exceptions
from google.cloud.storage import Blob

import utility


class Storage:

    def __init__(self):
        self.gcs = storage.Client(project=utility.project_id())

    def check_bucket(self, bucket_name):
        try:
            self.gcs.get_bucket(bucket_name)
            return True
        except exceptions.NotFound:
            print ('Bucket {} does not exists.'.format(bucket_name))
            return False
        except exceptions.BadRequest:
            print ('Error: Invalid bucket name {}'.format(bucket_name))
            return None
        except exceptions.Forbidden:
            print ('Error: Forbidden, Access denied for bucket {}'.format(bucket_name))
            raise exceptions.Forbidden


    def create_bucket(self, bucket_name):
        bucket_exists = self.check_bucket(bucket_name)

        if bucket_exists is not None and not bucket_exists:
            try:
                print ('creating bucket {}'.format(bucket_name))
                self.gcs.create_bucket(bucket_name)
                return True
            except Exception as e:
                print "Error: Create bucket Exception"
                print e
                return None
        return bucket_exists


    def store_json_to_gcs(self, bucket_name, capital_json, city_id):
        bucket = self.gcs.get_bucket(bucket_name)
        blob = bucket.blob(str(city_id))
        return blob.upload_from_string(data=json.dumps(capital_json))

    def store_file_to_gcs(self, bucket_name, filename):
        bucket = self.gcs.get_bucket(bucket_name)
        blob = Blob(filename, bucket)
        try:
            with open(filename, 'rb') as input_file:
                blob.upload_from_file(input_file)
            return True
        except IOError:
            print ('Error: Cannot find the file {}'.format(filename))

