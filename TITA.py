import streamlit as st
import psycopg2
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# --- 1. KONFIGURASI HALAMAN ---
st.set_page_config(
    page_title="Customer Profile Intelligence",
    layout="wide",
    page_icon="👤",
    initial_sidebar_state="collapsed"
)

# --- COLOR PALETTE ---
COLORS = {
    "primary": "#3b82f6",
    "success": "#10b981",
    "warning": "#f59e0b",
    "danger": "#ef4444",
    "navy": "#0f172a",
    "slate": "#1e293b",
    "muted": "#64748b",
    "light": "#94a3b8",
    "border": "#1e293b",
}
PALETTE = ["#3b82f6", "#10b981", "#f59e0b", "#ef4444", "#8b5cf6", "#06b6d4"]

# --- 2. CSS DARK MODE ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;600;700;800&display=swap');

    html, body, [class*="css"], .stApp {
        font-family: 'Plus Jakarta Sans', sans-serif;
        background-color: #0f172a !important;
        color: #e2e8f0 !important;
    }
   
    .main-title { color: #f1f5f9; font-size: 36px; font-weight: 800; letter-spacing: -0.02em; margin-bottom: 2px; }
    .main-subtitle { color: #94a3b8; font-size: 14px; margin-bottom: 4px; }
    .main-scope-badge {
        display: inline-block;
        background: #1e3a5f;
        color: #60a5fa;
        font-size: 11px;
        font-weight: 700;
        padding: 3px 10px;
        border-radius: 99px;
        letter-spacing: 0.06em;
        text-transform: uppercase;
        margin-bottom: 20px;
    }
    .title-divider { border: none; border-top: 1px solid #1e293b; margin-bottom: 28px; }

    .section-header { color: #f1f5f9; font-size: 30px; font-weight: 800; margin-top: 48px; margin-bottom: 8px; padding-top: 8px; border-top: 3px solid #3b82f6; display: inline-block; }
    .section-desc { color: #94a3b8; font-size: 14px; margin-bottom: 16px; margin-top: 6px; }
    .sub-header { color: #cbd5e1; font-size: 15px; font-weight: 700; margin-bottom: 8px; margin-top: 4px; }

    .kpi-card {
        background: #1e293b;
        border: 1px solid #334155;
        border-radius: 14px;
        padding: 20px 22px;
        box-shadow: 0 4px 16px rgba(0,0,0,0.25);
        border-left-width: 4px;
        border-left-style: solid;
        min-height: 175px;
        height: auto;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        box-sizing: border-box;
    }
    .kpi-card-blue  { border-left-color: #3b82f6; }
    .kpi-card-green { border-left-color: #10b981; }
    .kpi-card-amber { border-left-color: #f59e0b; }
    .kpi-card-red   { border-left-color: #ef4444; }
    .kpi-card-purple { border-left-color: #8b5cf6; }
    .kpi-label { color: #64748b; font-size: 11px; font-weight: 700; letter-spacing: 0.08em; text-transform: uppercase; margin-bottom: 8px; }
    .kpi-value { color: #f1f5f9; font-size: 30px; font-weight: 800; line-height: 1.1; margin-bottom: 6px; }
    .kpi-icon { font-size: 18px; margin-bottom: 10px; }
    .kpi-badge { display: inline-block; font-size: 11px; font-weight: 600; padding: 2px 8px; border-radius: 99px; margin-top: 4px; }
    .kpi-badge-blue   { background: #1e3a5f; color: #60a5fa; }
    .kpi-badge-green  { background: #14342a; color: #34d399; }
    .kpi-badge-amber  { background: #3a2e0c; color: #fbbf24; }
    .kpi-badge-red    { background: #3b1515; color: #f87171; }
    .kpi-badge-purple { background: #2e1a5f; color: #c4b5fd; }

    .chart-card { background: #1e293b; border: 1px solid #334155; border-radius: 14px; padding: 20px 20px 8px 20px; box-shadow: 0 4px 16px rgba(0,0,0,0.25); margin-bottom: 8px; }

    /* Progress bar Active Rate */
    .active-rate-wrap { padding: 8px 0 4px 0; }
    .active-rate-bar-bg {
        background: #0f172a;
        border-radius: 99px;
        height: 18px;
        width: 100%;
        overflow: hidden;
        margin: 10px 0 6px 0;
        border: 1px solid #334155;
    }
    .active-rate-bar-fill {
        height: 100%;
        border-radius: 99px;
        transition: width 0.3s ease;
        display: flex;
        align-items: center;
        justify-content: flex-end;
        padding-right: 8px;
    }
    .rate-row { display: flex; justify-content: space-between; font-size: 12px; color: #64748b; margin-top: 4px; }
    .target-line-label { font-size: 11px; color: #f59e0b; margin-top: 6px; }

    [data-baseweb="select"] > div { background-color: #1e293b !important; border-color: #334155 !important; color: #e2e8f0 !important; }
    [data-baseweb="menu"] { background-color: #1e293b !important; }
    [data-baseweb="option"] { background-color: #1e293b !important; color: #e2e8f0 !important; }
    [data-baseweb="option"]:hover { background-color: #334155 !important; }

    .stDownloadButton button { background-color: #3b82f6 !important; color: white !important; border-radius: 10px !important; border: none !important; padding: 0.5rem 1rem !important; font-weight: 600 !important; width: 100% !important; }
    .stDownloadButton button:hover { background-color: #2563eb !important; color: white !important; }
    
    .stMarkdown p, .stMarkdown li, .stMarkdown h1, .stMarkdown h2, .stMarkdown h3 { color: #e2e8f0 !important; }
    .stCaption { color: #64748b !important; }
    hr { border-color: #1e293b !important; }

    .footer { margin-top: 60px; padding: 20px 0 10px 0; border-top: 1px solid #1e293b; color: #475569; font-size: 13px; text-align: center; }
    .empty-state { text-align: center; padding: 60px 20px; color: #64748b; font-size: 15px; }
    .empty-state-icon { font-size: 48px; margin-bottom: 12px; }

    .rec-card-green, .rec-card-red, .rec-card-blue {
        padding: 20px;
        border-radius: 12px;
        height: 100%;
        min-height: 220px;
        display: flex;
        flex-direction: column;
        justify-content: flex-start;
        box-sizing: border-box;
    }
    .rec-card-green  { background-color: #0d2419; border-left: 5px solid #10b981; }
    .rec-card-red    { background-color: #200d0d; border-left: 5px solid #ef4444; }
    .rec-card-blue   { background-color: #0d1a2e; border-left: 5px solid #3b82f6; }
    .rec-card-green p, .rec-card-red p, .rec-card-blue p { font-size: 13px; flex: 1; margin: 0; }

    .insight-box {
        background: #0f172a;
        border: 1px solid #334155;
        border-left: 4px solid #3b82f6;
        border-radius: 10px;
        padding: 14px 18px;
        font-size: 13px;
        color: #94a3b8;
        line-height: 1.7;
        margin-top: 12px;
    }
    .insight-box b { color: #e2e8f0; }

    [data-baseweb="tag"] { background-color: #3b82f6 !important; color: white !important; }
    [data-baseweb="tag"] span { color: white !important; }
    .stMultiSelect [data-baseweb="select"] > div { background-color: #0f172a !important; border-color: #334155 !important; }
    [data-testid="collapsedControl"] { display: none !important; }
    section[data-testid="stSidebar"] { display: none !important; }
    [data-testid="stMetricValue"] { color: #f1f5f9 !important; }
    [data-testid="stMetricLabel"] { color: #94a3b8 !important; }
    [data-testid="stMetricDelta"] svg { display: none; }
    </style>
    """, unsafe_allow_html=True)

# --- MAIN TITLE ---
st.markdown("""
<div class="main-title">Customer Profile Intelligence</div>
<div class="main-subtitle">Analisis perilaku dan profil pelanggan DVD Rental — segmentasi, aktivitas, dan peluang retensi.</div>
<div class="main-scope-badge">📌 Scope: Customer Profiles · Part of Group Analysis Project</div>
<hr class="title-divider"/>
""", unsafe_allow_html=True)

# --- 3. DATABASE CONNECTION ---
def get_connection():
    return psycopg2.connect(
        host="localhost", database="DVDRental",
        user="postgres", password="Puspita281205", port="5432"
    )

@st.cache_data
def load_data():
    try:
        conn = get_connection()
        query = """
        WITH first_rentals AS (
            SELECT customer_id, MIN(rental_date) AS first_rental_date
            FROM rental GROUP BY customer_id
        )
        SELECT
            c.customer_id,
            CONCAT(c.first_name, ' ', c.last_name) AS customer_name,
            c.email,
            ct.city,
            c.create_date AS acquisition_date,
            fr.first_rental_date,
            COUNT(DISTINCT r.rental_id) AS total_rentals,
            COALESCE(SUM(p.amount), 0) AS total_spent,
            MAX(r.rental_date) AS last_rental_date
        FROM customer c
        JOIN address a ON c.address_id = a.address_id
        JOIN city ct ON a.city_id = ct.city_id
        JOIN first_rentals fr ON c.customer_id = fr.customer_id
        LEFT JOIN rental r ON c.customer_id = r.customer_id
        LEFT JOIN payment p ON r.rental_id = p.rental_id
        GROUP BY c.customer_id, ct.city, fr.first_rental_date,
                 c.first_name, c.last_name, c.email, c.create_date
        """
        df = pd.read_sql(query, conn)
        conn.close()
        df['last_rental_date']  = pd.to_datetime(df['last_rental_date'])
        df['first_rental_date'] = pd.to_datetime(df['first_rental_date'])
        latest = df['last_rental_date'].max()
        df['days_since_last_rental'] = (latest - df['last_rental_date']).dt.days

        # --- CLV FIELDS ---
        # Customer lifetime dalam hari (first → last rental)
        df['customer_lifetime_days'] = (
            df['last_rental_date'] - df['first_rental_date']
        ).dt.days.clip(lower=1)
        # Lifetime dalam bulan (min 1)
        df['customer_lifetime_months'] = (df['customer_lifetime_days'] / 30).clip(lower=1)
        # Spending per bulan aktif
        df['spend_per_month'] = df['total_spent'] / df['customer_lifetime_months']
        # Rentals per bulan aktif
        df['rentals_per_month'] = df['total_rentals'] / df['customer_lifetime_months']
        return df
    except Exception as e:
        st.error(f"Error Database: {e}")
        return pd.DataFrame()

@st.cache_data
def load_early_spending():
    conn = get_connection()
    query = """
    SELECT
        c.customer_id,
        COALESCE(SUM(CASE
            WHEN r.rental_date <= (
                SELECT MIN(r2.rental_date) + INTERVAL '30 days'
                FROM rental r2 WHERE r2.customer_id = c.customer_id
            ) THEN p.amount ELSE 0
        END), 0) AS early_spending
    FROM customer c
    LEFT JOIN rental r ON c.customer_id = r.customer_id
    LEFT JOIN payment p ON r.rental_id = p.rental_id
    GROUP BY c.customer_id
    """
    df_early = pd.read_sql(query, conn)
    conn.close()
    return df_early

@st.cache_data
def load_rental_history(customer_ids: tuple):
    conn = get_connection()
    ids_str = ','.join(map(str, customer_ids))
    query = f"""
    SELECT r.customer_id, r.rental_date, r.return_date, c.name AS genre
    FROM rental r
    JOIN inventory i      ON r.inventory_id  = i.inventory_id
    JOIN film_category fc ON i.film_id        = fc.film_id
    JOIN category c       ON fc.category_id   = c.category_id
    WHERE r.customer_id IN ({ids_str})
    ORDER BY r.rental_date
    """
    df_hist = pd.read_sql(query, conn)
    conn.close()
    df_hist['rental_date'] = pd.to_datetime(df_hist['rental_date'])
    return df_hist

@st.cache_data
def load_monthly_volume():
    """Total volume rental per bulan dari SELURUH dataset — untuk trend chart yang bermakna."""
    conn = get_connection()
    query = """
    SELECT
        DATE_TRUNC('month', rental_date) AS month,
        COUNT(*) AS total_rentals
    FROM rental
    GROUP BY 1
    ORDER BY 1
    """
    df_vol = pd.read_sql(query, conn)
    conn.close()
    df_vol['month'] = pd.to_datetime(df_vol['month'])
    return df_vol


def classify_refined_segment(row):
    is_high_revenue   = row['total_spent'] > 150
    is_frequent_renter = row['total_rentals'] > 30
    is_active          = row['days_since_last_rental'] <= 100
    if is_high_revenue and is_frequent_renter and is_active:
        return 'Champions'
    elif not is_active:
        return 'At Risk'
    else:
        return 'Regular'

def clean_layout():
    return dict(
        plot_bgcolor="#1e293b",
        paper_bgcolor="#1e293b",
        font=dict(family="Plus Jakarta Sans", color="#e2e8f0"),
        xaxis=dict(showgrid=True, gridcolor="#334155", zeroline=False, color="#94a3b8"),
        yaxis=dict(showgrid=True, gridcolor="#334155", zeroline=False, color="#94a3b8"),
        margin=dict(t=10, b=10, l=10, r=10),
        legend=dict(bgcolor="#1e293b", bordercolor="#334155", font=dict(color="#e2e8f0"))
    )

def render_html_table(df_display):
    seg_color = {'Champions': '#10b981', 'At Risk': '#ef4444', 'Regular': '#3b82f6'}
    rows_html = ""
    for _, row in df_display.iterrows():
        sc = seg_color.get(row['segment'], '#3b82f6')
        status_icon = '🟢' if row['days_since_last_rental'] <= 100 else '🔴'
        last_rental = pd.to_datetime(row['last_rental_date']).strftime('%d %b %Y') if pd.notna(row['last_rental_date']) else '-'
        days_val = row['days_since_last_rental']
        if days_val <= 100:
            days_color = '#10b981'
        elif days_val <= 200:
            days_color = '#f59e0b'
        else:
            days_color = '#ef4444'

        rows_html += f"""
        <tr style="border-bottom: 1px solid #334155;">
            <td style="padding:10px 14px; color:#f1f5f9; font-weight:600;">{row['customer_name']}</td>
            <td style="padding:10px 14px; color:#94a3b8; font-size:12px;">{row['email']}</td>
            <td style="padding:10px 14px; color:#e2e8f0;">{row['city']}</td>
            <td style="padding:10px 14px;">
                <span style="background:{sc}22; color:{sc}; padding:2px 10px; border-radius:99px; font-size:12px; font-weight:600;">
                    {row['segment']}
                </span>
            </td>
            <td style="padding:10px 14px; color:#e2e8f0;">{status_icon} {'Active' if row['days_since_last_rental'] <= 100 else 'Inactive'}</td>
            <td style="padding:10px 14px; color:#60a5fa; font-weight:700;">${row['total_spent']:,.2f}</td>
            <td style="padding:10px 14px; color:#e2e8f0; text-align:center;">{int(row['total_rentals'])}</td>
            <td style="padding:10px 14px; color:#94a3b8; font-size:12px;">{last_rental}</td>
            <td style="padding:10px 14px; color:{days_color}; text-align:center; font-weight:600;">{int(days_val)}</td>
        </tr>
        """
    legend_html = """
    <div style="padding:8px 14px 10px 14px; background:#0f172a; border-bottom:1px solid #334155;
                font-size:11px; color:#64748b; display:flex; gap:20px; align-items:center;">
        <span style="font-weight:700; text-transform:uppercase; letter-spacing:0.06em;">Days Since — Color Key:</span>
        <span><span style="color:#10b981;">■</span>&nbsp; ≤ 100 days (Active)</span>
        <span><span style="color:#f59e0b;">■</span>&nbsp; 101–200 days (Warning)</span>
        <span><span style="color:#ef4444;">■</span>&nbsp; > 200 days (High Risk)</span>
    </div>
    """
    return f"""
    <div style="overflow-x:auto; overflow-y:auto; max-height:420px; border-radius:10px; border:1px solid #334155; background:#1e293b;">
    <table style="width:100%; border-collapse:collapse; font-family:'Plus Jakarta Sans',sans-serif; font-size:13px;">
        <thead style="position:sticky; top:0; z-index:1;">
            <tr style="background:#0f172a; border-bottom:2px solid #334155;">
                <th style="padding:12px 14px; text-align:left; color:#94a3b8; font-size:11px; letter-spacing:0.08em; text-transform:uppercase; white-space:nowrap;">Customer Name</th>
                <th style="padding:12px 14px; text-align:left; color:#94a3b8; font-size:11px; letter-spacing:0.08em; text-transform:uppercase;">Email</th>
                <th style="padding:12px 14px; text-align:left; color:#94a3b8; font-size:11px; letter-spacing:0.08em; text-transform:uppercase;">City</th>
                <th style="padding:12px 14px; text-align:left; color:#94a3b8; font-size:11px; letter-spacing:0.08em; text-transform:uppercase;">Segment</th>
                <th style="padding:12px 14px; text-align:left; color:#94a3b8; font-size:11px; letter-spacing:0.08em; text-transform:uppercase;">Status</th>
                <th style="padding:12px 14px; text-align:left; color:#94a3b8; font-size:11px; letter-spacing:0.08em; text-transform:uppercase;">Total Spent</th>
                <th style="padding:12px 14px; text-align:center; color:#94a3b8; font-size:11px; letter-spacing:0.08em; text-transform:uppercase;">Rentals</th>
                <th style="padding:12px 14px; text-align:left; color:#94a3b8; font-size:11px; letter-spacing:0.08em; text-transform:uppercase; white-space:nowrap;">Last Rental</th>
                <th style="padding:12px 14px; text-align:center; color:#94a3b8; font-size:11px; letter-spacing:0.08em; text-transform:uppercase; white-space:nowrap;">Days Since ⓘ</th>
            </tr>
            <tr><td colspan="9" style="padding:0;">{legend_html}</td></tr>
        </thead>
        <tbody>{rows_html}</tbody>
    </table>
    </div>
    """

# ─── LOAD & SEGMENT ─────────────────────────────────────────
df = load_data()
df['segment'] = df.apply(classify_refined_segment, axis=1)

# ─── FILTER BAR ─────────────────────────────────────────────
st.markdown("""
<div style="background:#1e293b; border:1px solid #334155; border-radius:14px;
            padding:16px 20px; margin-bottom:24px;">
    <div style="color:#94a3b8; font-size:11px; font-weight:700;
                letter-spacing:0.08em; text-transform:uppercase; margin-bottom:10px;">
        🗺️ Filter by Location
    </div>
""", unsafe_allow_html=True)

col_filter, col_download = st.columns([4, 1])
with col_filter:
    city_options = ["All Cities"] + sorted(df["city"].unique().tolist())
    city_filter_sel = st.selectbox("", options=city_options, label_visibility="collapsed")
    city_filter = sorted(df["city"].unique().tolist()) if city_filter_sel == "All Cities" else [city_filter_sel]

with col_download:
    df_preview = df[df["city"].isin(city_filter)].copy() if city_filter else df.copy()
    st.download_button(
        label="⬇️ Export CSV",
        data=df_preview.to_csv(index=False).encode('utf-8'),
        file_name='customer_profile_data.csv',
        mime='text/csv',
        use_container_width=True,
    )
st.markdown("</div>", unsafe_allow_html=True)

if not df.empty:

    @st.cache_data
    def convert_df(df_to_download):
        return df_to_download.to_csv(index=False).encode('utf-8')

    if not city_filter:
        st.markdown("""
        <div class="empty-state">
            <div class="empty-state-icon">🗺️</div>
            <strong>No cities selected.</strong><br>
            Please select at least one location to display data.
        </div>
        """, unsafe_allow_html=True)
        st.stop()

    df_f = df[df["city"].isin(city_filter)].copy()

    # ─── KPI CALCULATIONS ────────────────────────────────────
    t_cust        = len(df_f)
    total_revenue = df_f['total_spent'].sum()
    avg_spending  = df_f['total_spent'].mean() if t_cust > 0 else 0
    median_spending = df_f['total_spent'].median()

    active_count   = len(df_f[df_f['days_since_last_rental'] <= 100])
    inactive_count = t_cust - active_count
    active_rate    = (active_count / t_cust * 100) if t_cust > 0 else 0
    inactive_rate  = 100 - active_rate

    at_risk_customers = df_f[df_f['segment'] == 'At Risk']
    risk_count      = len(at_risk_customers)
    risk_pct        = (risk_count / t_cust * 100) if t_cust > 0 else 0
    risk_exposure   = at_risk_customers['total_spent'].sum()
    avg_days_at_risk = at_risk_customers['days_since_last_rental'].mean() if risk_count > 0 else 0

    if avg_days_at_risk <= 130:
        urgency_label, urgency_badge = "🟡 Recoverable", "kpi-badge-amber"
    elif avg_days_at_risk <= 200:
        urgency_label, urgency_badge = "🔴 High Urgency", "kpi-badge-red"
    else:
        urgency_label, urgency_badge = "💀 Near Lost", "kpi-badge-red"

    df_early = load_early_spending()
    df_f = df_f.merge(df_early, on='customer_id', how='left')
    avg_early_spending    = df_f['early_spending'].mean() if t_cust > 0 else 0
    avg_lifetime_spending = df_f['total_spent'].mean() if t_cust > 0 else 0
    spending_growth_pct   = (
        ((avg_lifetime_spending - avg_early_spending) / avg_early_spending) * 100
        if avg_early_spending > 0 else 0
    )

    # ─── BARIS 1: OVERVIEW KPI ───────────────────────────────
    k1, k2, k3 = st.columns(3)
    with k1:
        st.markdown(f"""
        <div class="kpi-card kpi-card-blue">
            <div class="kpi-icon">👥</div>
            <div class="kpi-label">Total Customers</div>
            <div class="kpi-value">{t_cust:,}</div>
            <div><span class="kpi-badge kpi-badge-blue">📍 {df_f['city'].nunique()} Cities</span></div>
        </div>""", unsafe_allow_html=True)
    with k2:
        st.markdown(f"""
        <div class="kpi-card kpi-card-green">
            <div class="kpi-icon">💰</div>
            <div class="kpi-label">Total Revenue</div>
            <div class="kpi-value">${total_revenue:,.0f}</div>
            <div><span class="kpi-badge kpi-badge-green">📈 +{spending_growth_pct:.1f}% lifetime growth</span></div>
        </div>""", unsafe_allow_html=True)
    with k3:
        skew_gap = avg_spending - median_spending
        st.markdown(f"""
        <div class="kpi-card kpi-card-amber">
            <div class="kpi-icon">📈</div>
            <div class="kpi-label">Average Spending</div>
            <div class="kpi-value">${avg_spending:.2f}</div>
            <div style="display:flex; gap:6px; flex-wrap:wrap;">
                <span class="kpi-badge kpi-badge-amber">Median ${median_spending:.2f}</span>
                <span class="kpi-badge kpi-badge-amber">{'⚠️ Outlier-driven' if skew_gap > 20 else '✅ Healthy spread'}</span>
            </div>
        </div>""", unsafe_allow_html=True)

    # ─── DIVIDER ─────────────────────────────────────────────
    st.markdown("""
    <div style="margin: 32px 0 20px 0;">
        <div style="display:flex; align-items:center; gap:14px;">
            <div style="flex:1; height:1px; background:#334155;"></div>
            <span style="color:#64748b; font-size:11px; font-weight:700; letter-spacing:0.1em; text-transform:uppercase; white-space:nowrap;">
                📊 Customer Activity & Risk
            </span>
            <div style="flex:1; height:1px; background:#334155;"></div>
        </div>
    </div>""", unsafe_allow_html=True)

    # ─── BARIS 2: ACTIVITY & RISK KPI ────────────────────────
    k4, k5, k6 = st.columns(3)
    with k4:
        st.markdown(f"""
        <div class="kpi-card kpi-card-green">
            <div class="kpi-icon">🟢</div>
            <div class="kpi-label">Active Customers</div>
            <div class="kpi-value">{active_count:,}</div>
            <div style="display:flex; gap:6px; flex-wrap:wrap;">
                <span class="kpi-badge kpi-badge-green">{active_rate:.1f}% of Total</span>
                <span class="kpi-badge kpi-badge-green">≤ 100 days idle</span>
            </div>
        </div>""", unsafe_allow_html=True)
    with k5:
        st.markdown(f"""
        <div class="kpi-card kpi-card-red">
            <div class="kpi-icon">🔴</div>
            <div class="kpi-label">Inactive Customers</div>
            <div class="kpi-value">{inactive_count:,}</div>
            <div style="display:flex; gap:6px; flex-wrap:wrap;">
                <span class="kpi-badge kpi-badge-red">{inactive_rate:.1f}% of Total</span>
                <span class="kpi-badge kpi-badge-red">> 100 days idle</span>
            </div>
        </div>""", unsafe_allow_html=True)
    with k6:
        st.markdown(f"""
        <div class="kpi-card kpi-card-red">
            <div class="kpi-icon">🚨</div>
            <div class="kpi-label">Potential Revenue Loss</div>
            <div class="kpi-value">${risk_exposure:,.0f}</div>
            <div style="display:flex; gap:6px; flex-wrap:wrap;">
                <span class="kpi-badge kpi-badge-red">{risk_pct:.1f}% Population at Risk</span>
                <span class="kpi-badge kpi-badge-red">⌀ {avg_days_at_risk:.0f} days gone</span>
                <span class="kpi-badge {urgency_badge}">{urgency_label}</span>
            </div>
        </div>""", unsafe_allow_html=True)

    # ─── PERBAIKAN #1: Gauge → Progress Bar + Trend → Monthly Volume ─
    st.markdown("<div style='margin-top:28px;'></div>", unsafe_allow_html=True)
    rate_col, trend_col = st.columns([1, 1])

    # --- KIRI: Active Rate Overview pakai Plotly (aman di dalam st.columns) ---
    with rate_col:
        bar_color       = "#10b981" if active_rate >= 50 else "#ef4444"
        gap_from_target = active_rate - 50
        gap_label = (f"▲ +{gap_from_target:.1f}% di atas target"
                     if gap_from_target >= 0
                     else f"▼ {abs(gap_from_target):.1f}% di bawah target 50%")
        gap_color = "#10b981" if gap_from_target >= 0 else "#ef4444"
        need_to_activate = max(0, round(t_cust * 0.5) - active_count)

        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        st.markdown('<p class="sub-header">🎯 Active Rate Overview</p>', unsafe_allow_html=True)
        st.caption("Target: minimal 50% customer base aktif dalam 100 hari terakhir.")

        # Angka besar + gap label
        st.markdown(
            f"<div style='display:flex;justify-content:space-between;align-items:baseline;"
            f"margin-bottom:8px;'>"
            f"<span style='font-size:42px;font-weight:800;color:#f1f5f9;line-height:1;'>"
            f"{active_rate:.1f}%</span>"
            f"<span style='font-size:13px;color:{gap_color};font-weight:700;'>{gap_label}</span>"
            f"</div>",
            unsafe_allow_html=True
        )

        # Horizontal bar chart pakai Plotly — pasti render
        fig_bar = go.Figure()
        # Inactive bar (background)
        fig_bar.add_trace(go.Bar(
            x=[inactive_rate], y=["Active Rate"],
            orientation='h',
            marker_color="rgba(239,68,68,0.2)",
            name=f"Inactive ({inactive_rate:.1f}%)",
            text=f"🔴 {inactive_count} tidak aktif",
            textposition="inside",
            insidetextanchor="end",
            textfont=dict(color="#f87171", size=11),
        ))
        # Active bar (foreground)
        fig_bar.add_trace(go.Bar(
            x=[active_rate], y=["Active Rate"],
            orientation='h',
            marker_color=bar_color,
            name=f"Active ({active_rate:.1f}%)",
            text=f"🟢 {active_count} aktif",
            textposition="inside",
            insidetextanchor="start",
            textfont=dict(color="white", size=11),
        ))
        # Garis target 50%
        fig_bar.add_vline(
            x=50, line_dash="dash", line_color="#f59e0b", line_width=2,
            annotation_text="Target 50%",
            annotation_position="top",
            annotation_font_color="#f59e0b",
            annotation_font_size=10,
        )
        fig_bar.update_layout(
            barmode='stack',
            plot_bgcolor="#1e293b", paper_bgcolor="#1e293b",
            font=dict(family="Plus Jakarta Sans", color="#e2e8f0"),
            xaxis=dict(range=[0, 100], showgrid=False, zeroline=False,
                       showticklabels=False, color="#94a3b8"),
            yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            margin=dict(t=28, b=4, l=4, r=4),
            height=75,
            showlegend=False,
        )
        st.plotly_chart(fig_bar, use_container_width=True, config={"displayModeBar": False})

        # Mini stats — inline side by side, compact
        st.markdown(
            f"<div style='display:grid;grid-template-columns:1fr 1fr;gap:8px;margin-top:4px;'>"
            # kiri
            f"<div style='background:#0f172a;border-radius:8px;padding:10px 12px;border:1px solid #334155;'>"
            f"<div style='font-size:10px;color:#64748b;text-transform:uppercase;letter-spacing:0.06em;margin-bottom:2px;'>Perlu diaktifkan</div>"
            f"<div style='font-size:20px;font-weight:800;color:#ef4444;line-height:1.1;'>{need_to_activate}</div>"
            f"<div style='font-size:10px;color:#64748b;margin-top:2px;'>pelanggan untuk capai target</div>"
            f"</div>"
            # kanan
            f"<div style='background:#0f172a;border-radius:8px;padding:10px 12px;border:1px solid #334155;'>"
            f"<div style='font-size:10px;color:#64748b;text-transform:uppercase;letter-spacing:0.06em;margin-bottom:2px;'>Threshold aktif</div>"
            f"<div style='font-size:20px;font-weight:800;color:#f59e0b;line-height:1.1;'>100 hari</div>"
            f"<div style='font-size:10px;color:#64748b;margin-top:2px;'>sejak rental terakhir</div>"
            f"</div>"
            f"</div>",
            unsafe_allow_html=True
        )
        st.markdown('</div>', unsafe_allow_html=True)

    # --- KANAN: Monthly Rental Volume — data bermakna, banyak titik ---
    with trend_col:
        df_vol = load_monthly_volume()
        fig_vol = px.bar(
            df_vol, x='month', y='total_rentals',
            color_discrete_sequence=["#3b82f6"],
            labels={'month': 'Month', 'total_rentals': 'Total Rentals'}
        )
        # Tambahkan line trend di atas bar
        fig_vol.add_trace(go.Scatter(
            x=df_vol['month'], y=df_vol['total_rentals'],
            mode='lines+markers',
            line=dict(color='#10b981', width=2),
            marker=dict(size=5, color='#10b981'),
            name='Trend',
            showlegend=True
        ))
        layout = clean_layout()
        layout['legend'] = dict(
            orientation="h", yanchor="top", y=1.12,
            xanchor="right", x=1,
            font=dict(color="#e2e8f0", size=11), bgcolor="rgba(0,0,0,0)"
        )
        layout['xaxis'] = dict(showgrid=True, gridcolor="#334155", zeroline=False,
                               color="#94a3b8", tickangle=-35)
        layout['margin'] = dict(t=10, b=40, l=40, r=10)
        layout['height'] = 340
        fig_vol.update_layout(**layout, bargap=0.15)

        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        st.markdown('<p class="sub-header">📅 Monthly Rental Volume (All Customers)</p>', unsafe_allow_html=True)
        st.caption("Total transaksi rental per bulan dari seluruh dataset — menunjukkan tren bisnis nyata.")
        st.plotly_chart(fig_vol, use_container_width=True, config={"displayModeBar": False})
        st.markdown('</div>', unsafe_allow_html=True)

    # ─── SPENDING DISTRIBUTION ───────────────────────────────
    st.markdown('<h2 class="section-header">💰 Spending Distribution</h2>', unsafe_allow_html=True)
    st.markdown('<p class="section-desc">Pemahaman tentang sebaran pengeluaran di seluruh customer base.</p>', unsafe_allow_html=True)

    dist_col, box_col = st.columns([3, 2])

    with dist_col:
        fig_hist = px.histogram(
            df_f, x='total_spent', nbins=40,
            color_discrete_sequence=[COLORS["primary"]],
            labels={'total_spent': 'Total Spending ($)', 'count': 'Number of Customers'}
        )
        mean_val   = df_f['total_spent'].mean()
        median_val = df_f['total_spent'].median()
        max_val    = df_f['total_spent'].max()
        at_risk_threshold = 180

        fig_hist.add_vline(x=mean_val, line_dash="dash", line_color=COLORS["warning"],
            annotation_text=f"Mean ${mean_val:.0f}", annotation_position="top right",
            annotation_font_color=COLORS["warning"])
        fig_hist.add_vline(x=median_val, line_dash="dot", line_color=COLORS["success"],
            annotation_text=f"Median ${median_val:.0f}", annotation_position="top left",
            annotation_font_color=COLORS["success"])
        fig_hist.add_vrect(x0=at_risk_threshold, x1=max_val + 5,
            fillcolor="rgba(239, 68, 68, 0.08)", layer="below", line_width=0)
        fig_hist.add_vline(x=at_risk_threshold, line_dash="dot",
            line_color="#ef4444", line_width=1.5,
            annotation_text="⚠️ High-Value At-Risk Zone (>$180)",
            annotation_position="top right",
            annotation_font_color="#ef4444", annotation_font_size=11)

        hist_layout = clean_layout()
        hist_layout['bargap'] = 0.05
        hist_layout['yaxis_title'] = "Number of Customers"
        hist_layout['height'] = 380
        hist_layout['margin'] = dict(t=20, b=40, l=50, r=20)
        fig_hist.update_layout(**hist_layout)
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        st.markdown('<p class="sub-header">Overall Spending Distribution</p>', unsafe_allow_html=True)
        st.caption("Dashed = Mean · Dotted = Median · Area merah = zona pelanggan high-value yang berisiko.")
        st.plotly_chart(fig_hist, use_container_width=True, config={"displayModeBar": False})
        st.markdown('</div>', unsafe_allow_html=True)

    # Box plot per segment (insight tambahan)
    with box_col:
        fig_box = px.box(
            df_f, x='segment', y='total_spent',
            color='segment',
            color_discrete_map={
                'Champions': '#10b981',
                'At Risk':   '#ef4444',
                'Regular':   '#3b82f6',
            },
            labels={'total_spent': 'Total Spending ($)', 'segment': 'Segment'},
            points='outliers'
        )
        fig_box.update_traces(marker=dict(size=4, opacity=0.6))
        layout_box = clean_layout()
        layout_box['showlegend'] = False
        layout_box['height'] = 380
        layout_box['margin'] = dict(t=20, b=40, l=50, r=20)
        layout_box['xaxis'] = dict(
            showgrid=False, zeroline=False, color="#94a3b8",
            categoryorder='array',
            categoryarray=['At Risk', 'Regular', 'Champions']
        )
        fig_box.update_layout(**layout_box, yaxis_title="Total Spending ($)")
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        st.markdown('<p class="sub-header">Spending per Segment</p>', unsafe_allow_html=True)
        st.caption("Distribusi spending tiap segment — box menunjukkan median & IQR, titik = outlier.")
        st.plotly_chart(fig_box, use_container_width=True, config={"displayModeBar": False})
        st.markdown('</div>', unsafe_allow_html=True)

    skew_gap_display = mean_val - median_val
    if skew_gap_display > 20:
        st.warning(f"⚠️ Mean **${skew_gap_display:.0f} lebih tinggi** dari Median — spending right-skewed, dipengaruhi segelintir high spender.")
    else:
        st.success(f"✅ Mean dan Median berdekatan (selisih: ${skew_gap_display:.0f}) — distribusi pengeluaran relatif merata.")

    # ─── PERBAIKAN #3: CLV ANALYSIS ──────────────────────────
    st.markdown('<h2 class="section-header">⏳ Customer Lifetime Value Analysis</h2>', unsafe_allow_html=True)
    st.markdown('<p class="section-desc">Seberapa lama pelanggan aktif dan berapa nilainya — fondasi untuk strategi retensi jangka panjang.</p>', unsafe_allow_html=True)

    # KPI CLV
    avg_lifetime_months  = df_f['customer_lifetime_months'].mean()
    avg_spend_per_month  = df_f['spend_per_month'].mean()
    avg_rentals_per_month = df_f['rentals_per_month'].mean()
    median_lifetime      = df_f['customer_lifetime_months'].median()

    clv_k1, clv_k2, clv_k3, clv_k4 = st.columns(4)
    with clv_k1:
        st.markdown(f"""
        <div class="kpi-card kpi-card-purple">
            <div class="kpi-icon">⏳</div>
            <div class="kpi-label">Avg Customer Lifetime</div>
            <div class="kpi-value">{avg_lifetime_months:.1f} mo</div>
            <div><span class="kpi-badge kpi-badge-purple">Median {median_lifetime:.1f} mo</span></div>
        </div>""", unsafe_allow_html=True)
    with clv_k2:
        st.markdown(f"""
        <div class="kpi-card kpi-card-blue">
            <div class="kpi-icon">💵</div>
            <div class="kpi-label">Avg Spend / Month</div>
            <div class="kpi-value">${avg_spend_per_month:.2f}</div>
            <div><span class="kpi-badge kpi-badge-blue">per bulan aktif</span></div>
        </div>""", unsafe_allow_html=True)
    with clv_k3:
        st.markdown(f"""
        <div class="kpi-card kpi-card-green">
            <div class="kpi-icon">🎬</div>
            <div class="kpi-label">Avg Rentals / Month</div>
            <div class="kpi-value">{avg_rentals_per_month:.1f}x</div>
            <div><span class="kpi-badge kpi-badge-green">frekuensi bulanan</span></div>
        </div>""", unsafe_allow_html=True)
    with clv_k4:
        # Estimasi CLV sederhana: avg spend/month × avg lifetime months
        estimated_clv = avg_spend_per_month * avg_lifetime_months
        st.markdown(f"""
        <div class="kpi-card kpi-card-amber">
            <div class="kpi-icon">🏆</div>
            <div class="kpi-label">Estimated Avg CLV</div>
            <div class="kpi-value">${estimated_clv:.0f}</div>
            <div><span class="kpi-badge kpi-badge-amber">spend/mo × lifetime</span></div>
        </div>""", unsafe_allow_html=True)

    st.markdown("<div style='margin-top:20px;'></div>", unsafe_allow_html=True)
    clv_chart1, clv_chart2 = st.columns([1, 1])

    # Chart 1: Scatter lifetime vs total spent, warna per segment
    with clv_chart1:
        fig_scatter = px.scatter(
            df_f,
            x='customer_lifetime_months',
            y='total_spent',
            color='segment',
            size='total_rentals',
            hover_data=['customer_name', 'city', 'total_rentals'],
            color_discrete_map={
                'Champions': '#10b981',
                'At Risk':   '#ef4444',
                'Regular':   '#3b82f6',
            },
            labels={
                'customer_lifetime_months': 'Customer Lifetime (months)',
                'total_spent': 'Total Spending ($)',
                'segment': 'Segment'
            },
            opacity=0.7
        )
        # Tambah garis tren linear sederhana
        fig_scatter.update_traces(marker=dict(line=dict(width=0.5, color='#334155')))
        layout_sc = clean_layout()
        layout_sc['legend'] = dict(
            orientation="h", yanchor="bottom", y=-0.3,
            xanchor="center", x=0.5,
            font=dict(color="#e2e8f0"), bgcolor="#1e293b"
        )
        fig_scatter.update_layout(**layout_sc)

        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        st.markdown('<p class="sub-header">Lifetime vs Total Spending</p>', unsafe_allow_html=True)
        st.caption("Semakin lama aktif, semakin besar pengeluaran? Ukuran titik = jumlah rental.")
        st.plotly_chart(fig_scatter, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # Chart 2: Distribusi lifetime per segment (violin/box)
    with clv_chart2:
        fig_violin = px.violin(
            df_f,
            x='segment', y='customer_lifetime_months',
            color='segment',
            box=True,
            points='outliers',
            color_discrete_map={
                'Champions': '#10b981',
                'At Risk':   '#ef4444',
                'Regular':   '#3b82f6',
            },
            labels={
                'customer_lifetime_months': 'Customer Lifetime (months)',
                'segment': 'Segment'
            }
        )
        layout_vio = clean_layout()
        layout_vio['showlegend'] = False
        layout_vio['xaxis'] = dict(showgrid=False, zeroline=False, color="#94a3b8")
        fig_violin.update_layout(**layout_vio, yaxis_title="Lifetime (months)")

        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        st.markdown('<p class="sub-header">Distribusi Lifetime per Segment</p>', unsafe_allow_html=True)
        st.caption("Seberapa lama pelanggan tiap segment bertahan aktif? Lebar violin = densitas data.")
        st.plotly_chart(fig_violin, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # Insight box CLV
    champ_clv = df_f[df_f['segment'] == 'Champions']['total_spent'].mean() if len(df_f[df_f['segment'] == 'Champions']) > 0 else 0
    regular_clv = df_f[df_f['segment'] == 'Regular']['total_spent'].mean() if len(df_f[df_f['segment'] == 'Regular']) > 0 else 0
    atrisk_lifetime = df_f[df_f['segment'] == 'At Risk']['customer_lifetime_months'].mean() if len(df_f[df_f['segment'] == 'At Risk']) > 0 else 0

    st.markdown(f"""
    <div class="insight-box">
        <b>📌 Key CLV Insights:</b><br>
        • Rata-rata pelanggan aktif selama <b>{avg_lifetime_months:.1f} bulan</b> dengan pengeluaran <b>${avg_spend_per_month:.2f}/bulan</b> — estimasi CLV rata-rata <b>${estimated_clv:.0f}</b>.<br>
        • Champions menghabiskan rata-rata <b>${champ_clv:.0f}</b> per orang — jauh di atas Regular (<b>${regular_clv:.0f}</b>). Kehilangan satu Champion setara kehilangan {round(champ_clv/max(regular_clv,1), 1)}x Regular customer.<br>
        • Pelanggan At Risk sudah aktif rata-rata <b>{atrisk_lifetime:.1f} bulan</b> sebelum berhenti — mereka bukan pelanggan baru, mereka yang pernah loyal. Win-back campaign layak diprioritaskan.
    </div>
    """, unsafe_allow_html=True)

    # ─── OPERATIONAL INSIGHT ─────────────────────────────────
    st.markdown('<hr>', unsafe_allow_html=True)
    st.markdown('## ⚙️ Operational Insight')
    st.markdown('Gunakan bagian ini untuk aksi penyelamatan pelanggan berisiko tinggi.')

    at_risk_customers = df_f[df_f['segment'] == 'At Risk']
    if not at_risk_customers.empty:
        at_risk_whales = at_risk_customers.nlargest(5, 'total_spent')
        st.error("🚨 **TODAY'S TOP PRIORITY: High-Value Customers on the Brink of Leaving!**")
        cols = st.columns(len(at_risk_whales))
        for i, (idx, row) in enumerate(at_risk_whales.iterrows()):
            with cols[i]:
                st.metric(label=row['customer_name'],
                          value=f"${row['total_spent']:.0f}",
                          delta="AT RISK", delta_color="inverse")
                st.caption(f"Last rental: {row['days_since_last_rental']} days ago")
    else:
        st.success("✅ Tidak ada high-value customer yang saat ini berstatus 'At Risk'.")

    # ─── CUSTOMER DIRECTORY ───────────────────────────────────
    st.markdown('<h2 class="section-header">🗂️ Customer Directory</h2>', unsafe_allow_html=True)
    st.markdown('<p class="section-desc">Cari, ranking, dan drill down ke profil individual pelanggan.</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">📋 Full Customer Directory</p>', unsafe_allow_html=True)

    col_search, col_seg, col_sort = st.columns([2, 1.5, 1.5])
    with col_search:
        search_query = st.text_input("🔍 Search by Name or Email:", placeholder="e.g. John, john@email.com ...", key="cust_search")
    with col_seg:
        seg_options  = sorted(df_f['segment'].unique().tolist())
        selected_seg = st.multiselect("Filter Segment:", options=seg_options, default=seg_options, key="cust_seg")
    with col_sort:
        sort_by = st.selectbox("Sort By:", options=["Total Spent ↓","Total Rentals ↓","Days Since Last Rental ↑","Name A–Z"], key="cust_sort")

    display_df = df_f[df_f['segment'].isin(selected_seg)].copy()
    if search_query:
        mask = (
            display_df['customer_name'].str.contains(search_query, case=False, na=False) |
            display_df['email'].str.contains(search_query, case=False, na=False)
        )
        display_df = display_df[mask]

    sort_map = {
        "Total Spent ↓":            ('total_spent', False),
        "Total Rentals ↓":          ('total_rentals', False),
        "Days Since Last Rental ↑": ('days_since_last_rental', True),
        "Name A–Z":                 ('customer_name', True),
    }
    sort_col, sort_asc = sort_map[sort_by]
    display_df = display_df.sort_values(sort_col, ascending=sort_asc)

    st.caption(f"Showing **{len(display_df)}** customers")
    st.html(render_html_table(display_df))

    st.markdown("#### 📥 Download List")
    dl_col1, dl_col2 = st.columns([1, 1])
    with dl_col1:
        seg_dl = st.selectbox("Select segment to download:", options=['All'] + seg_options, key="dl_seg")
    with dl_col2:
        dl_df = display_df if seg_dl == 'All' else display_df[display_df['segment'] == seg_dl]
        st.download_button(
            label=f"⬇️ Download {seg_dl}",
            data=dl_df.to_csv(index=False).encode('utf-8'),
            file_name=f'customers_{seg_dl.lower().replace(" ", "_")}.csv',
            mime='text/csv',
            use_container_width=True,
        )

    st.markdown('<br>', unsafe_allow_html=True)

    # ─── CUSTOMER DRILL DOWN ──────────────────────────────────
    st.markdown('<p class="sub-header">🔎 Customer Drill Down</p>', unsafe_allow_html=True)
    st.caption("Pilih pelanggan untuk melihat profil lengkap, riwayat rental, dan preferensi genre.")

    customer_options = (
        df_f.sort_values('customer_name')
        .apply(lambda r: f"{r['customer_name']} — {r['city']}", axis=1).tolist()
    )
    selected_label = st.selectbox("Choose Customer:",
                                  options=["(Select a customer)"] + customer_options,
                                  key="drill_select")

    if selected_label != "(Select a customer)":
        sel_name, sel_city = selected_label.split(" — ", 1)
        cust_row = df_f[(df_f['customer_name'] == sel_name) & (df_f['city'] == sel_city)].iloc[0]
        cid      = int(cust_row['customer_id'])
        df_hist  = load_rental_history((cid,))

        seg_color_map = {'Champions': '#10b981', 'At Risk': '#ef4444', 'Regular': '#3b82f6'}
        seg_color     = seg_color_map.get(cust_row['segment'], '#3b82f6')
        status_label  = '🟢 Active' if cust_row['days_since_last_rental'] <= 100 else '🔴 Inactive'

        st.markdown(f"""
        <div style="background:linear-gradient(135deg,#1e293b,#0f172a); border:1px solid #334155;
                    border-left:5px solid {seg_color}; border-radius:14px; padding:24px 28px; margin:12px 0 20px 0;">
            <div style="display:flex; justify-content:space-between; align-items:flex-start; flex-wrap:wrap; gap:12px;">
                <div>
                    <div style="color:#94a3b8; font-size:11px; font-weight:700; letter-spacing:0.08em; text-transform:uppercase; margin-bottom:4px;">Customer Profile</div>
                    <div style="color:#f1f5f9; font-size:26px; font-weight:800; margin-bottom:4px;">{cust_row['customer_name']}</div>
                    <div style="color:#64748b; font-size:13px;">{cust_row['email']}</div>
                    <div style="color:#64748b; font-size:13px; margin-top:2px;">📍 {cust_row['city']}</div>
                </div>
                <div style="display:flex; flex-direction:column; gap:8px; align-items:flex-end;">
                    <span style="background:{seg_color}22; color:{seg_color}; padding:4px 14px; border-radius:99px; font-weight:700; font-size:13px;">{cust_row['segment']}</span>
                    <span style="background:#1e293b; color:#94a3b8; padding:4px 14px; border-radius:99px; font-size:12px; border:1px solid #334155;">{status_label}</span>
                </div>
            </div>
            <hr style="border-color:#334155; margin:16px 0;">
            <div style="display:flex; gap:32px; flex-wrap:wrap;">
                <div>
                    <div style="color:#64748b; font-size:11px; text-transform:uppercase; letter-spacing:0.06em;">Lifetime Spending</div>
                    <div style="color:#f1f5f9; font-size:22px; font-weight:800;">${cust_row['total_spent']:,.2f}</div>
                </div>
                <div>
                    <div style="color:#64748b; font-size:11px; text-transform:uppercase; letter-spacing:0.06em;">Total Rentals</div>
                    <div style="color:#f1f5f9; font-size:22px; font-weight:800;">{int(cust_row['total_rentals'])}</div>
                </div>
                <div>
                    <div style="color:#64748b; font-size:11px; text-transform:uppercase; letter-spacing:0.06em;">Avg per Rental</div>
                    <div style="color:#f1f5f9; font-size:22px; font-weight:800;">${cust_row['total_spent']/max(cust_row['total_rentals'],1):.2f}</div>
                </div>
                <div>
                    <div style="color:#64748b; font-size:11px; text-transform:uppercase; letter-spacing:0.06em;">Active Lifetime</div>
                    <div style="color:#f1f5f9; font-size:22px; font-weight:800;">{cust_row['customer_lifetime_months']:.1f} mo</div>
                </div>
                <div>
                    <div style="color:#64748b; font-size:11px; text-transform:uppercase; letter-spacing:0.06em;">Last Rental</div>
                    <div style="color:#f1f5f9; font-size:22px; font-weight:800;">{int(cust_row['days_since_last_rental'])} days ago</div>
                </div>
                <div>
                    <div style="color:#64748b; font-size:11px; text-transform:uppercase; letter-spacing:0.06em;">Member Since</div>
                    <div style="color:#f1f5f9; font-size:22px; font-weight:800;">{pd.to_datetime(cust_row['acquisition_date']).strftime('%b %Y')}</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        ch1, ch2 = st.columns([3, 2])

        with ch1:
            if not df_hist.empty:
                df_timeline = (
                    df_hist.set_index('rental_date').resample('ME').size()
                    .reset_index(name='rentals')
                )
                df_timeline['rental_date'] = df_timeline['rental_date'].dt.strftime('%b %Y')
                fig_tl = px.bar(df_timeline, x='rental_date', y='rentals',
                                color_discrete_sequence=[seg_color],
                                labels={'rental_date': 'Month', 'rentals': 'Rentals'})
                fig_tl.update_layout(**clean_layout(), xaxis_tickangle=-30)
                st.markdown('<div class="chart-card">', unsafe_allow_html=True)
                st.markdown('<p class="sub-header">📅 Monthly Rental Activity</p>', unsafe_allow_html=True)
                st.caption("How often does this customer rent over time?")
                st.plotly_chart(fig_tl, use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)
            else:
                st.info("No rental history found for this customer.")

        with ch2:
            if not df_hist.empty:
                genre_counts = (
                    df_hist.groupby('genre').size()
                    .reset_index(name='count').sort_values('count', ascending=False)
                )
                total_rc = genre_counts['count'].sum()
                genre_counts['pct'] = genre_counts['count'] / total_rc * 100
                main_genres  = genre_counts[genre_counts['pct'] >= 5].copy()
                other_genres = genre_counts[genre_counts['pct'] < 5]
                if len(other_genres) > 0:
                    others_row = pd.DataFrame([{
                        'genre': f'Others ({len(other_genres)} genres)',
                        'count': other_genres['count'].sum(),
                        'pct':   other_genres['pct'].sum()
                    }])
                    genre_counts_clean = pd.concat(
                        [main_genres[['genre','count','pct']], others_row], ignore_index=True)
                else:
                    genre_counts_clean = main_genres[['genre','count','pct']]

                fig_genre = px.pie(genre_counts_clean, names='genre', values='count',
                                   hole=0.55, color_discrete_sequence=PALETTE)
                layout_g = clean_layout()
                layout_g['legend'] = dict(orientation="v", font=dict(size=11, color="#e2e8f0"), bgcolor="#1e293b")
                layout_g['margin'] = dict(t=10, b=30, l=10, r=10)
                fig_genre.update_layout(**layout_g)
                fig_genre.update_traces(
                    textinfo='percent+label',
                    hovertemplate='<b>%{label}</b><br>%{value} rentals (%{percent})<extra></extra>',
                    textfont=dict(size=10)
                )
                st.markdown('<div class="chart-card">', unsafe_allow_html=True)
                st.markdown('<p class="sub-header">🎬 Favourite Genres</p>', unsafe_allow_html=True)
                st.caption("Distribusi genre dari seluruh rental. Genre <5% digabung ke 'Others'.")
                st.plotly_chart(fig_genre, use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)

    # ─── STRATEGIC ACTION PLAN ────────────────────────────────
    avg_rental_rate = df_f['total_rentals'].mean() / max(
        (df_f['last_rental_date'].max() - df_f['first_rental_date'].min()).days / 30, 1
    )

    st.markdown('<h2 class="section-header">💡 Strategic Action Plan</h2>', unsafe_allow_html=True)
    st.markdown('<p class="section-desc">Rekomendasi otomatis berbasis data kondisi pelanggan saat ini.</p>', unsafe_allow_html=True)

    champions_count = len(df_f[df_f['segment'] == 'Champions'])
    champions_pct   = (champions_count / t_cust * 100) if t_cust > 0 else 0
    potential_loss  = df_f[df_f['segment'] == 'At Risk']['total_spent'].sum()

    if champions_count == 0:
        champ_title = "💎 Build Your Champions"
        champ_body  = "No Champions detected. Focus on converting top Regular customers through exclusive early-access promos to push them over the threshold."
    elif champions_pct < 10:
        champ_title = "💎 Protect Your Champions"
        champ_body  = f"Only <b>{champions_count} Champions ({champions_pct:.1f}%)</b> detected — a thin base. Offer VIP early access to new titles and a dedicated loyalty tier."
    else:
        champ_title = "💎 Champions Strategy"
        champ_body  = f"<b>{champions_count} Champions ({champions_pct:.1f}%)</b> driving top-line revenue. Reward with 2x Loyalty Points and exclusive perks."

    if risk_count == 0:
        risk_title = "✅ No Active Risk Detected"
        risk_body  = "All customers are currently active. Set alerts if any customer exceeds 90 days without a rental."
        risk_card  = "rec-card-blue"
    elif urgency_label == "🟡 Recoverable":
        risk_title = "⚠️ Win-back Window Open"
        risk_body  = f"<b>${potential_loss:,.0f}</b> at risk across <b>{risk_count} customers</b> — avg inactivity {avg_days_at_risk:.0f} days. Send 'We Miss You' promo with 20% off."
        risk_card  = "rec-card-red"
    elif urgency_label == "🔴 High Urgency":
        risk_title = "🔴 High Urgency: Act Now"
        risk_body  = f"<b>${potential_loss:,.0f}</b> exposure across <b>{risk_count} customers</b> averaging <b>{avg_days_at_risk:.0f} days</b> inactive. Escalate to direct outreach with time-limited 30% discount."
        risk_card  = "rec-card-red"
    else:
        risk_title = "💀 Near-Lost: Last Resort"
        risk_body  = f"<b>{risk_count} customers</b> averaging <b>{avg_days_at_risk:.0f} days</b> inactive. Deploy high-value 'Come Back' bundle targeting only top spenders."
        risk_card  = "rec-card-red"

    if avg_rental_rate < 1.5:
        up_title = "🚀 Activation Needed"
        up_body  = f"Avg rental rate only <b>{avg_rental_rate:.1f}x/month</b>. Introduce 'Rent 3 for 2' bundle to build engagement habits."
    elif avg_rental_rate < 3.0:
        up_title = "🚀 Upselling Strategy"
        up_body  = f"Rental rate <b>{avg_rental_rate:.1f}x/month</b> — moderate. Offer 'Rent 5 for Less' bundle to push frequency toward Champions territory."
    else:
        up_title = "🚀 Maximize High-Frequency Customers"
        up_body  = f"Strong avg rental rate of <b>{avg_rental_rate:.1f}x/month</b>. Shift focus to <i>spend per rental</i> — promote premium titles with small surcharge."

    rec1, rec2, rec3 = st.columns(3)
    with rec1:
        st.markdown(f"""<div class="rec-card-green">
            <h4 style="color:#34d399; margin-top:0;">{champ_title}</h4>
            <p style="color:#a7f3d0; font-size:14px;">{champ_body}</p>
        </div>""", unsafe_allow_html=True)
    with rec2:
        st.markdown(f"""<div class="{risk_card}">
            <h4 style="color:#f87171; margin-top:0;">{risk_title}</h4>
            <p style="color:#fecaca; font-size:14px;">{risk_body}</p>
        </div>""", unsafe_allow_html=True)
    with rec3:
        st.markdown(f"""<div class="rec-card-blue">
            <h4 style="color:#60a5fa; margin-top:0;">{up_title}</h4>
            <p style="color:#bfdbfe; font-size:14px;">{up_body}</p>
        </div>""", unsafe_allow_html=True)

# ─── FOOTER ──────────────────────────────────────────────────
st.markdown("""
    <div class="footer">
        Customer Profile Intelligence Dashboard &nbsp;·&nbsp; Analyst: <strong>Puspita Tri Rahayu</strong>
    </div>
    """, unsafe_allow_html=True)