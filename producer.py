import boto3
import json
import time
import random

kinesis = boto3.client('kinesis', region_name='us-east-1')

users = ["u1", "u2", "u3"]

while True:
    event = {
        "user_id": random.choice(users),
        "action": random.choice(["login", "click", "logout"]),
        "timestamp": time.time()
    }

    kinesis.put_record(
        StreamName="user-activity-stream",
        Data=json.dumps(event),
        PartitionKey=event["user_id"]
    )

    print("Sent:", event)
    time.sleep(1)
