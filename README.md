# Leukemia_Cancer_Detection
Automated detection of Acute Lymphoblastic Leukemia (ALL) using CNN-based ensemble models trained on segmented and non-segmented microscopic blood smear images.

## 📁 Repository Structure
```plaintext
Leukemia-Cancer-Detection/
├── data/                        
│   ├── segmented/
│   │   ├── train/
│   │   ├── val/
│   │   └── test/
│   └── non_segmented/
│       ├── train/
│       ├── val/
│       └── test/
├── models_on_segmented_data/     # CNN models trained on segmented data
├── models_on_non_segmented_data/ # CNN models trained on non-segmented data
├── web/                          # Flask web app files for prediction interface
├── README.md                     # Project documentation
├── requirements.txt              # Python dependencies
└── LICENSE                       # License information
```

## 📊 Dataset

The dataset contains microscopic images used for Acute Lymphoblastic Leukemia detection. The data is split into train, validation, and test sets for robust evaluation.

Due to the large size of the dataset, it is not included in this repository. You can access the datasets from the following sources:

### 🔗 Dataset Sources

| Dataset | Description | Link |
|---|---|---|
| **ALL-IDB** (Acute Lymphoblastic Leukemia Image Database) | A public image database designed for the evaluation and comparison of algorithms for segmentation and classification of leukemic cells in microscopic images. Includes both segmented (ALL-IDB2) and non-segmented (ALL-IDB1) variants. | [scotti.di.unimi.it/all](https://scotti.di.unimi.it/all/) |
| **Blood Cells Cancer (ALL) – 4 Class** | A Kaggle dataset containing blood cell microscopic images categorized into 4 classes for ALL detection. | [Kaggle Dataset](https://www.kaggle.com/datasets/mohammadamireshraghi/blood-cell-cancer-all-4class) |

> **Note:** Please review and comply with the respective terms of use and licenses for each dataset before use in your research or projects.

## 🧠 Deep Learning Models

Pre-trained models and training scripts are available in the following folders:
- `models_on_segmented_data/` — Models trained on segmented dataset
- `models_on_non_segmented_data/` — Models trained on non-segmented dataset

**Included architectures:**
- MobileNetV2
- VGG16
- DenseNet121

An ensemble approach combines these models to improve detection accuracy.

## 📱 Web Application

The `web/` folder contains a Flask-based web application providing a user-friendly interface for:
- Uploading blood smear images
- Running predictions using the trained ensemble model
- Displaying prediction results
- Downloading the annotated images post-prediction

## ⚙️ Requirements

Install dependencies via:
```bash
pip install -r requirements.txt
```

## 📌 Citation

If you use this repository or dataset in your research, please cite:

_(Citation details will be updated upon DOI assignment)_

## 📨 Contact

For questions or collaborations, please reach out:

**InteX Research Lab**
📧 intexresearchlab@gmail.com
