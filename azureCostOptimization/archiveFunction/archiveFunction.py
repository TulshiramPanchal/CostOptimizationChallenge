
import datetime
import json
from azure.cosmos import CosmosClient
from azure.storage.blob import BlobServiceClient

cosmos_client = CosmosClient(COSMOS_ENDPOINT, credential=COSMOS_KEY)
cosmos_container = cosmos_client.get_database_client(billing_records_db).get_container_client(billing_records)

blob_service_client = BlobServiceClient.from_connection_string(BLOB_CONNECTION_STRING)
blob_container_client = blob_service_client.get_container_client(archived-billing-records)

def archive_old_records()
    today = datetime.datetime.utcnow()
    cutoff = today - datetime.timedelta(days=90)

    query = SELECT  FROM c WHERE c.timestamp  @timestamp
    parameters = [{name @timestamp, value cutoff.isoformat()}]
    records = cosmos_container.query_items(query=query, parameters=parameters, enable_cross_partition_query=True)

    for record in records
        record_id = record['id']
        blob_name = f{record_id}.json
        blob_data = json.dumps(record)

        blob_client = blob_container_client.get_blob_client(blob_name)
        blob_client.upload_blob(blob_data, overwrite=True)

        metadata = {
            id record_id,
            blob_uri blob_client.url,
            archived True,
            timestamp record['timestamp']
        }
        cosmos_container.upsert_item(metadata)

        cosmos_container.delete_item(record['id'], partition_key=record['id'])
