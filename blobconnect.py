import os, uuid
from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
from azure.storage.blob import BlobServiceClient as blob_service_client

#from azure.storage.blob import BlockBlobService


try:
    print("Azure Blob Storage Python quickstart sample")

    # Quickstart code goes here
    account_url = "https://allraw.blob.core.windows.net"
    default_credential = DefaultAzureCredential()
    # Create a unique name for the container
    container_name = str(uuid.uuid4())
    print(container_name)

    # Create the container
    #container_client = blob_service_client.create_container(container_name)
    #ContainerClient.create_container(container_name)
    #block_blob_service = BlockBlobService(account_name='allraw', account_key='q5jlCcDX7PtTXSmJwtXZAs4UMTRjeIjiu9LkuTYtRELpj10ykoMK8mCdAEbOD5rqWKHE+Or0ZhYK+AStKGSbiw==')
    #block_blob_service.create_container('mycontainer')
    
    #DefaultEndpointsProtocol=[http|https];AccountName=myAccountName;AccountKey=myAccountKey
    CONNECT_STR = "DefaultEndpointsProtocol=[http|https];AccountName=allraw;AccountKey=q5jlCcDX7PtTXSmJwtXZAs4UMTRjeIjiu9LkuTYtRELpj10ykoMK8mCdAEbOD5rqWKHE+Or0ZhYK+AStKGSbiw=="
    CONTAINER_NAME = "test"
    input_file_path = "/home/lamia/Desktop/sdaia/blob-quickstart/telegram_audio.ogg"
    output_blob_name = "telegram_audio.ogg"

    container_client = ContainerClient.from_connection_string(conn_str=CONNECT_STR, container_name=CONTAINER_NAME)

    # Upload file
    with open(input_file_path, "rb") as data:
        container_client.upload_blob(name=output_blob_name, data=data)

    # Create the BlobServiceClient object
    #blob_service_client = BlobServiceClient(account_url, credential=default_credential)

except Exception as ex:
    print('Exception:')
    print(ex)
    
    