import streamlit as st
import pandas as pd
from databricks import sql

# Function to query the Databricks warehouse
# def query_database(supplier):
#     query = f"SELECT product_id, price FROM prods.data.products WHERE supplier = '{supplier}'"
#     try:
#         with sql.connect(
#             server_hostname="<your-databricks-server-hostname>",
#             http_path="<your-databricks-http-path>",
#             access_token="<your-databricks-access-token>"
#         ) as connection:
#             with connection.cursor() as cursor:
#                 cursor.execute(query)
#                 rows = cursor.fetchall()
#                 # Convert query result to a Pandas DataFrame
#                 df = pd.DataFrame(rows, columns=["product_id", "price"])
#                 return df
#     except Exception as e:
#         st.error(f"Error querying the database: {e}")
#         return pd.DataFrame(columns=["product_id", "price"])

def query_database(supplier):
    data = {
        "supplier_id": [f"S{str(i).zfill(3)}" for i in range(1, 11)],
        "product_id": [f"P{str(i).zfill(4)}" for i in range(1, 11)],
        "sku": [f"SKU-{random.randint(1000, 9999)}" for _ in range(10)],
        "price": [round(random.uniform(10.0, 100.0), 2) for _ in range(10)],
    }
    return pd.DataFrame(data)

# Streamlit app UI
def main():
    st.title("Databricks Database Interaction")
    
    # Dropdown menu for suppliers
    supplier_options = ["Supplier A", "Supplier B", "Supplier C"]
    supplier = st.selectbox("Supplier", options=["Select a supplier"] + supplier_options)

    # "Run Query" button
    run_query_button = st.button("Run Query", disabled=(supplier == "Select a supplier"))

    # Display initial text or table
    if "query_result" not in st.session_state:
        st.session_state.query_result = None

    if st.session_state.query_result is None:
        if not run_query_button:
            st.write("Please run a query to display the data.")
        else:
            st.write("The query is running, please wait...")

    # Run the query if button is pressed
    if run_query_button and supplier != "Select a supplier":
        st.session_state.query_result = query_database(supplier)

    # Display query results as a table with filters
    if st.session_state.query_result is not None:
        df = st.session_state.query_result
        
        # Add filters for product_id and price
        with st.expander("Filters"):
            product_id_filter = st.text_input("Filter by Product ID")
            price_filter = st.number_input("Filter by Price", value=0.0, step=0.01)

        # Apply filters to the DataFrame
        if product_id_filter:
            df = df[df["product_id"].astype(str).str.contains(product_id_filter)]
        if price_filter > 0:
            df = df[df["price"] >= price_filter]

        # Display the DataFrame
        st.dataframe(df, height=400)

if __name__ == "__main__":
    main()
