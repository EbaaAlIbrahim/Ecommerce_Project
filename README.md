#  E-Commerce Personalization & Retail Data Pipeline

A comprehensive, end-to-end data project that simulates a massive e-commerce platform (like Amazon or Noon). This project covers the full life cycle of data: building automated data engineering pipelines, training an AI recommendation engine, and generating actionable business intelligence reports.

##  Project Architecture Overview
The system is divided into three distinct professional roles:
1. **Data Engineering**: Extracting messy raw web server logs, cleaning formatting errors/duplicates, and loading them into a structured SQLite Data Warehouse.
2. **Data Science**: Extracting clean purchase histories to train an Item-Based Co-occurrence recommendation algorithm that predicts customer buying patterns.
3. **Data Analytics**: Querying the warehouse with SQL joins to build executive regional performance and product popularity trend reports.

---

##  Tech Stack & Prerequisites
* **Language**: Python 3.x
* **Database**: SQLite3 (Relational Data Warehouse)
* **Libraries Engine**: Pandas (Data Manipulation), Faker (Synthetic Data Generation)
* **Operating System**: Windows 10

To run this project locally, clone the repository and install the dependencies:
```bash
pip install pandas faker
```

---

##  File Structure & Execution Steps

Run the scripts in numerical order to execute the pipeline from scratch:

###  Step 1: Data Generation (`1_generate_raw_data.py`)
* **What it does**: Simulates a live e-commerce server tracking 50 products and 1,000 user logs over a 30-day period.
* **Why it matters**: It purposely injects real-world data flaws: duplicate clicks from server bugs, messy list-string formatting (`['click']`), and missing geographical regions from failed user GPS signals.

###  Step 2: Automated Data Cleaning (`2_clean_data.py`)
* **What it does**: Acts as the cleaning pipeline. It uses Regular Expressions (Regex) to scrub broken string brackets, drops identical duplicate server entries, and populates missing fields with `"Unknown"`.
* **Why it matters**: Ensures the data is 100% accurate before it enters company storage, preventing broken reports or inaccurate AI training down the line.

###  Step 3: Storing in the Warehouse (`3_store_warehouse.py`)
* **What it does**: Connects to an SQLite engine and creates two structured relational database tables (`inventory` and `user_activity`) using Primary and Foreign keys. It loads the clean datasets directly into this database schema.
* **Why it matters**: Establishes a "Single Source of Truth" where any department in the company can safely query clean data.

###  Step 4: AI Model Training (`4_train_recommendation_system.py`)
* **What it does**: The Data Science engine. It uses SQL queries to extract only verified purchase data, runs a self-join algorithm to find items frequently bought together by the same users, and computes a "Recommendation Strength" score.
* **Why it matters**: Automates personalized marketing to increase user click-through rates and average order values.

###  Step 5: Interactive Engine Test (`5_test_recommendations.py`)
* **What it does**: A command-line interface application that lets a user type in a product ID (e.g., `PROD_001`). The script searches the trained AI rules matrix and returns the top 3 items that customers bought alongside it.

###  Step 6: Business Intelligence Analytics (`6_run_business_analytics.py`)
* **What it does**: Connects to the data warehouse and runs complex analytical queries with `JOIN`, `SUM`, `COUNT`, and `GROUP BY` operations. 
* **Output Reports**: 
  * *Regional Sales Performance*: Ranks cities by total item sales and exact revenue generated.
  * *Product Category Popularity*: Pinpoints which marketplace verticals dominate volume and gross profit.
