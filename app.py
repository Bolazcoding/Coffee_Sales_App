import pandas as pd 
import streamlit as st 
import altair as alt

def load_data():

    df = pd.read_excel("Coffee_sales.xlsx")
    # replace the NaN with "Non-card"
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
        selected_filters[key] = st.sidebar.multiselect(key,options)

    # take a copy of the data
    filtered_df = df.copy()

    # apply filter selection to the data
    for key, selected_values in selected_filters.items():
        if selected_values:
            filtered_df = filtered_df[filtered_df[key].isin(selected_values)]

    # display the data
    # st.dataframe(filtered_df)


    # section 2: Calculations
    no_of_cups = len(filtered_df)
    total_revenue = filtered_df["money"].sum()
    avg_sales = filtered_df["money"].mean()
    perct_sales_contrib = f"{(total_revenue / df["money"].sum()) * 100:,.2f}%"

    # display a quick overview

    st.write("### Quick Overview")

    # streamlit column components
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Cups Sold: ", no_of_cups)

    with col2:
        st.metric("Total Revenue: ", f"{total_revenue:,.2f}")

    with col3:
        st.metric("Average Sale: ", f"{avg_sales:,.2f}")

    with col4:
        st.metric("Sales Percentage: ", perct_sales_contrib)

    # Analysis findings based on research questions
    st.write("### Analysis Findings")

    temp1 = df["Time_of_Day"].value_counts().reset_index()
    temp1.columns = ["Time of Day","Cups Sold"]

    st.dataframe(temp1)

    # simple chart
    import altair as alt

    chart1 = alt.Chart(temp1).mark_bar().encode(
        x=alt.X("Cups Sold:Q"),
        y=alt.Y("Time of Day:N"),
        color=alt.Color("Time of Day:N", legend=None)

    ).properties(height= 250)

    # display the chart
    st.altair_chart(chart1, use_container_width=True)

    # top coffee types
    st.write("### Revenue by Coffee Types")
    temp2 = filtered_df.groupby("coffee_name")["money"].sum().\
        reset_index().sort_values(by="money", ascending=False)
    # temp2.columns = []

    st.dataframe(temp2)

    chart2 = alt.Chart(temp2).mark_bar().encode(
        x=alt.X("coffee_name:N"),
        y=alt.Y("money:Q"),
        color=alt.Color("coffee_name:N", legend=None)

    ).properties(height= 250)

    st.altair_chart(chart2, use_container_width=True)


    # Monthly Sales Trend
    st.write("### Monthly Sales Trend")
    temp3 = filtered_df.groupby("Month_name")["money"].sum().\
    reset_index().sort_values(by="money", ascending=False)

    st.dataframe(temp3)

    # monthly plot
    chart3 = alt.Chart(temp3).mark_bar().encode(
        x=alt.X("Month_name:N"),
        y=alt.Y("money:Q"),
        color=alt.Color("Month_name:N", legend=None)

    ).properties(height= 250)

    st.altair_chart(chart3)

    # date plot
    chart4 = alt.Chart(df).mark_line(point=True).encode(
        x=alt.X("date:T"),
        y=alt.Y("money:Q"),
        color=alt.Color("coffee_name:N")

    ).properties(height= 250)

    st.altair_chart(chart4)



    st.subheader("Average Revenue Per Coffee Sold")

    temp5 = df.groupby("coffee_name")["money"].mean().\
    reset_index().sort_values(by="money", ascending =True)

    st.dataframe(temp5)

    chart5 = alt.Chart(temp5).mark_line(point=True).encode(
        x=alt.X("coffee_name"),
        y=alt.Y("money"),
    ).properties(height= 250)

    st.altair_chart(chart5)




except Exception as e:
    st.error("Error: check error details")

    with st.expander("Error Details"):
        st.code(str(e))
        # st.code(traceback.format_exc())
