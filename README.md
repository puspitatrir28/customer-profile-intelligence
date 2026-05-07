# 👤 Customer Profile Intelligence Dashboard

![Python](https://img.shields.io/badge/Python-3.11-blue?style=flat-square&logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-1.x-red?style=flat-square&logo=streamlit)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-336791?style=flat-square&logo=postgresql)
![Plotly](https://img.shields.io/badge/Plotly-5.x-3F4F75?style=flat-square&logo=plotly)
![Status](https://img.shields.io/badge/Status-Completed-brightgreen?style=flat-square)

> **Group Project — Data Visualization Course**
> Analyst: **Puspita Tri Rahayu** · Information Systems, Data Science Concentration · President University

An interactive Streamlit dashboard for analyzing DVD Rental customer behavior — covering segmentation, activity monitoring, spending patterns, Customer Lifetime Value (CLV), and data-driven strategic recommendations.

---

## 📌 Project Scope

This dashboard is part of a group project analyzing the `dvdrental` PostgreSQL dataset. My contribution focuses on **Customer Profiles** — understanding who the customers are, how they behave, and how the business should respond.

---

## 🔍 Business Questions Answered

- Who are the **active customers** and who has gone silent?
- How much **revenue is at risk** from churned customers?
- How is **customer spending distributed** across the base?
- Which customers need **immediate action** today?
- What is the estimated **Customer Lifetime Value** per segment?
- What **strategic actions** should the business take right now?

---

## ✨ Key Features

| Feature | Description |
|---------|-------------|
| 🗺️ **Location Filter** | Filter all metrics by city in real-time |
| 📊 **KPI Overview** | Total customers, revenue, and avg spending at a glance |
| 🚨 **Activity & Risk Monitoring** | Active vs inactive rate with urgency classification |
| 🎯 **Active Rate Overview** | Progress bar vs 50% target with gap analysis |
| 📅 **Monthly Rental Volume** | Business trend across the full dataset timeline |
| 💰 **Spending Distribution** | Histogram with mean, median, and at-risk zone annotation |
| 📦 **Spending per Segment** | Box plot comparing At Risk, Regular, and Champions |
| ⏳ **CLV Analysis** | Lifetime vs spending scatter, violin distribution, and CLV KPIs |
| ⚙️ **Operational Insight** | Top 5 high-value at-risk customers prioritized for outreach |
| 🗂️ **Customer Directory** | Searchable, filterable, sortable full customer table with color-coded Days Since |
| 🔎 **Customer Drill Down** | Individual profile with monthly rental activity and favourite genre chart |
| 💡 **Strategic Action Plan** | 3 auto-generated recommendations that update dynamically based on data |
| 📥 **CSV Export** | Download filtered customer data by segment |

---

## 📸 Dashboard Preview

> *(Add your screenshots here after uploading to GitHub)*

| Section | Preview |
|---------|---------|
| KPI Overview | `screenshots/kpi_overview.png` |
| Activity & Risk | `screenshots/activity_risk.png` |
| Spending Distribution | `screenshots/spending_dist.png` |
| CLV Analysis | `screenshots/clv_analysis.png` |
| Customer Drill Down | `screenshots/drill_down1.png` |
| Customer Drill Down | `screenshots/drill_down2.png` |
| Strategic Action Plan | `screenshots/action_plan.png` |

---

## 🛠️ Tech Stack

| Layer | Tools |
|-------|-------|
| **Language** | Python 3.11 |
| **Web App** | Streamlit |
| **Database** | PostgreSQL 15 (dvdrental dataset) |
| **Data Processing** | Pandas |
| **Visualization** | Plotly (Express + Graph Objects) |
| **DB Connector** | psycopg2 |

---

## 📁 Project Structure

```
customer-profile-intelligence/
│
├── TITA.py                  # Main Streamlit dashboard
├── README.md                # Project documentation
├── requirements.txt         # Python dependencies
└── screenshots/             # Dashboard preview images (optional)
    ├── kpi_overview.png
    ├── activity_risk.png
    ├── spending_dist.png
    ├── clv_analysis.png
    ├── drill_down.png
    └── action_plan.png
```

---

## ⚙️ Setup & Installation

### Prerequisites
- Python 3.9+
- PostgreSQL with `dvdrental` database restored
- Git

### 1. Clone the repository
```bash
git clone https://github.com/YOUR_USERNAME/customer-profile-intelligence.git
cd customer-profile-intelligence
```

### 2. Create a virtual environment
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Set up the database

Make sure PostgreSQL is running and the `dvdrental` database is restored.
You can download the dvdrental dataset from the [official PostgreSQL tutorial](https://www.postgresqltutorial.com/postgresql-getting-started/postgresql-sample-database/).

Then update the database credentials in `TITA.py`:
```python
def get_connection():
    return psycopg2.connect(
        host="localhost",
        database="DVDRental",
        user="your_username",       # change this
        password="your_password",   # change this
        port="5432"
    )
```

### 5. Run the dashboard
```bash
streamlit run TITA.py
```

Open your browser at `http://localhost:8501`

---

## 📊 Dataset

**Source:** [dvdrental — PostgreSQL Sample Database](https://www.postgresqltutorial.com/postgresql-getting-started/postgresql-sample-database/)

| Table Used | Purpose |
|------------|---------|
| `customer` | Customer basic info |
| `address`, `city` | Geographic data |
| `rental` | Rental transaction history |
| `payment` | Revenue data |
| `inventory`, `film_category`, `category` | Genre data for drill down |

**Key Stats:**
- 599 customers across 597 cities
- Total revenue: $61,312
- Date range: May 2005 — February 2006

---

## 🧠 Methodology

### Customer Segmentation
Customers are classified into 3 segments based on two criteria:

```
Champions  → total_spent > $150 AND total_rentals > 30 AND active (≤100 days idle)
At Risk    → inactive (>100 days since last rental)
Regular    → all other active customers
```

### Activity Definition
A customer is considered **active** if their last rental was within the past **100 days** from the most recent transaction date in the dataset.

### CLV Estimation
```
Customer Lifetime (months) = (last_rental_date - first_rental_date) / 30
Spend per Month            = total_spent / customer_lifetime_months
Estimated CLV              = spend_per_month × customer_lifetime_months
```

---

## 💡 Key Insights

1. **73.6% of customers are inactive** — only 158 out of 599 customers are still active, far below the 50% target threshold.
2. **$44,864 in potential revenue loss** — this is not lost yet. With the right win-back campaign, a significant portion is recoverable.
3. **Healthy spending distribution** — mean ($102) ≈ median ($100), indicating no extreme outliers distorting the average.
4. **At Risk customers are not new customers** — they were once loyal. Win-back campaigns for them are far more cost-efficient than acquiring new customers.
5. **Only 6 Champions (1%)** — the top-tier customer base is critically thin and needs immediate retention protection.

---

## 📬 Contact

**Puspita Tri Rahayu**
Information Systems · Data Science Concentration
President University · Semester 5

[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-blue?style=flat-square&logo=linkedin)](https://linkedin.com/in/YOUR_LINKEDIN)
[![GitHub](https://img.shields.io/badge/GitHub-Follow-black?style=flat-square&logo=github)](https://github.com/YOUR_USERNAME)

---

## 📝 License

This project is built for academic purposes as part of a Data Visualization course.
Dataset used: [dvdrental](https://www.postgresqltutorial.com/postgresql-getting-started/postgresql-sample-database/) — free to use for learning purposes.
