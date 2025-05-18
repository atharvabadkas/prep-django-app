import re
import requests
from io import BytesIO
from PIL import Image
import numpy as np

from .models import ImageClassificationResult

def extract_wt_from_filename(image_name):
    """
    Extract WT and number from the image filename.
    """
    match = re.search(r'WT(-?\d+)', image_name)
    if match:
        return match.group(0), int(match.group(1))
    return None, None

def classify_image(image_path, model):
    """
    Classify an image using the provided CLIP model wrapper.
    """
    try:
        # If the path is a URL, download the image first
        if image_path.startswith('http'):
            response = requests.get(image_path)
            if response.status_code == 200:
                image_data = BytesIO(response.content)
                image = Image.open(image_data).convert('RGB')
            else:
                print(f"Failed to fetch image. HTTP Status: {response.status_code}")
                return 'failure'
        else:
            image = Image.open(image_path).convert('RGB')

        # Use the CLIP wrapper's predict method
        result = model.predict(image)
        return result
    except Exception as e:
        print(f"Error during classification: {e}")
        return 'failure'

def handle_classification_results(image, result):
    """
    Handle the classification results, flagging images as "SU" or "SK2" based on filename.
    """
    wt, wt_number = extract_wt_from_filename(image['name'])

    if wt_number == 65100001:
        image['classification_flag'] = "SU"  # Proxy image flag
    else:
        image['classification_flag'] = "SK2"  # Weight image flag
    
    # If primary model fails, run the secondary model
    if result == 'failure':
        result = process_with_secondary_model(image)
    
    # Store result in the database - commented out until migrations are run
    # ImageClassificationResult.objects.create(
    #     image_name=image['name'],
    #     classification_flag=image['classification_flag'],
    #     classification_status=result
    # )
    
    # Just print the result for now
    print(f"Classified {image['name']} as {result} with flag {image['classification_flag']}")

def process_with_secondary_model(image):
    """
    Process the image using the secondary model and perform additional operations.
    This is a placeholder function that can be implemented if a secondary CLIP model is needed.
    """
    # For now, we'll just return a failure status
    # In a real implementation, you would:
    # 1. Load a secondary CLIP model
    # 2. Classify the image using that model
    # 3. Set appropriate flags based on the classification result
    
    # Determine the image type (proxy or weight)
    wt, wt_number = extract_wt_from_filename(image['name'])
    if wt_number == 65100001:
        image_type = "proxy"  # Proxy image
    else:
        image_type = "weight"  # Weight image
    
    # Set a default flag for failed classifications
    image['classification_flag'] = "UNKNOWN"
    
    return 'failure'

def model_process_images(images_list, model):
    """
    Process a list of images using the CLIP model.
    """
    for image in images_list:
        # Get the image URL from thumbnailLink
        image_url = image['thumbnailLink']
        
        # Classify the image
        classification_result = classify_image(image_url, model)
        
        # Store the classification result
        image['classification_result'] = classification_result

        # Handle classification results
        handle_classification_results(image, classification_result)

    return images_list