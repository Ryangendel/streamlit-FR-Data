# import streamlit as st
# import pandas as pd
# import os
# import matplotlib.pyplot as plt
# from datetime import datetime

# df1 = pd.read_csv("data/wp_statistics_historical.csv")
# df2 = pd.read_csv("data/wp_statistics_pages.csv")
# df3 = pd.read_csv("data/wp_statistics_visitor.csv")
# df4 = pd.read_csv("data/wp_statistics_visitor_relationships.csv")

# # Set path to your CSV folder
# DATA_FOLDER = 'data'

# st.title("Fortitude Ranch & Collapse Survivor Data")

# df1['uri'] = df1['uri'].str.replace(r'\?fbclid=.*', '', regex=True)
# df1 = df1[~df1['uri'].str.contains('wordfence_lh|wp-admin|xmlrpc', na=False)]

# # Group by `uri` and count how many times each was visited
# # Count how many times each URI appears
# uri_counts = df1['uri'].value_counts().reset_index()
# uri_counts.columns = ['uri', 'visit_count']

# # Display table
# st.subheader("🔢 URI Visit Counts (Cleaned)")
# st.dataframe(uri_counts)

# # Display bar chart of top visited URIs
# st.subheader("📊 Top 20 Visited URIs")
# fig, ax = plt.subplots(figsize=(10, 6))
# uri_counts.head(20).plot(kind='barh', x='uri', y='visit_count', ax=ax)
# ax.invert_yaxis()
# ax.set_xlabel("Visits")
# ax.set_ylabel("URI")
# ax.set_title("Most Visited URIs (Cleaned)")
# st.pyplot(fig)

# # ------------------------------------

# st.title("📊 Weekly Visits Grouped by URI")

# # Load df2
# # Parse date column
# df2['date'] = pd.to_datetime(df2['date'], errors='coerce')
# df2 = df2.dropna(subset=['date'])

# # Create a week column (start of each week)
# df2['week'] = df2['date'].dt.to_period('W').apply(lambda r: r.start_time)

# # Group by week and URI, sum counts
# weekly_uri_counts = df2.groupby(['week', 'uri'])['count'].sum().reset_index()

# # Pivot for plotting
# pivot_df = weekly_uri_counts.pivot(index='week', columns='uri', values='count').fillna(0)

# # Optional: show only top N URIs to avoid overcrowding
# top_n = 10
# top_uris = pivot_df.sum().sort_values(ascending=False).head(top_n).index
# pivot_df = pivot_df[top_uris]

# # Format week labels to hide time (00:00:00)
# pivot_df.index = pivot_df.index.strftime('%Y-%m-%d')

# # Plot stacked bar chart
# st.subheader("🧱 Weekly Visits per URI (Stacked Bar)")
# fig, ax = plt.subplots(figsize=(16, 8))  # <-- Increased width and height
# pivot_df.plot(kind='bar', stacked=True, ax=ax)
# ax.set_ylabel("Total Visits", fontsize=14)
# ax.set_xlabel("Week", fontsize=14)
# ax.set_title("Weekly Visits by URI", fontsize=18)
# plt.xticks(rotation=45, ha='right', fontsize=12)
# plt.yticks(fontsize=12)
# st.pyplot(fig)

# # -----------------------------------
# st.title("📊 User Interaction Analysis Dashboard")

# df3['first_view'] = pd.to_datetime(df3['first_view'], errors='coerce')
# df3['last_view'] = pd.to_datetime(df3['last_view'], errors='coerce')

# # ---------- 1. Device Types ----------
# st.header("1️⃣ Device Types Used")

# # Normalize device labels
# df3['device_normalized'] = df3['device'].replace({
#     'mobile:smart': 'Smartphone',
#     'smartphone': 'Smartphone'
# })

# device_counts = df3['device_normalized'].value_counts()
# fig1, ax1 = plt.subplots(figsize=(10, 6))
# device_counts.plot(kind='bar', ax=ax1)
# ax1.set_ylabel("Number of Users")
# ax1.set_title("Devices Used by Visitors")
# st.pyplot(fig1)

# # ---------- 2. Platform Types ----------
# st.header("2️⃣ Platforms Used")
# platform_counts = df3['platform'].value_counts()
# fig2, ax2 = plt.subplots(figsize=(10, 6))
# platform_counts.plot(kind='bar', ax=ax2)
# ax2.set_ylabel("Number of Users")
# ax2.set_title("Platforms Used by Visitors")
# st.pyplot(fig2)

