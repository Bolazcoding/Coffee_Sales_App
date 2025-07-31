import pandas as pd
import streamlit as st
import altair as alt

def load_data():
    df = pd.read_excel("Coffee_sales.xlsx")
    # replace the NaN with "None" / "Non-Card"

    df.loc[:, "card"] = df.card.fillna("Non-card")

    return df

try: 
    df = load_data()

    st.title("Coffee Sales App")

   
    # filters
    filters = {
        "coffee_name": df["coffee_name"].unique(),
        "Time_of_Day": df["Time_of_Day"].unique(),
        "Month_name": df["Month_name"].unique(),
        "cash_type": df["cash_type"].unique(),
        "Weekday": df["Weekday"].unique(),
    }
    # store user selection
    selected_filters = {}

    # generate multi-select widgets dynamically
    for key, options in filters.items():
        selected_filters[key] = st.sidebar.multiselect(key, options)

    # take a copy of the data
    filtered_df = df.copy()

    # apply filter selection to the data
    for key, selected_values in selected_filters.items():
        if selected_values:
            filtered_df = filtered_df[filtered_df[key].isin(selected_values)]

    # display the data
    st.dataframe(filtered_df)

    # st.dataframe(df.head(4))
    # st.dataframe(df)

    # section 2: Calculations
    no_of_cups = len(filtered_df)
    total_revenue = filtered_df["money"].sum()
    avg_sale = filtered_df["money"].mean()
    perct_sales_contrib = f"{(total_revenue / df["money"].sum()) * 100:,.2f}%"

    # display a quick overview using metrics

    st.write("### Quick Overview")

    # streamlit column components
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Cups Sold: ", no_of_cups)

    with col2: 
        st.metric("Revenue: ", f"{total_revenue:,.2f}")

    
    with col3: 
        st.metric("Avg Sale: ", f"{avg_sale:,.2f}")

    with col4: 
        st.metric("Percent Contribution to Sales: ", perct_sales_contrib)


    st.write("### Analysis Findings")

    temp_1 = df['Time_of_Day'].value_counts().reset_index()
    temp_1.columns = ["Time of Day", "Cups sold"]

    st.dataframe(temp_1)

    # simple chart
    import altair as alt

    chart_1 = alt.Chart(temp_1).mark_bar().encode(
        x=alt.X("Cups sold:Q"),
        y=alt.Y("Time of Day:N"),
        color=alt.Color("Time of Day:N", legend=None)

    ).properties(height = 250)

    # display the chart
    st.altair_chart(chart_1, use_container_width=True)

    # top coffee types
    st.write("### Revenue by Coffee Types")
    temp_2 = filtered_df.groupby("coffee_name")["money"].sum().\
        reset_index().sort_values(by ="money", ascending=False)

    # temp_2.columns = []
    st.dataframe(temp_2)

    # st.write("### Monthly Sales Trend")

    temp_3 = df.groupby("Month_name")["money"].sum().\
        reset_index().sort_values(by ="money", ascending=False)

     st.dataframe(temp_3)

    chart_2 = alt.Chart(temp_2).mark_bar().encode(
        x=alt.X("Coffee_name:N"),
        y=alt.Y("money:Q"),
        color=alt.Color("Coffee_name:N", legend=None)

    ).properties(height = 250)
    # display the chart
    st.altair_chart(chart_2)

    # st.subheader("### Average Revenue per Coffee Sold")

    # temp_5 = df.groupby("coffee_name")["money"].mean().\
    #     reset_index().sort_values(by ="money", ascending=False)
    # t.dataframe(temp_5)

    # chart_5 = alt.Chart(temp_5).mark_line().encode(
    #     x=alt.X("Coffee_name"),
    #     y=alt.Y("money"),
    #     # color=alt.Color("Coffee_name:N", legend=None)

    # ).properties(height = 250)

    #  st.altair_chart(chart_5)


except Exception as e: 
    st.error("Error: check error details")

    with st.expander("Error Details"):
        st.code(str (e))
        # st.code(traceback.format_exc())