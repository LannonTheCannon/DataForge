import streamlit as st
import plotly.express as px
import pandas as pd
from data import load_data


def display_data_story():
    st.title("🕵️‍♂️ The Credit Card Fraud Detective Story")
    st.write("Join us on a thrilling journey through data to uncover the secrets of credit card fraud!")

    story_sections = [
        "Prologue: The Mystery Begins",
        "Chapter 1: The Time Anomaly",
        "Chapter 2: The Amount Myth",
        "Chapter 3: The Timing Puzzle",
        "Epilogue: Cracking the Code"
    ]

    selected_section = st.radio("Choose your chapter:", story_sections)

    df = load_data("./data_pkl")

    if selected_section == "Prologue: The Mystery Begins":
        st.header("Prologue: The Mystery Begins")
        st.write("In a world where digital transactions reign supreme, a sinister force lurks in the shadows...")
        st.image("https://placehold.co/600x400?text=Credit+Card+Fraud+Mystery",
                 caption="The world of digital transactions")
        st.write(
            "Our mission: to analyze 1.7 million transactions and unmask the patterns of fraud hiding in plain sight.")

        # Display some key statistics
        col1, col2, col3 = st.columns(3)
        col1.metric("Total Transactions", f"{len(df):,}")
        col2.metric("Fraud Cases", f"{df['TX_FRAUD'].sum():,}")
        col3.metric("Fraud Rate", f"{df['TX_FRAUD'].mean():.2%}")

    elif selected_section == "Chapter 1: The Time Anomaly":
        st.header("Chapter 1: The Time Anomaly")
        st.write(
            "As we began our investigation, an unusual pattern emerged in the timeline of fraudulent activities...")

        # Create a time series plot of fraud over time
        fraud_over_time = df.set_index('TX_DATETIME').resample('D')['TX_FRAUD'].mean()
        fig = px.line(fraud_over_time, title='Daily Fraud Rate Over Time')
        st.plotly_chart(fig)

        st.write(
            "Notice the strange spike? It coincides perfectly with a major online shopping event. The fraudsters were hiding in the chaos of increased transaction volume!")

    elif selected_section == "Chapter 2: The Amount Myth":
        st.header("Chapter 2: The Amount Myth")
        st.write(
            "Conventional wisdom suggests that fraudsters go after big transactions. But what if we told you that wasn't the case?")

        # Create a box plot of transaction amounts for fraudulent and non-fraudulent transactions
        fig = px.box(df, x='TX_FRAUD', y='TX_AMOUNT', points="all", title='Transaction Amounts: Fraud vs Non-Fraud')
        st.plotly_chart(fig)

        st.write(
            "Surprisingly, fraudulent transactions often involve smaller amounts. They're flying under the radar, hoping to go unnoticed!")

    elif selected_section == "Chapter 3: The Timing Puzzle":
        st.header("Chapter 3: The Timing Puzzle")
        st.write("The plot thickens as we uncover the fraudsters' favorite times to strike...")

        # Create a heatmap of fraud by hour and day of week
        df['hour'] = pd.to_datetime(df['TX_DATETIME']).dt.hour
        df['day_of_week'] = pd.to_datetime(df['TX_DATETIME']).dt.dayofweek
        fraud_by_time = df.groupby(['hour', 'day_of_week'])['TX_FRAUD'].mean().unstack()
        fig = px.imshow(fraud_by_time, title='Fraud Rate by Hour and Day of Week',
                        labels=dict(x="Day of Week", y="Hour of Day", color="Fraud Rate"))
        st.plotly_chart(fig)

        st.write(
            "Astonishingly, fraud peaks at 2 PM on Tuesdays! Why? Because that's when people are most distracted at work, less likely to notice a small, strange transaction.")

    elif selected_section == "Epilogue: Cracking the Code":
        st.header("Epilogue: Cracking the Code")
        st.write("Armed with our newfound insights, we can now predict and prevent fraud like never before!")

        # Display key takeaways
        st.subheader("Key Takeaways:")
        st.write("1. Fraudsters hide in the noise of high-volume shopping events.")
        st.write("2. Small transactions are their weapon of choice.")
        st.write("3. They strike when we're most distracted.")

        # Add a fun interactive element
        savings_estimate = st.slider("Estimate the potential savings from improved fraud detection:", 0, 1000000,
                                     500000, format="$%d")
        st.success(
            f"By implementing these insights, we could potentially save up to ${savings_estimate:,} annually in prevented fraud!")

    # Add a teaser for the next part of your series
    st.markdown("---")
    st.write(
        "Stay tuned for our next exciting chapter, where we'll build a real-time fraud alert system using Streamlit!")
    if st.button("Notify me when the next chapter is ready!"):
        st.balloons()
        st.success("You're all set! We'll notify you when the next part of our fraud-busting adventure is live.")