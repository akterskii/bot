import os

from google.oauth2 import service_account
import googleapiclient.discovery
#
# # Get credentials
# filename = "credentials\My_First_Project-d8b13a80b5b0.json"
# credentials = service_account.Credentials.from_service_account_file(
#     filename=filename,  # os.environ['GOOGLE_APPLICATION_CREDENTIALS'],
#     scopes=['https://www.googleapis.com/auth/cloud-platform'])
#
# # Create the Cloud IAM service object
# service = googleapiclient.discovery.build(
#     'iam', 'v1', credentials=credentials)
#
# # Call the Cloud IAM Roles API
# # If using pylint, disable weak-typing warnings
# # pylint: disable=no-member
# response = service.roles().list().execute()
# roles = response['roles']
#
# # Process the response
# for role in roles:
#     print('Title: ' + role['title'])
#     print('Name: ' + role['name'])
#     if 'description' in role:
#         print('Description: ' + role['description'])
#     print('')
#     break

from google.cloud import bigquery
# Construct a BigQuery client object.

client = bigquery.Client()

# TODO(developer): Set dataset_id to the ID of the dataset to fetch.
# dataset_id = 'your-project.your_dataset'
dataset_id = 'users_BFemKh4v'
dataset = client.get_dataset(dataset_id)  # Make an API request.

entry = bigquery.AccessEntry(
    role="READER",
    entity_type="userByEmail",
    entity_id="sample.bigquery.dev@gmail.com",
)
#os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = filename
entries = list(dataset.access_entries)
entries.append(entry)
dataset.access_entries = entries

dataset = client.update_dataset(dataset, ["access_entries"])  # Make an API request.

full_dataset_id = "{}.{}".format(dataset.project, dataset.dataset_id)
print(
    "Updated dataset '{}' with modified user permissions.".format(full_dataset_id)
)