# # ---------- 3. North American Regions ----------
# st.header("3️⃣ Visitors by Region (North America Only)")
# na_df = df3[df3['continent'] == 'North America']
# region_counts = na_df['region'].value_counts()
# region_counts = region_counts[region_counts > 30]  # Filter out regions < 30

# fig3, ax3 = plt.subplots(figsize=(12, 6))
# region_counts.plot(kind='bar', ax=ax3)
# ax3.set_ylabel("Visitors")
# ax3.set_title("North American Visitors by Region (30+ only)")
# st.pyplot(fig3)

# # ---------- 4. Time Spent on Site ----------
# st.header("4️⃣ Time Spent on Site (Minutes)")

# # Calculate session duration in minutes
# df3['duration_minutes'] = (df3['last_view'] - df3['first_view']).dt.total_seconds() / 60
# df3 = df3[df3['duration_minutes'].notna() & (df3['duration_minutes'] > 0)]

# # Create fixed-width bins (20 minutes)
# bin_width = 20
# max_duration = int(df3['duration_minutes'].max())
# bins = range(0, max_duration + bin_width, bin_width)

# fig4, ax4 = plt.subplots(figsize=(12, 6))
# ax4.hist(df3['duration_minutes'], bins=bins, edgecolor='black')
# ax4.set_xlabel("Session Duration (minutes)")
# ax4.set_ylabel("Number of Users")
# ax4.set_title("Session Duration Distribution (20-Minute Increments)")
# ax4.set_xticks(bins)
# plt.xticks(rotation=45)
# st.pyplot(fig4)

# # ---------- 5. Same vs Different Page ----------
# st.header("5️⃣ Same Page vs Different Page Sessions")
# # Compare first and last page
# same_page = (df3['first_page'] == df3['last_page'])
# same_count = same_page.sum()
# different_count = (~same_page).sum()
# labels = ['Same Page', 'Different Page']
# values = [same_count, different_count]

# fig5, ax5 = plt.subplots()
# ax5.pie(values, labels=labels, autopct='%1.1f%%', startangle=140)
# ax5.set_title("Session Navigation Behavior")
# st.pyplot(fig5)

# st.header("6️⃣ Most Popular Visit Times")

# # Drop NaNs just in case
# time_df = df3.dropna(subset=['first_view']).copy()

# # Extract day of week and hour from first_view
# time_df['day_of_week'] = time_df['first_view'].dt.day_name()
# time_df['hour'] = time_df['first_view'].dt.hour

# # Count visits per day
# day_counts = time_df['day_of_week'].value_counts().reindex(
#     ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
# )

# fig6a, ax6a = plt.subplots(figsize=(10, 4))
# day_counts.plot(kind='bar', ax=ax6a)
# ax6a.set_title("Visits by Day of the Week")
# ax6a.set_ylabel("Number of Visits")
# st.pyplot(fig6a)

# # Count visits per hour
# hour_counts = time_df['hour'].value_counts().sort_index()

# fig6b, ax6b = plt.subplots(figsize=(12, 4))
# hour_counts.plot(kind='bar', ax=ax6b)
# ax6b.set_title("Visits by Hour of the Day")
# ax6b.set_xlabel("Hour (24-hour format)")
# ax6b.set_ylabel("Number of Visits")
# st.pyplot(fig6b)


# st.header("8️⃣ Top 10 Days by Visit Volume")

# # Make sure 'date_only' exists
# df3['date_only'] = df3['first_view'].dt.date

# # Count visits per day and get top 10
# daily_visits = df3['date_only'].value_counts().sort_values(ascending=False).head(10)

# # Sort for clean chart (descending order)
# daily_visits = daily_visits.sort_values()

# # Display table
# st.write("📅 **Top 10 Visit Days** (based on `first_view`):")
# st.dataframe(daily_visits.rename("Visit Count"))

# # Horizontal bar chart
# fig_top10, ax_top10 = plt.subplots(figsize=(10, 6))
# daily_visits.plot(kind='barh', ax=ax_top10, color='skyblue', edgecolor='black')
# ax_top10.set_xlabel("Number of Visits")
# ax_top10.set_ylabel("Date")
# ax_top10.set_title("Top 10 Days by Visit Count")
# st.pyplot(fig_top10)



# # ---------- 9. Bounce Rate by Device and Platform ----------
# st.header("9️⃣ Bounce Rate by Device & Platform")

