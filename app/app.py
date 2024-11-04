from flask import Flask, render_template
import os
import psycopg2
import psycopg2.pool
import pandas as pd
import plotly.express as px
import plotly.io as pio

app = Flask(__name__)

# Database connection setup
DB_HOST =  "34.93.195.0"
DB_NAME =  "postgres"
DB_USER =  "postgres"
DB_PASS =  "Plotpointe!@3456"
DB_PORT =  "5432"

connection_pool = psycopg2.pool.SimpleConnectionPool(
    1, 200, host=DB_HOST, port=DB_PORT, database=DB_NAME, user=DB_USER, password=DB_PASS
)

def fetch_daily_deleted_comments():
    try:
        with connection_pool.getconn() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT DATE(c.posted_date) AS date, s.name AS sponsor_name, COUNT(c.comment) AS comment_count
                    FROM comments c
                    JOIN sponsor s ON c.sponsor_id = s.id
                    WHERE c.status = 'Deleted'
                    GROUP BY DATE(c.posted_date), s.name
                    ORDER BY DATE(c.posted_date)
                """)
                data = cur.fetchall()
                return pd.DataFrame(data, columns=["date", "sponsor_name", "comment_count"])
    except Exception as e:
        print(f"Error fetching data: {e}")
        return pd.DataFrame()

def fetch_comments_per_1k_views():
    try:
        with connection_pool.getconn() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT s.name AS sponsor_name,
                           SUM(CASE WHEN c.status = 'Deleted' THEN 1 ELSE 0 END) AS deleted_comments,
                           SUM(st.views_total) AS total_views
                    FROM comments c
                    JOIN sponsor s ON c.sponsor_id = s.id
                    JOIN video v ON s.id = v.sponsor_id
                    JOIN statistics st ON v.id = st.video_id
                    GROUP BY s.name
                    HAVING SUM(st.views_total) > 0
                """)
                data = cur.fetchall()
                df = pd.DataFrame(data, columns=["sponsor_name", "deleted_comments", "total_views"])
                df["comments_per_1k_views"] = (df["deleted_comments"] / df["total_views"]) * 1000
                return df
    except Exception as e:
        print(f"Error fetching data: {e}")
        return pd.DataFrame()

@app.route('/')
def index():
    # Chart 1: Daily Deleted Comment Counts by Sponsor (Bar Chart)
    df1 = fetch_daily_deleted_comments()
    fig1 = px.bar(
        df1, x="date", y="comment_count", color="sponsor_name",
        title="Daily Deleted Comment Counts by Sponsor",
        labels={"date": "Date", "comment_count": "Comment Count", "sponsor_name": "Sponsor Name"},
        barmode="stack"
    )
    fig1.update_layout(xaxis_title="Date", yaxis_title="Deleted Comment Count", hovermode="x unified")
    chart1 = pio.to_html(fig1, full_html=False)

    # Chart 2: Daily Deleted Comment Counts by Sponsor (Line Chart)
    fig2 = px.line(df1, x="date", y="comment_count", color="sponsor_name", title="Daily Deleted Comment Counts by Sponsor")
    fig2.update_layout(xaxis_title="Date", yaxis_title="Comment Count", hovermode="x unified")
    chart2 = pio.to_html(fig2, full_html=False)

    # Chart 3: Deleted Comments per 1,000 Views by Sponsor
    df3 = fetch_comments_per_1k_views()
    fig3 = px.bar(
        df3, x="sponsor_name", y="comments_per_1k_views",
        title="Deleted Comments per 1,000 Views by Sponsor",
        labels={"comments_per_1k_views": "Comments per 1,000 Views", "sponsor_name": "Sponsor Name"}
    )
    fig3.update_layout(xaxis_title="Sponsor Name", yaxis_title="Deleted Comments per 1,000 Views", hovermode="x")
    chart3 = pio.to_html(fig3, full_html=False)

    return render_template("index.html", chart1=chart1, chart2=chart2, chart3=chart3)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)


