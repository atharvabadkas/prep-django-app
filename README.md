# Prep App with CLIP Model Integration

This Django application uses a CLIP (Contrastive Language-Image Pre-training) model for image classification. The application fetches images from Google Drive, classifies them using the CLIP model, and displays the results in a web interface.

## Setup Instructions

1. Clone the repository
2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Make sure you have the following files in the `models` directory:
   - `prep_label_classifier.pkl`
   - `prep_label_encoder.pkl`

4. Set up your Google Drive API credentials:
   - Create a service account in the Google Cloud Console
   - Download the credentials JSON file
   - Place it at the root of the project as `credentials.json`

5. Run the Django application:
   ```
   python manage.py runserver
   ```

## How It Works

1. The application uses the CLIP model to classify images
2. The model is loaded in `load_architecture.py`
3. Images are classified in `classifications.py`
4. The web interface allows you to:
   - Select a date to view images
   - View the classification results
   - Export the results to Excel

## Model Architecture

The application uses the following components:

- **CLIP Model**: ViT-L-14 pretrained on LAION-2B
- **Classifier**: A trained classifier loaded from `prep_label_classifier.pkl`
- **Label Encoder**: A label encoder loaded from `prep_label_encoder.pkl`
- **Augmentation**: Uses albumentations for image augmentation during prediction

## Troubleshooting

If you encounter any issues:

1. Make sure all dependencies are installed correctly
2. Check that the model files are in the correct location
3. Verify that your Google Drive API credentials are valid
4. Check the console for any error messages

## Notes

- The application uses a wrapper class (`CLIPWrapper`) to maintain compatibility with the existing code
- The `process_with_secondary_model` function is a placeholder and can be implemented if a secondary model is needed 