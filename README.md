# Predictive Modeling of Dengue Cases in Campina Grande

This repository contains the data processing and exploratory analysis pipeline developed for the undergraduate thesis (TCC):

**Predictive Modeling of Dengue Cases in Campina Grande: A Machine Learning-Based Approach**

The project focuses on the preparation, auditing, and analysis of epidemiological surveillance data to support the construction of predictive models for dengue case classification.

---

## 📌 Project Objectives

- Perform a systematic audit of missing data in real-world epidemiological datasets
- Identify and standardize symptom, warning sign, severity, and outcome variables across multiple years
- Prepare a clean and consistent dataset for supervised machine learning models
- Predict the final case classification, including:
  - Discarded
  - Dengue
  - Dengue with warning signs
  - Severe dengue
  - Chikungunya

---

## 🗂️ Project Structure

```text
Testes Base de dados Campina Grande/
│
├── data/                     # Raw datasets (not versioned)
│
├── src/                      # Source code
│   ├── utils/                # Data processing utilities
│   │   ├── __init__.py
│   │   ├── missing.py            # Missing data analysis and metrics
│   │   ├── columns.py            # Safe column removal and filtering
│   │   ├── similarity.py         # Detection of duplicated or similar columns
│   │   ├── name_normalizer.py    # Column name normalization and standardization
│   │   ├── clinical_vocab.py     # Vocabulary of clinical terms and symptoms
│   │   ├── clinical_matcher.py   # Automatic matching of clinical-related columns
│   │   └── clinical_cleaner.py   # Cleaning and consolidation of clinical features
│   │
│   └── load_and_clean.ipynb      # Main data loading, auditing, and preprocessing pipeline
│
├── .gitignore
└── README.md

## 📊 Data Source

The data used in this project originate from the **Sistema de Informação de Agravos de Notificação (SINAN)**, Brazil’s national disease surveillance system.

The datasets were formally requested from the **Municipal Health Department of Campina Grande (Paraíba, Brazil)** and comprise notified dengue cases from the years **2018 and 2021 to 2025**.

The original files were provided in **DBF format** and contain clinical, epidemiological, sociodemographic, and administrative information related to each notified case.

Due to **privacy, ethical, and legal constraints**, the raw datasets are not publicly available and are therefore excluded from version control. This repository focuses exclusively on the data processing methodology and analytical pipeline.

## ⚙️ Requirements

The project was developed using **Python** and relies on common data science and scientific computing libraries.

Main requirements include:

- Python 3.9+
- pandas
- numpy
- matplotlib
- seaborn
- scikit-learn
- jupyter

It is recommended to run the pipeline inside a virtual environment (e.g., `venv` or `conda`) to ensure dependency isolation and reproducibility.