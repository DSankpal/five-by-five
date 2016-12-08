import base64
import json

from google.cloud import pubsub

import utility


class PubSub:

    def __init__(self):
        self.psc = pubsub.Client(project=utility.project_id())

    def publish(self, topic_name, data):
        """Publishes a message to a Pub/Sub topic with the given data."""

        # Topic name is of format - projects/hackathon-team-005/topics/test-005
        parts = topic_name.split('/')
        if len(parts) != 4:
            raise Exception('Invalid topic path')
        else:
            project_name = parts[1]
            topic_part = parts[3]
            client = pubsub.Client(project=project_name)
            topic = client.topic(topic_part)
            # topic.create()
            # Data must be a bytestring
            # data = base64.b64encode(json.dumps(data)).encode('utf-8')
            # data = data.encode('utf-8')
            message_id = topic.publish(json.dumps(data), client)
            print('Message {} published.'.format(message_id))
            return message_id