# # Create bounce column
# df3['bounced'] = df3['first_page'] == df3['last_page']

# # Group by device
# bounce_by_device = df3.groupby('device')['bounced'].mean().sort_values(ascending=False)
# st.subheader("📱 Bounce Rate by Device")
# st.bar_chart(bounce_by_device)

# # Group by platform
# bounce_by_platform = df3.groupby('platform')['bounced'].mean().sort_values(ascending=False)
# st.subheader("💻 Bounce Rate by Platform")
# st.bar_chart(bounce_by_platform)

# # ---------- 10. Average Session Duration by Region and Platform ----------
# st.header("🔟 Avg Session Duration by Region & Platform")

# # Only use data from North America
# na_df = df3[df3['continent'] == 'North America']

# # Group by region (North America only)
# avg_duration_region = na_df.groupby('region')['duration_minutes'].mean().dropna().sort_values(ascending=False)
# st.subheader("🌍 Avg Duration by Region (North America Only)")
# if not avg_duration_region.empty:
#     st.bar_chart(avg_duration_region)
# else:
#     st.info("No region data available for North America.")

# # Group by platform (global)
# avg_duration_platform = df3.groupby('platform')['duration_minutes'].mean().dropna().sort_values(ascending=False)
# st.subheader("💻 Avg Duration by Platform")
# if not avg_duration_platform.empty:
#     st.bar_chart(avg_duration_platform)
# else:
#     st.info("No platform data available.")

# # ---------- 11. Most Common Exit Pages ----------
# st.header("1️⃣1️⃣ Top Exit Pages (last_page)")

# exit_pages = df3['last_page'].value_counts().head(10)
# fig_exit, ax_exit = plt.subplots(figsize=(10, 5))
# exit_pages.plot(kind='barh', ax=ax_exit, color='salmon')
# ax_exit.invert_yaxis()
# ax_exit.set_xlabel("Number of Sessions")
# ax_exit.set_title("Top 10 Most Common Exit Pages")
# st.pyplot(fig_exit)

# # ---------- 12. Returning vs New Users ----------
# st.header("1️⃣2️⃣ Returning vs New Users")

# # Drop rows with null or empty user_id
# user_ids = df3['user_id'].dropna()
# user_ids = user_ids[user_ids.astype(str).str.strip() != ""]

# if not user_ids.empty:
#     user_counts = user_ids.value_counts()
#     returning_users = (user_counts > 1).sum()
#     new_users = (user_counts == 1).sum()

#     fig_users, ax_users = plt.subplots()
#     ax_users.pie(
#         [new_users, returning_users],
#         labels=['New Users', 'Returning Users'],
#         autopct='%1.1f%%',
#         startangle=140
#     )
#     ax_users.set_title("User Loyalty: New vs Returning")
#     st.pyplot(fig_users)
# else:
#     st.info("No user ID data available to determine new vs returning users.")
# # ---------- 13. Weekly Visit Trends ----------
# st.header("1️⃣3️⃣ Weekly Visit Trends")

# df3['week'] = df3['first_view'].dt.to_period('W').apply(lambda r: r.start_time)
# weekly_visits = df3['week'].value_counts().sort_index()

# fig_weekly, ax_weekly = plt.subplots(figsize=(12, 6))
# weekly_visits.plot(kind='line', marker='o', ax=ax_weekly)
# ax_weekly.set_ylabel("Visits")
# ax_weekly.set_xlabel("Week")
# ax_weekly.set_title("Visits Over Time (Weekly)")
# plt.xticks(rotation=45)
# st.pyplot(fig_weekly)

# # ---------- 14. First Page Popularity ----------
# st.header("1️⃣4️⃣ Most Common First Pages")

# first_page_counts = df3['first_page'].value_counts().head(10)
# fig_first, ax_first = plt.subplots(figsize=(10, 5))
# first_page_counts.plot(kind='bar', ax=ax_first, color='mediumseagreen')
# ax_first.set_ylabel("Visitors")
# ax_first.set_title("Top 10 First Pages")
# st.pyplot(fig_first)


# ==========================0000000000000000000000000000
import streamlit as st
import pandas as pd
import os
import matplotlib.pyplot as plt
from datetime import datetime
import plotly.express as px

# Load data
df1 = pd.read_csv("data/wp_statistics_historical.csv")
df2 = pd.read_csv("data/wp_statistics_pages.csv")
df3 = pd.read_csv("data/wp_statistics_visitor.csv")
df4 = pd.read_csv("data/wp_statistics_visitor_relationships.csv")

