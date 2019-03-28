import boto3
import yaml
from botocore.exceptions import ClientError

#taking in data from yaml
with open('dataset1.yaml', 'r') as data:
    doc=yaml.load(data)

# This address must be verified with Amazon SES.
SENDER = doc['sender']
print(SENDER)

# This array must be verified by SES for now.
RECIPIENT = doc['recipient']
print(RECIPIENT)

AWS_REGION = "us-west-2"

# The subject line for the email.
SUBJECT = doc['subject']

# The email body for recipients with non-HTML email clients.
BODY_TEXT = (doc['body'])
            
# The HTML body of the email.
BODY_HTML = """<html>
<head></head>
<body>"""+doc['body']+"""
</body>
</html>
"""            

CHARSET = "UTF-8"

# Create a new SES resource and specify a region.
client = boto3.client('ses',region_name=AWS_REGION)

# Try to send the email.
try:
    #Provide the contents of the email.
    response = client.send_email(
        Destination={
            'ToAddresses': [SENDER,], # sender gets a version of their email
            'BccAddresses': RECIPIENT, # all the recepients have their emails in BCC
        },
        Message={
            'Body': {
                'Html': {
                    'Charset': CHARSET,
                    'Data': BODY_HTML,
                },
                'Text': {
                    'Charset': CHARSET,
                    'Data': BODY_TEXT,
                },
            },
            'Subject': {
                'Charset': CHARSET,
                'Data': SUBJECT,
            },
        },
        Source=SENDER,
    )
except ClientError as e:
    print(e.response['Error']['Message'])
else:
    print("Email sent! Message ID:"),
    print(response['MessageId'])