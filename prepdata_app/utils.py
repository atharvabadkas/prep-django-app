# from googleapiclient.discovery import build
# from googleapiclient.http import MediaIoBaseDownload
# from google.oauth2 import service_account
# import os

# # Set up credentials
# SCOPES = ['https://www.googleapis.com/auth/drive.readonly']
# SERVICE_ACCOUNT_FILE = 'credentials.json'

# def get_images_from_drive(folder_id):
#     credentials = service_account.Credentials.from_service_account_file(
#         SERVICE_ACCOUNT_FILE, scopes=SCOPES
#     )
#     service = build('drive', 'v3', credentials=credentials)

#     # Get all files in the folder
#     results = service.files().list(
#         q=f"'{folder_id}' in parents and mimeType contains 'image/'",
#         fields="files(id, name)"
#     ).execute()

#     images = []
#     for file in results.get('files', []):
#         image_url = f"https://drive.google.com/uc?id={file['id']}"
#         images.append({'name': file['name'], 'url': image_url})
    
#     return images

# import os
# from googleapiclient.discovery import build
# from googleapiclient.http import MediaIoBaseDownload
# from google.oauth2.service_account import Credentials

# def get_images_from_drive(folder_id):
#     """Fetch image URLs from a Google Drive folder."""
#     # Set up the Google Drive API client
#     SCOPES = ['https://www.googleapis.com/auth/drive.readonly']
#     creds = Credentials.from_service_account_file('credentials.json', scopes=SCOPES)
#     service = build('drive', 'v3', credentials=creds)

#     # Query files in the specified folder
#     query = f"'{folder_id}' in parents and mimeType contains 'image/' and trashed = false"
#     results = service.files().list(q=query, fields="files(id, name)").execute()
#     items = results.get('files', [])

#     images = []
#     if not items:
#         print('No images found in the specified folder.')
#     else:
#         for item in items:
#             # Generate a direct link for viewing the image
#             image_url = f"https://drive.google.com/uc?id={item['id']}"
#             images.append({'url': image_url, 'name': item['name']})
#     return images

# def get_images_from_drive(folder_id):
#     """Fetch sharable image URLs from a Google Drive folder."""
#     from googleapiclient.discovery import build
#     from google.oauth2.service_account import Credentials

#     # Authenticate using the service account
#     SCOPES = ['https://www.googleapis.com/auth/drive']
#     creds = Credentials.from_service_account_file('credentials.json', scopes=SCOPES)
#     service = build('drive', 'v3', credentials=creds)

#     # Query the files in the folder
#     query = f"'{folder_id}' in parents and mimeType contains 'image/' and trashed = false"
#     results = service.files().list(q=query, fields="files(id, name, thumbnailLink)").execute()
#     items = results.get('files', [])

#     images = []
#     if not items:
#         print('No images found.')
#     else:
#         for item in items:
#             # Use the webViewLink to ensure access
#             images.append({
#                 'url': item.get('thumbnailLink'),
#                 'name': item['name']
#             })
#     return images

# # webViewLink

#remove duplicates, assign flags(temp)

#Remove duplicate images based on unique identifiers like name, timestamp, and weight.
def remove_duplicates(images):
    seen = set()
    unique_images = []
    for image in images:
        # Use a tuple of unique attributes as the identifier
        identifier = (image['time_date'], image['item_weight'])
        if identifier not in seen:
            seen.add(identifier)
            unique_images.append(image)
    return unique_images


# Function to assign flags based on temperature ranges
def assign_flags(camera_temp, mcu_temp, weight):
    camera_flag = 0
    mcu_flag = 0
    weight_flag = 0

    # Camera temperature conditions
    if 5 <= int(camera_temp) <= 45:
        camera_flag = "TC1"
    elif 45 < int(camera_temp) <= 55:
        camera_flag = "TC2"
    elif 55 < int(camera_temp) <= 100:
        camera_flag = "TC3"
    else:
        camera_flag = "TC4"

    # MCU temperature conditions
    if 5 <= int(mcu_temp) <= 60:
        mcu_flag = "TX1"
    elif 60 < int(mcu_temp) <= 80:
        mcu_flag = "TX2"
    elif 80 < int(mcu_temp) <= 100:
        mcu_flag = "TX3"
    else:
        mcu_flag = "TX4"

    #weight image conditions:
    if (-10000 <= int(weight) <= 200000):
        weight_flag = 'WT1'
    else:
        weight_flag = 'WT2'

    return camera_flag, mcu_flag, weight_flag