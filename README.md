# 🎬 Movie Box Office Prediction

## 📌 Overview

This project scrapes movie data from Wikipedia (1913–2024), cleans and preprocesses it, performs exploratory data analysis (EDA), and develops machine learning models to predict a movie’s box office revenue from its budget, release year, and title.

The goal is to walk through a complete **data science pipeline**:

1. **Data Collection** (web scraping with BeautifulSoup + requests)
2. **Data Cleaning & Preparation** (handling missing values, normalizing money data)
3. **Exploratory Data Analysis** (EDA with statistics and visualizations)
4. **Model Development** (Linear Regression, Gradient Boosting with text features)
5. **Evaluation & Reflection**

---

## 📂 Repository Structure

├── scraper.py # Web scraper for Wikipedia
├── eda.ipynb # Exploratory Data Analysis
├── model.ipynb # Model training and evaluation
├── requirements.txt # Project dependencies
├── clean_movies_dataset.csv # Cleaned dataset generated after EDA
├── images/ # Poster images (not used in modeling)
└── README.md # Project documentation

---

## 📊 Data Source

- Data Source: https://en.wikipedia.org/wiki/List_of_highest-grossing_films
- Wikipedia yearly pages: `https://en.wikipedia.org/wiki/<YEAR>_in_film`
- Table used: **Highest-grossing films** (per year)
- Time range: **1913–2024**
- Data collected:
  - Title
  - Year
  - Budget (raw string + cleaned numeric in millions USD)
  - Box Office (raw string + cleaned numeric in millions USD)
  - Poster image (downloaded but not included in modeling)

## Why this source?

- I have chosen wikipedia data because in wikipedia, data is consistently structured in yearly "Highest-grossing films" tables, making scraping easier
- it is mentioned to take data of at least 1000 rows so this is one of the largest available structured data in wikipedia
- It contains **both budget and box office values**, which are essential for regression based prediction.
- I could have taken data from sites like Amazon, but such sites block scraping, and advanced techniques are required to extract data from them
- if web scrapping is not mentioned in the document i would have easily took data from the kaggle without scraping
- so at last i was left with the option of wikipedia data only

---

## 🧹 Data Preprocessing

### 1. Cleaning

- Removed citation markers like `[1]`, `[2]` and parenthetical notes like `(estimated)`.
- Normalized Unicode (fancy quotes, dashes → ASCII).
- Converted **budget/box office** into numeric form (millions USD).
- Handled ranges like `$150–200 million` → averaged to `175M`.
- Handled plain numbers like `$981,000` → converted to `0.981M`.

### 2. Feature Engineering

- `budget_millionUSD`, `box_office_millionUSD` → numeric targets.
- `log_budget`, `log_box_office` → log-transformed features/targets for stability.
- `title_clean` → normalized movie titles (used for TF-IDF).

### 3. Handling Missing Values

- Movies without budget info were dropped from modeling dataset (`df_model`).
- Final dataset for modeling: **917 movies**.

### 4. Outlier Removal

- Extremely high budgets (e.g., > $500M) excluded to prevent skew.
- Final working dataset: **913 movies**.

---

## 🔎 Exploratory Data Analysis (EDA)

- **Summary statistics**: budgets mostly under $100M, revenues highly skewed.
- **Boxplots & histograms**: revealed long-tail distributions.
- **Correlation matrix**: budget strongly correlated with box office (r ≈ 0.86).
- **Trends over time**: budgets and revenues generally rising after 1970s.
- **Outlier analysis**: billion-dollar blockbusters (e.g., _Avatar_, _Avengers_).

---

## 🤖 Modeling Approach

Two setups were tested:

### Setup 1: Numeric only

- Features: `log_budget`, `year`
- Models:
  - **Linear Regression** (baseline)
  - **Gradient Boosting Regressor** (advanced)

### Setup 2: Numeric + Text

- Features: `log_budget`, `year`, TF-IDF of `title_clean` (max_features=500)
- Models:
  - **Linear Regression with TF-IDF**
  - **Gradient Boosting with TF-IDF**

---

## 📈 Results

### Setup 1: Numeric only

- **Linear Regression** → MAE: 0.403, RMSE: ~0.55, R²: 0.943
- **Gradient Boosting** → MAE: 0.296, RMSE: ~0.40, R²: 0.967

### Setup 2: Numeric + Text

- **Linear Regression + TF-IDF** → MAE: 0.479, R²: 0.907 (worse, due to sparse text)
- **Gradient Boosting + TF-IDF** → MAE: 0.286, R²: 0.969 (best overall)

⚡ **Best model**: Gradient Boosting with numeric + text features.

- Captures nonlinear effects.
- Leverages franchise keywords (_Star Wars_, _Avengers_, etc.).
- Achieved **~0.29 log-scale MAE → ~30% relative error in real scale**.

---

## 📊 Visualizations

- **Histograms** → budget & revenue distributions (raw vs log scale).
- **Boxplots** → outliers in budgets and revenues.
- **Scatter plots** → predicted vs actual (log scale & real scale).
- **Heatmap** → correlations among numeric features.
- **Bar charts** → model comparison (MAE, RMSE, R²).

---

## 🔮 Reflections

- **Budgets are highly predictive**, but not perfect — marketing, franchise effects, and reviews matter too.
- **Titles add slight predictive power** when using advanced models (GB).
- **Linear Regression** works surprisingly well but fails with text features.
- **Gradient Boosting** is robust to skew and outliers → best choice.
- **Limitations**:
  - Missing budgets for some movies.
  - Wikipedia estimates may be inconsistent.
  - External factors (season, competition, reviews) not included.

---

## ⚙️ Installation & Usage

Clone the repo and install dependencies:

```bash
git clone https://github.com/cschauhan0304/AI-ML-Engineer-Assignment.git
cd AI-ML-Engineer-Assignment
pip install -r requirements.txt

```

Run the scraper:
python scraper.py

Run EDA and Modeling in Jupyter:
jupyter notebook eda.ipynb
jupyter notebook model.ipynb

📦 Requirements
See requirements.txt. Main libraries:
pandas, numpy
requests, beautifulsoup4
scikit-learn, scipy
matplotlib, seaborn

🙌 Acknowledgements

Data Source: https://en.wikipedia.org/wiki/List_of_highest-grossing_films
