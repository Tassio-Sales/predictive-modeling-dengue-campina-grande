\# Predictive Modeling of Dengue Cases in Campina Grande



This repository contains the data processing and exploratory analysis pipeline developed for the undergraduate thesis (TCC):



\*\*"Predictive Modeling of Dengue Cases in Campina Grande: A Machine Learning-Based Approach"\*\*



The project focuses on preparing, auditing, and analyzing epidemiological surveillance data to support the construction of predictive models for dengue case classification.



---



\## 📌 Project Objectives



\- Perform a systematic audit of missing data in real-world epidemiological datasets

\- Identify and standardize symptom, warning sign, severity, and outcome variables across multiple years

\- Prepare a clean and consistent dataset for supervised machine learning models

\- Predict the final case classification:

&nbsp; - Discarded

&nbsp; - Dengue

&nbsp; - Dengue with warning signs

&nbsp; - Severe dengue

&nbsp; - Chikungunya



---



\## 🗂️ Project Structure



```text

Testes Base de dados Campina Grande/

│

├── data/                     # Raw datasets (not versioned)

│

├── src/                      # Source code

│   ├── utils/                # Data processing utilities

│   │   ├── \_\_init\_\_.py

│   │   ├── missing.py            # Missing data analysis and metrics

│   │   ├── columns.py            # Safe column removal and filtering

│   │   ├── similarity.py         # Detection of duplicated/similar columns

│   │   ├── name\_normalizer.py    # Column name normalization and standardization

│   │   ├── clinical\_vocab.py     # Vocabulary of clinical terms and symptoms

│   │   ├── clinical\_matcher.py   # Automatic matching of clinical columns

│   │   └── clinical\_cleaner.py   # Cleaning and consolidation of clinical features

│   │

│   └── load\_and\_clean.ipynb   # Main data loading and auditing pipeline

│

├── .gitignore

└── README.md