# Preprocessing
df1['uri'] = df1['uri'].str.replace(r'\?fbclid=.*', '', regex=True)
df1 = df1[~df1['uri'].str.contains('wordfence_lh|wp-admin|xmlrpc', na=False)]

df2['date'] = pd.to_datetime(df2['date'], errors='coerce')
df2 = df2.dropna(subset=['date'])
df2['week'] = df2['date'].dt.to_period('W').apply(lambda r: r.start_time)

df3['first_view'] = pd.to_datetime(df3['first_view'], errors='coerce')
df3['last_view'] = pd.to_datetime(df3['last_view'], errors='coerce')
df3['duration_minutes'] = (df3['last_view'] - df3['first_view']).dt.total_seconds() / 60
df3 = df3[df3['duration_minutes'].notna() & (df3['duration_minutes'] > 0)]
df3['week'] = df3['first_view'].dt.to_period('W').apply(lambda r: r.start_time)
df3['device_normalized'] = df3['device'].replace({'mobile:smart': 'Smartphone', 'smartphone': 'Smartphone'})

# Sidebar Navigation
st.sidebar.title("📊 Dashboard Navigation")
page = st.sidebar.radio("Choose a page:", ["Fortitude Ranch Overview", "Collapse Survivor Overview"])

# ---------------------------- PAGE 1 ----------------------------
if page == "Fortitude Ranch Overview":
    st.title("🌐 Traffic Overview")

    # Convert to datetime
    df3['first_view'] = pd.to_datetime(df3['first_view'])

    # Filter for the last 14 days
    last_14_days = pd.Timestamp.now() - pd.Timedelta(days=14)
    df_recent = df3[df3['first_view'] >= last_14_days].copy()

    # Extract date only
    df_recent['date'] = df_recent['first_view'].dt.date

    # Group by date and sum hits
    daily_visits = df_recent.groupby('date')['hits'].sum().reset_index()

    # Plot
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(daily_visits['date'], daily_visits['hits'], marker='o')
    ax.set_title('Total Page Views (Last 14 Days (DATA WAS EXTRACTED MIDDAY))', fontsize=14)
    ax.set_xlabel('Date')
    ax.set_ylabel('Total Page Views')
    ax.grid(True)

    # Show in Streamlit
    st.pyplot(fig)



    # st.subheader("🔢 URI Visit Counts (Cleaned)")
    uri_counts = df1['uri'].value_counts().reset_index()
    uri_counts.columns = ['uri', 'visit_count']
    # st.dataframe(uri_counts)

    st.subheader("📊 Top 20 Visited Pages on FR.com")
    fig, ax = plt.subplots(figsize=(10, 6))
    uri_counts.head(20).plot(kind='barh', x='uri', y='visit_count', ax=ax)
    ax.invert_yaxis()
    ax.set_xlabel("Visits")
    ax.set_title("Most Visited URIs")
    st.pyplot(fig)

    st.subheader("🧱 Weekly Visits per URI")
    weekly_uri_counts = df2.groupby(['week', 'uri'])['count'].sum().reset_index()
    pivot_df = weekly_uri_counts.pivot(index='week', columns='uri', values='count').fillna(0)
    top_uris = pivot_df.sum().sort_values(ascending=False).head(10).index
    pivot_df = pivot_df[top_uris]
    pivot_df.index = pivot_df.index.strftime('%Y-%m-%d')

    fig_weekly, ax_weekly = plt.subplots(figsize=(16, 8))
    pivot_df.plot(kind='bar', stacked=True, ax=ax_weekly)
    ax_weekly.set_ylabel("Total Visits")
    ax_weekly.set_xlabel("Week")
    ax_weekly.set_title("Weekly Visits by URI")
    st.pyplot(fig_weekly)

    st.subheader("📅 Most Popular Site Visit Days")
    time_df = df3.dropna(subset=['first_view']).copy()
    time_df['day_of_week'] = time_df['first_view'].dt.day_name()
    time_df['hour'] = time_df['first_view'].dt.hour

    day_counts = time_df['day_of_week'].value_counts().reindex(
        ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    )
    fig_day, ax_day = plt.subplots(figsize=(10, 4))
    day_counts.plot(kind='bar', ax=ax_day)
    ax_day.set_title("Visits by Day of the Week")
    st.pyplot(fig_day)

    hour_counts = time_df['hour'].value_counts().sort_index()
    fig_hour, ax_hour = plt.subplots(figsize=(12, 4))
    hour_counts.plot(kind='bar', ax=ax_hour)
    ax_hour.set_title("Visits by Hour of the Day")
    st.pyplot(fig_hour)

    st.subheader("📈 Top 10 Days by Visit Volume")
    df3['date_only'] = df3['first_view'].dt.date
    daily_visits = df3['date_only'].value_counts().sort_values(ascending=False).head(10).sort_values()
    # st.dataframe(daily_visits.rename("Visit Count"))
    fig_top, ax_top = plt.subplots(figsize=(10, 6))
    daily_visits.plot(kind='barh', ax=ax_top, color='skyblue')
    ax_top.set_title("Top 10 Days by Visits")
    st.pyplot(fig_top)

    st.subheader("📆 Weekly Visit Trends")
    weekly_visits = df3['week'].value_counts().sort_index()
    fig_trend, ax_trend = plt.subplots(figsize=(12, 6))
    weekly_visits.plot(kind='line', marker='o', ax=ax_trend)
    ax_trend.set_title("Visits Over Time (Weekly)")
    st.pyplot(fig_trend)

    st.subheader("Device Types")
    device_counts = df3['device_normalized'].value_counts()
    fig1, ax1 = plt.subplots(figsize=(10, 6))
    device_counts.plot(kind='bar', ax=ax1)
    ax1.set_title("Devices Used by Visitors")
    st.pyplot(fig1)

    st.subheader("Operating Systems Used")
    platform_counts = df3['platform'].value_counts()
    fig2, ax2 = plt.subplots(figsize=(10, 6))
    platform_counts.plot(kind='bar', ax=ax2)
    ax2.set_title("Platforms Used by Visitors")
    st.pyplot(fig2)

    st.subheader("Top Visitors by State")
    na_df = df3[df3['continent'] == 'North America']
    region_counts = na_df['region'].value_counts()
    region_counts = region_counts[region_counts > 30]
    fig3, ax3 = plt.subplots(figsize=(12, 6))
    region_counts.plot(kind='bar', ax=ax3)
    ax3.set_title("Visitors by Region")
    st.pyplot(fig3)

    st.subheader("Time Spent on Site (20-Minute Bins)")
    bin_width = 20
    max_duration = int(df3['duration_minutes'].max()) + bin_width
    bins = range(0, max_duration, bin_width)
    fig4, ax4 = plt.subplots(figsize=(12, 6))
    ax4.hist(df3['duration_minutes'], bins=bins, edgecolor='black')
    ax4.set_title("Session Duration (Minutes)")
    ax4.set_xticks(bins)
    st.pyplot(fig4)

    st.subheader("Percent of Users Who Only Visited One Page")
    same_page = df3['first_page'] == df3['last_page']
    same_count = same_page.sum()
    different_count = (~same_page).sum()
    fig5, ax5 = plt.subplots()
    ax5.pie([same_count, different_count], labels=['Same Page', 'Different Page'],
            autopct='%1.1f%%', startangle=140)
    ax5.set_title("User Navigation Behavior")
    st.pyplot(fig5)

    st.subheader("Bounce Rate by Device (visited and left)")
    bounce_by_device = df3.groupby('device')['first_page'].apply(
        lambda x: (x == df3.loc[x.index, 'last_page']).mean()
    )
    st.bar_chart(bounce_by_device)

    st.subheader("Avg Session Duration by Region (NA Only)")
    avg_dur_region = na_df.groupby('region')['duration_minutes'].mean().dropna()
    st.bar_chart(avg_dur_region)

    st.subheader("Top Pages Users Leave On")
    exit_pages = df3['last_page'].value_counts().head(10)
    fig_exit, ax_exit = plt.subplots(figsize=(10, 5))
    exit_pages.plot(kind='barh', ax=ax_exit, color='salmon')
    ax_exit.invert_yaxis()
    ax_exit.set_title("Top Exit Pages")
    st.pyplot(fig_exit)


