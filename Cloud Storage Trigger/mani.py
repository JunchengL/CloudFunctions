from google.cloud import storage
import json

# Cloud Function with storage trigger to create new bucket in a specific project

def CreateBucket(data, context):

    # initialize storage client
    storageClient_local = storage.Client()

    # get current bucket
    current_bucket = storageClient_local.get_bucket(data['bucket'])
    
    # get configuration json file, and read content to get the project ID
    blob_config_file = current_bucket.blob('conf.json')
    json_data_string = blob_config_file.download_as_string().decode('ascii')
    json_data = json.loads(json_data_string)
    project = json_data['project_id']

    def createB(bucketName,projectName):
        storageClient_dest = storage.Client(project = projectName)
        bucket = storageClient_dest.bucket(bucketName)
        bucket.storage_class = "STANDARD"
        bucket.create(location = "eu")
        print("Bucket for created in project {}.".format(project_name))
    
    for project_name in project:
        
        bucket_name = project_name + '-transfiles-in'
    
        try:
            createB(bucket_name,project_name)

        except Exception as ex:
            print("exception!\n{}".format(ex))