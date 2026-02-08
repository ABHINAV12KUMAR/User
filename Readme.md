# 📊 User Activity Data Store using AWS Kinesis

A real-time, event-driven data pipeline built using AWS Kinesis Data Streams, AWS Lambda, and Amazon S3 to collect, process, and store user activity data.

---

## 🚀 Project Overview

This project demonstrates how to build a real-time streaming system where user activity events are:
- Produced from a local machine
- Ingested by AWS Kinesis
- Processed by AWS Lambda
- Stored in Amazon S3
- Monitored using AWS CloudWatch

---

## 🏗️ Architecture

```
Python Producer (Local Machine)
        ↓
AWS Kinesis Data Stream
        ↓
AWS Lambda (Consumer)
        ↓
Amazon S3 (Storage)
```

---

## 🛠️ Technologies Used

- Python 3
- AWS Kinesis Data Streams
- AWS Lambda
- Amazon S3
- AWS CloudWatch
- boto3 (AWS SDK for Python)

---

## 📁 Project Structure

```
user-data-store-using-kinesis/
│
├── producer.py
└── README.md
```

---

## 🔐 Prerequisites

- AWS Account
- IAM user with programmatic access
- Python 3 installed
- AWS CLI installed

---

## 💻 Local Setup (IMPORTANT)

### 1️⃣ Create Project Folder

```bash
mkdir user-data-store-using-kinesis
cd user-data-store-using-kinesis
```

---

### 2️⃣ Create Python Virtual Environment (Recommended)

```bash
python3 -m venv venv
source venv/bin/activate   # Linux / Mac
# venv\Scripts\activate  # Windows
```

---

### 3️⃣ Install Required Library

```bash
pip install boto3
```

Verify:
```bash
python -c "import boto3; print('boto3 installed')"
```

---

### 4️⃣ Configure AWS CLI

```bash
aws configure
```

Enter:
- AWS Access Key ID
- AWS Secret Access Key
- Default region name (example: us-east-1)
- Output format: json

Verify:
```bash
aws sts get-caller-identity
```

---

## ☁️ AWS Setup Steps

### 5️⃣ Create Kinesis Data Stream

- Service: AWS Kinesis
- Stream name: `user-activity-stream`
- Capacity mode: On-demand
- Region: us-east-1

---

### 6️⃣ Create S3 Bucket

- Bucket name: `user-activity-stream-data`
- Region: same as Kinesis

---

### 7️⃣ Create Lambda Function

- Function name: `kinesis-user-activity-processor`
- Runtime: Python 3.10

#### Permissions
Attach policies:
- AWSLambdaKinesisExecutionRole
- AmazonS3FullAccess

---

### 8️⃣ Lambda Code

```python
import json
import base64
import boto3

s3 = boto3.client("s3")
BUCKET = "user-activity-stream-data"

def lambda_handler(event, context):
    records = []

    for record in event["Records"]:
        payload = base64.b64decode(record["kinesis"]["data"])
        records.append(json.loads(payload))

    s3.put_object(
        Bucket=BUCKET,
        Key=f"events/{context.aws_request_id}.json",
        Body=json.dumps(records)
    )

    return {"status": "success"}
```

Deploy the function.

---

### 9️⃣ Connect Kinesis to Lambda

- Open Lambda
- Add trigger → Kinesis
- Select stream: `user-activity-stream`
- Enable trigger

---

## 🖥️ Local Producer Code

### 🔟 Create `producer.py`

```python
import boto3
import json
import time
import random

kinesis = boto3.client("kinesis", region_name="us-east-1")

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
```

---

## ▶️ How to Run the Project (LOCAL)

### 1️⃣ Activate Virtual Environment

```bash
source venv/bin/activate
```

---

### 2️⃣ Run Producer

```bash
python producer.py
```

Expected output:
```
Sent: {'user_id': 'u1', 'action': 'login', 'timestamp': ...}
```

---

### 3️⃣ Verify Output

- Lambda → Monitor → Invocations > 0
- Lambda → Errors = 0
- S3 Bucket → `events/` folder contains JSON files

---

## 🛑 Stop & Cleanup (Cost Saving)

- Stop producer: `CTRL + C`
- Delete Kinesis stream
- Disable or delete Lambda
- Delete S3 bucket (optional)

---

## 🧠 Key Learnings

- Real-time streaming with AWS Kinesis
- Event-driven serverless architecture
- Lambda as a stream consumer
- Local-to-cloud data ingestion
- Debugging region and permission issues

---
--- commit new Feature
