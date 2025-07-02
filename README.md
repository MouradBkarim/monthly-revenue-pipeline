# 📊 Monthly Customer Revenue Data Mart

This project demonstrates a full data stack workflow for building a **Snowflake-based data mart** with data quality and orchestration practices.

It uses:

✅ **dbt** (transformations and tests)
✅ **Soda** (data quality scans)
✅ **Airflow (Astro)** (orchestration)
✅ **Snowflake** (cloud data warehouse)

---

## 🚀 Use Case

> **Goal:** Build a data mart that tracks **Monthly Revenue per Customer by Region and Nation**.

It answers business questions like:

- _How much revenue did each customer generate per month?_
- _What is the breakdown by region and nation?_
- _How do discounts affect net revenue?_

---

## 📂 Project Structure

```
.
├── .astro/
├── dags/
│   └── dag.py
├── include/
│   └── dbt/
│       ├── cosmos_config.py
│       ├── models/
│           ├── staging/
│           ├── intermediate/
│           ├── marts/
│       └── tests/
│       ├── macros/
│           ├── revenu.sql
│       └── seeds/
│       └── snapshots/
│       ├── .......
│   └── soda/
│       ├── configuration.yml
│       ├── .....
└── .gitignore
```

### ➜ Staging Layer

- Clean, renamed, typed data from Snowflake `SNOWFLAKE_SAMPLE_DATA.TPCH_SF1`.
- Source freshness and relationship tests (dbt).

### ➜ Intermediate Layer

- Business logic joins:

  - Orders + LineItem → Order Items with discount and revenue calcs.
  - Customers enriched with Nation and Region.

### ➜ Marts Layer

- Final fact table:

  - **Monthly revenue per customer, region, nation**.
  - With/without discount columns.

- Tests for accepted values, uniqueness, not nulls.

---

## 🧪 Data Quality

### ✅ dbt Tests

- Source-level tests (freshness, relationships).
- Model-level tests (accepted values, uniqueness, not nulls).

### ✅ Soda Checks

- **Pre-transformation**: Validate source volumes and expected patterns.
- **Post-transformation**: Ensure transformed models meet business rules.

---

## ⚙️ Orchestration

Orchestrated with **Airflow** using **Astro Runtime**.

- DAG runs:
  1️⃣ **Pre-load checks** (Soda scans on raw sources)
  2️⃣ **dbt source tests** (alternative approach)
  3️⃣ **Staging models**
  4️⃣ **Intermediate models**
  5️⃣ **Mart models + dbt tests**
  6️⃣ **Post-transform checks** (Soda scans on marts)

- Astro environment runs tasks in **virtualenvs** to support Soda, dbt-snowflake.

---

## 🔗 How to Run Locally

### 1️⃣ Prerequisites

- Snowflake trial account
- Soda trial account
- Astro CLI
- Python 3.11+

### 2️⃣ Clone and Set Up

```bash
git clone https://github.com/yourusername/monthly-customer-revenue
cd monthly-customer-revenue

# Copy and edit your .env
cp .env.example .env

# Init astro
astro dev init

```

> Store your Snowflake creds and Soda keys in .env.

### 3️⃣ Snowflake setup

Before running this project, make sure your Snowflake environment is prepared.

This repo includes a ready-to-run SQL script to set up the warehouse, database, role, and schema required for dbt.

➡️ Script location: **infrastructure/snowflake_setup.sql**

### 4️⃣ Start Astro

```bash
# compile
dbt compile --project-dir ./include/dbt --profiles-dir ./include/dbt

# run tests
dbt test --project-dir ./include/dbt --profiles-dir ./include/dbt --profile data_pipeline --target dev

# run Airflow
astro dev start --no-cache
```

### 5️⃣ Access Airflow

- Web UI: [http://localhost:8080](http://localhost:8080)
- Trigger the DAG: **monthly_customers_revenu_dag**

---

## ✅ CI/CD with GitHub Actions

This project includes a **ready-to-use GitHub Actions workflow** that runs automated **CI checks** on every push and pull request.

---

### ⚙️ What It Does

When you **push** to `main` or open a **Pull Request**, GitHub Actions will:

✅ Install Python 3.11
✅ Install `dbt-snowflake`
✅ Install `soda-snowflake` (for consistency with local dev)
✅ Install project dependencies (`dbt deps`)
✅ Compile the dbt project (`dbt compile`)
✅ Run all dbt tests (`dbt test`)

---

### 📂 Workflow File

The workflow file lives at:

```
.github/workflows/dbt-ci.yml
```

---

🔐 Secrets Management
This project does not include any real credentials in the repo.

✅ You should add GitHub Actions secrets in your repository settings to provide your Snowflake and Soda credentials safely.

---

✅ Recommended GitHub Actions secrets:

- `SNOWFLAKE_ACCOUNT`
- `SNOWFLAKE_USER`
- `SNOWFLAKE_PASSWORD`
- `SODA_CLOUD_HOST`
- `SODA_CLOUD_API_KEY_ID`
- `SODA_CLOUD_API_KEY_SECRET`
- `SOURCE_SNOWFLAKE_WAREHOUSE`
- `SOURCE_SNOWFLAKE_DATABASE`
- `SOURCE_SNOWFLAKE_SCHEMA`
- `SOURCE_SNOWFLAKE_ROLE`
- `DST_SNOWFLAKE_WAREHOUSE`
- `DST_SNOWFLAKE_DATABASE`
- `DST_SNOWFLAKE_SCHEMA`
- `DST_SNOWFLAKE_ROLE`

---

## 📜 License

MIT License. Use and adapt freely.

---
