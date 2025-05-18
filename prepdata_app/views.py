# from django.shortcuts import render
# from .utils import get_images_from_drive

# def image_table_view(request):
#     folder_id = '1rk9bzKJqxYEh6nTKSL1kmbyM4pr4wV1J'
#     images = get_images_from_drive(folder_id)
#     return render(request, 'image_table.html', {'images': images})

import os
import json
import pandas as pd
import tensorflow as tf
from io import BytesIO
from PIL import Image
from pprint import pprint
from datetime import datetime
from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import render, redirect
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from django.views.decorators.csrf import csrf_exempt

from .filename import parse_filename  
from .utils import remove_duplicates 
from .load_architecture import load_architecture
from .classifications import model_process_images   

# Temporary in-memory storage
TEMP_DATA = []

# Initialize Google Drive API
def get_drive_service():
    from google.oauth2.service_account import Credentials
    SCOPES = ['https://www.googleapis.com/auth/drive']
    creds = Credentials.from_service_account_file('/Users/atharvabadkas/Coding /my_prepapp/credentials.json', scopes=SCOPES)
    return build('drive', 'v3', credentials=creds)

# List folders
def list_folders(request):
    service = get_drive_service()
    folder_id = '1HJVzNmxOh-gFygsWaEdcIKXMtx9gcAVQ'  # Replace with the ID of your main folder
    results = service.files().list(
        q=f"'{folder_id}' in parents and mimeType = 'application/vnd.google-apps.folder'",
        fields="files(id, name)"
    ).execute()
    folders = results.get('files', [])
    return render(request, 'list_folders.html', {'folders': folders})

# Check folder availability based on the selected date
def check_date_folder(request):
    if request.method == 'POST':
        selected_date = request.POST.get('selected_date')
        if not selected_date:
            return render(request, 'list_folders.html', {'error_message': 'Please select a date.'})

        # Format date to match your folder naming convention (e.g., YYYYMMDD)
        folder_name = datetime.strptime(selected_date, '%Y-%m-%d').strftime('%Y%m%d')

        # Fetch folders from Google Drive
        service = get_drive_service()
        folder_id = '1HJVzNmxOh-gFygsWaEdcIKXMtx9gcAVQ'  # Replace with your main folder ID
        results = service.files().list(
            q=f"'{folder_id}' in parents and mimeType = 'application/vnd.google-apps.folder'",
            fields="files(id, name)"
        ).execute()
        folders = results.get('files', [])
        print('listed the images')
        # Check if the folder exists
        matching_folder = next((folder for folder in folders if folder['name'] == folder_name), None)
        if matching_folder:
            return redirect('list_images', folder_id=matching_folder['id'])
        else:
            return render(request, 'list_folders.html', {'error_message': 'Data for this date is not available.'})

    return render(request, 'list_folders.html')

# List images in the selected folder
def list_images(request, folder_id):
    service = get_drive_service()
    
    image_data = []
    page_token = None           #pagination

    while True:
        results = service.files().list(
            q=f"'{folder_id}' in parents and mimeType contains 'image/'",
            fields="nextPageToken, files(id, name, createdTime, thumbnailLink)",
            pageToken=page_token,
            pageSize=100
        ).execute()
        images = results.get('files', [])

        for file in images:
            parsed_data = parse_filename(file['name'])
            # Example metadata for each image
            image_data.append({
                'thumbnailLink': file['thumbnailLink'],
                'item_weight':  parsed_data['weight'],                      
                'time_date': parsed_data['timestamp'],                      
                'camera_flag': parsed_data['camera_flag'],             
                'mcu_flag': parsed_data['mcu_flag'],  
                'weight_flag': parsed_data['weight_flag'],                  
                'name': file.get('name'),
            })

        #check for next page
        page_token = results.get('nextPageToken')
        if not page_token:
            break

    image_data = remove_duplicates(image_data)      #remove duplicates
    
    # Load the CLIP model architecture
    clip_model = load_architecture()
    
    # Process images with the CLIP model
    processed_data = model_process_images(image_data, clip_model)     #process the images
   
    # Sort by name in ascending order
    processed_data.sort(key=lambda x: x['name'])

    context = {
        "table_rows": processed_data,
    }

    return render(request, "list_images.html", context)


#Update - data for save button
@csrf_exempt
def update_data(request):
    global TEMP_DATA
    if request.method == "POST":
        # Parse the incoming data
        data = json.loads(request.body).get("data", [])
        if not data:
            return JsonResponse({"error": "No data received"}, status=400)

        # Update TEMP_DATA
        TEMP_DATA = data  # Replace or modify as needed
        print("Updated Temporary Data:", TEMP_DATA)  # Debugging
        print(TEMP_DATA)
        return JsonResponse({"message": "Data updated successfully"}, status=200)

    return JsonResponse({"error": "Invalid request"}, status=400)


#export excel file
@csrf_exempt
def export_to_excel(request):
    global TEMP_DATA
    if request.method == "POST":
        if not TEMP_DATA:
            return JsonResponse({"error": "No data to export"}, status=400)

        # Convert TEMP_DATA to DataFrame
        df = pd.DataFrame(TEMP_DATA)
        # # Replace the 'link' column with the 'image_name' derived from the link
        # if 'image' in df.columns:
        #     df['name'] = df['image'].apply(lambda x: os.path.basename(x))  # Extract the file name from the URL
        #     df = df.drop(columns=['image'])  # Remove the 'link' column if no longer needed

        print("Exporting DataFrame:\n", df)  # Debugging
        # print(df)

        # Create an Excel file in memory
        response = HttpResponse(content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
        response["Content-Disposition"] = 'attachment; filename="updated_data.xlsx"'

        with pd.ExcelWriter(response, engine="xlsxwriter") as writer:
            df.to_excel(writer, index=False)

        return response

    return JsonResponse({"error": "Invalid request"}, status=400)


