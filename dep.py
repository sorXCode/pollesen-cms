from dotenv import load_dotenv
# load envrionment variables from '.env' file
load_dotenv()
import os
from depot.manager import DepotManager

# Configure a *default* depot to store files on MongoDB GridFS
DepotManager.configure('default', {
    'depot.backend': 'depot.io.boto3.S3Storage',
    'depot.access_key_id': os.environ["AWS_ACCESS_KEY_ID"],
    'depot.secret_access_key': os.environ["AWS_SECRET_ACCESS_KEY"],
    'depot.bucket': os.environ["S3_BUCKET"]
})

storage = DepotManager.get()
pass

# # Save the file and get the fileid
# fileid = storage.create(open('./requirements.txt', 'rb'))

# # Get the file back
# stored_file = storage.get(fileid)
# print(stored_file.filename)
# print(stored_file.content_type)