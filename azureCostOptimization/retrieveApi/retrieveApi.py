
from azure.cosmos import CosmosClient
from azure.storage.blob import BlobServiceClient

cosmos_client = CosmosClient("<COSMOS_ENDPOINT>", credential="<COSMOS_KEY>")
cosmos_container = cosmos_client.get_database_client("billing_records_db").get_container_client("billing_records")

blob_service_client = BlobServiceClient.from_connection_string("<BLOB_CONNECTION_STRING>")
blob_container_client = blob_service_client.get_container_client("archived-billing-records")

def get_billing_record(record_id):
    try:
        record = cosmos_container.read_item(item=record_id, partition_key=record_id)
        return record
    except:
        metadata = cosmos_container.read_item(item=record_id, partition_key=record_id)
        blob_client = blob_container_client.get_blob_client(blob_name=f"{record_id}.json")
        blob_data = blob_client.download_blob().readall()
        return blob_data