# ---------------------------- PAGE 2 ----------------------------

elif page == "Collapse Survivor Overview":
    st.title("Collapse Survivor Website Overview")

    df5 = pd.read_csv("data/cs/weekly_visits.csv")  # replace with your actual file

    df5['Date'] = pd.to_datetime(df5['Date'], errors='coerce')
    df5 = df5.dropna(subset=['Date', 'Views'])

    # Group by date in case of duplicates
    df5 = df5.groupby('Date')['Views'].sum().reset_index()

    # Sort by date
    df5 = df5.sort_values('Date')

    # Plot the bar graph
    st.subheader("📆 Views Over Time")
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.bar(df5['Date'], df5['Views'], color='skyblue', edgecolor='black')
    ax.set_title("Views by Date")
    ax.set_xlabel("Date")
    ax.set_ylabel("Views")
    plt.xticks(rotation=45)
    st.pyplot(fig)


    df_search = pd.read_csv("data/cs/search_engine.csv")  # Replace with your actual file
    df_search = df_search.rename(columns={"Search Engines": "source", "1713": "visitors"})

    # Drop any rows with missing values
    df_search = df_search.dropna(subset=["source", "visitors"])

    # Normalize source column to lowercase for easier matching
    df_search['source'] = df_search['source'].str.lower()

    # Define search engine categories
    source_map = {
        'google': 'Google',
        'msn': 'MSN',
        'duckduckgo.com': 'DuckDuckGo',
        'bing': 'Bing',
        'yahoo': 'Yahoo',
        'yandex': 'Yandex',
        'youtube.com': 'YouTube',
        'washingtonexaminer.com': 'Washington Examiner',
        "Facebook":"Facebook"
    }

    # Function to map sources to simplified names
    def categorize_source(source):
        for keyword, label in source_map.items():
            if keyword in source:
                return label
        return None  # Ignore anything not in the list

    # Apply categorization
    df_search['group'] = df_search['source'].apply(categorize_source)

    # Filter out None values
    df_search = df_search.dropna(subset=['group'])

    # Group and sum visitor counts
    grouped = df_search.groupby('group')['visitors'].sum().sort_values(ascending=False)

    # Plot
    st.subheader("🔍 Visitors by Search Engine / Referrer")
    fig, ax = plt.subplots(figsize=(10, 6))
    grouped.plot(kind='bar', ax=ax, color='steelblue', edgecolor='black')
    ax.set_ylabel("Number of Visitors")
    ax.set_title("Search Engine / Referrer Traffic")
    plt.xticks(rotation=45)
    st.pyplot(fig)


    df_location = pd.read_csv("data/cs/traffic_location.csv", header=None)  # Adjust the path as needed

    # Rename for clarity
    df_location.columns = ['Country', 'Traffic']

    # Filter out countries with less than 10 visits
    df_filtered = df_location[df_location['Traffic'] >= 10]

    # Pie chart
    st.subheader("🌍 Traffic Sources by Country (10+ only)")
    fig, ax = plt.subplots(figsize=(8, 8))
    ax.pie(df_filtered['Traffic'], labels=df_filtered['Country'], autopct='%1.1f%%', startangle=140)
    ax.set_title("Where Website Traffic Comes From")
    st.pyplot(fig)


    df_pages = pd.read_csv("data/cs/page_visits.csv")  # Make sure you have "url" and "Visits" columns
    # Drop missing values
    df_pages = df_pages.dropna(subset=['url', 'visits'])

    # Group by URL in case of duplicates
    df_pages = df_pages.groupby('url')['visits'].sum().reset_index()

    # Sort by number of visits
    df_pages = df_pages.sort_values(by='visits', ascending=False)

    # -------- Option 1: Horizontal Bar Chart --------
    st.subheader("📊 Top Subpages by Visit Count (Horizontal Bar)")

    top_n = st.slider("How many top URLs to display?", min_value=10, max_value=100, value=30)

    fig1, ax1 = plt.subplots(figsize=(12, max(6, int(top_n * 0.3))))
    df_pages.head(top_n).plot(
        kind='barh',
        x='url',
        y='visits',
        ax=ax1,
        color='teal',
        edgecolor='black'
    )
    ax1.invert_yaxis()
    ax1.set_title("Visits to Top Subpages")
    ax1.set_xlabel("Number of Visits")
    st.pyplot(fig1)

    # -------- Option 2: Treemap for Many Pages --------
    st.subheader("🧱 Full Subpage Visit Distribution (Treemap)")

    fig2 = px.treemap(
        df_pages,
        path=['url'],
        values='visits',
        title='Treemap of Visits to All Subpages',
        height=600
    )
    st.plotly_chart(fig2)

    st.markdown("## 👥 Total Visitors: **11,113**")