# Customer Churn Analytics Dashboard

An interactive **Streamlit** application for exploring customer churn, reviewing model performance, identifying high-risk customers, and testing churn predictions for an individual customer.

## Features

- **Customer Churn Analysis** — churn rate by contract, payment method, and internet service; predicted risk distribution; churn by tenure.
- **High-Risk Customers** — filter and review customers ranked by predicted churn probability; export the filtered table as CSV.
- **Model Performance** — accuracy, precision, recall, F1-score, ROC-AUC, and confusion matrix.
- **Churn Predictor** — enter customer attributes and receive a prediction and estimated churn probability from the saved Gradient Boosting pipeline.

## Tech stack

- Python
- Streamlit
- Pandas
- Plotly
- scikit-learn
- imbalanced-learn
- Joblib

## Project structure

```text
churn_dashboard/
├── .streamlit/
│   └── config.toml
├── data/
│   ├── cleaned_customer_churn.csv
│   ├── confusion_matrix.csv
│   ├── customer_predictions.csv
│   └── model_metrics.csv
├── app.py
├── predictor.py
├── theme.py
├── final_churn_model.joblib
├── requirements.txt
├── run.bat
├── .gitignore
└── README.md
```

## Requirements

- Python **3.10 or newer**
- Internet connection for the initial package installation

The saved model was serialized with **scikit-learn 1.7.2**. Keep that version unchanged unless you retrain and re-export the model. The model also uses an `imbalanced-learn` pipeline, which is why `imbalanced-learn` is included in the dependencies.

## Run locally

### Windows

1. Download or clone this repository.
2. Open the project folder.
3. Double-click `run.bat`.

The script installs the dependencies and starts Streamlit.

### Any operating system (terminal)

From the project root, run:

```bash
python -m venv .venv
```

Activate the environment:

**Windows PowerShell**
```powershell
.venv\Scripts\Activate.ps1
```

**macOS / Linux**
```bash
source .venv/bin/activate
```

Install dependencies and start the app:

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

Open the local URL printed in the terminal (usually `http://localhost:8501`). Press `Ctrl+C` in the terminal to stop the app.

## Data and model notes

- The dashboard reads its CSV files from the `data/` directory. Keep the directory structure intact.
- `final_churn_model.joblib` is required by the Churn Predictor page and must remain in the project root.
- The CSV files include customer IDs. Before making this repository public, verify that the dataset is permitted for public redistribution and that the IDs/data do not identify real people. Remove or anonymize any data you are not authorized to publish.
- Add the original dataset source, attribution, and applicable dataset license here once verified. Do not assume that the model or dataset is free to redistribute simply because it is included in this project.
- Only load Joblib/pickle model files from sources you trust; these formats can execute code during loading.

## Model evaluation

The metrics shown in the dashboard are stored in `data/model_metrics.csv`, and the confusion matrix is stored in `data/confusion_matrix.csv`. They describe the saved model's evaluation; they are not recalculated when the dashboard starts.

## Troubleshooting

- **`python` is not recognized:** install Python 3.10+ and enable **Add Python to PATH**, then reopen the terminal.
- **Model loading or import error:** install all packages with `python -m pip install -r requirements.txt`. In particular, the saved pipeline requires `imbalanced-learn` and scikit-learn 1.7.2.
- **Port 8501 is busy:** run `python -m streamlit run app.py --server.port 8502`.

## License

No license has been added yet. If you plan to make this repository public, choose a license only after confirming that you have the rights to license the code and redistribute the included dataset and model.
