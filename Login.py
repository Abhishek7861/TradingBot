from typing import Collection
from py5paisa import FivePaisaClient
from ApiKeys import *

# Function to login user and return client object
def loginUser():
    cred={
    "APP_NAME":AppName,
    "APP_SOURCE":AppSource,
    "USER_ID":UserID,
    "PASSWORD":Password,
    "USER_KEY":UserKey,
    "ENCRYPTION_KEY":EncryptionKey
    }
    client = FivePaisaClient(email=email, passwd=loginPassword, dob=dob,cred=cred)
    client.login()
    return client

# loginUser()