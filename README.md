# Prep App with CLIP Model Integration

This Django application uses a CLIP (Contrastive Language-Image Pre-training) model for image classification. The application fetches images from Google Drive, classifies them using the CLIP model, and displays the results in a web interface.

## 🥘 Prep Django App

The **Prep Django App** is a backend system developed using Django that manages the flow of food preparation data. It enables structured tracking and analysis of images and related metadata for food preparation processes, allowing seamless integration with machine learning models and a Google Drive-based storage system.

---

## 🚀 Features

- Upload and manage image data associated with food prep
- Handle device-specific logic and metadata (MAC ID, device type, etc.)
- Integration with Google Drive for image storage
- Dynamic model loading from Google Cloud Storage
- Image prediction using YOLO and CLIP models
- Results visualization through the Django admin and custom views
- SQLite support for local development
- BigQuery support for production datasets

---

## 🛠️ Tech Stack

- **Backend Framework**: Django
- **Database**: SQLite (dev), Google BigQuery (prod)
- **Cloud**: Google Cloud Platform (Drive, BigQuery, GCS)
- **ML Integration**: PyTorch, OpenCLIP, YOLOv8
- **Storage**: Google Drive / GCS for image access

---

## 📁 Project Structure

```
prep-django-app/
├── manage.py
├── prep_app/
│   ├── models.py         # ImageData, ImagePredictionResult, TemporaryData models
│   ├── views.py          # Views for prediction, dashboard, form
│   ├── forms.py          # Custom form to filter by MAC ID, Date
│   ├── urls.py           # URL routing
│   ├── utils/            # Functions for GCS, model loading, preprocessing
│   └── templates/        # Custom HTML templates
├── static/
│   └── js/css/assets     # Frontend assets
├── requirements.txt
└── README.md
```

---

## ⚙️ Installation

1. **Clone the repository**:

```bash
git clone https://github.com/atharvabadkas/prep-django-app.git
cd prep-django-app
```

2. **Create and activate virtual environment**:

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

3. **Install dependencies**:

```bash
pip install -r requirements.txt
```

4. **Run migrations**:

```bash
python manage.py migrate
```

5. **Start the development server**:

```bash
python manage.py runserver
```

---

## 🔍 Key Functionalities

- Load models from GCS dynamically using `model_paths` from BigQuery
- Classify images using YOLO for vessel detection and CLIP for SKU recognition
- Save predictions to SQLite or forward to BigQuery for production
- Form-based query interface to select by MAC ID, date, stream type
- Visualization: Render predictions, confidence, and overlay image

---

## 🧠 ML Models

- CLIP (ViT-based) for SKU recognition (via `predict_proba`)
- YOLOv8 for vessel detection
- Model download logic embedded using `gcsfs` and `torch.load`
- Custom pipeline for preprocessing images and loading results

---

## 📊 Data Flow

1. User uploads or selects images (from GDrive)
2. Image is preprocessed
3. YOLO detects vessels
4. CLIP classifies ingredients
5. Results stored in DB and shown in web dashboard

---

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
