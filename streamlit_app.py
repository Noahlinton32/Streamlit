import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker

# Replace 'data.csv' with the actual filename and path of your CSV file
csv_file = 'data.csv'

# Read the CSV file into a pandas DataFrame
df = pd.read_csv(csv_file)

# Removing outliers from 'price' and 'house_size' columns
df = df[
    (df['price'] >= df['price'].mean() - 3 * df['price'].std()) &
    (df['price'] <= df['price'].mean() + 3 * df['price'].std())
]
df = df[
    (df['house_size'] >= df['house_size'].mean() - 3 * df['house_size'].std()) &
    (df['house_size'] <= df['house_size'].mean() + 3 * df['house_size'].std())
]

# Calculate descriptive statistics
statistics = df.describe().transpose()

# Sort by option
sort_option = st.selectbox('Sort by:', options=statistics.columns.tolist())

# Ascending/Descending option
asc_desc = st.selectbox('Order:', options=['Ascending', 'Descending'])
order = True if asc_desc == 'Ascending' else False

statistics = statistics.sort_values(by=sort_option, ascending=order)

# Display the statistics with streamlit
st.write("Descriptive Statistics:")
st.table(statistics)

# Additional Statistics
st.write("Additional Statistics:")
st.write(f"Number of rows: {len(df):,}")
st.write(f"Average price: ${df['price'].mean():,.2f}")
st.write(f"Minimum price: ${df['price'].min():,.2f}")
st.write(f"Maximum price: ${df['price'].max():,.2f}")
st.write(f"Average number of bedrooms: {df['bed'].mean():.1f}")
st.write(f"Average number of bathrooms: {df['bath'].mean():.1f}")

# Visualizations
# Histogram of prices
plt.figure(figsize=(8, 6))
plt.hist(df['price'], bins=20, edgecolor='black', color='skyblue')
plt.xlabel('Price')
plt.ylabel('Frequency')
plt.title('Histogram of Prices')
plt.gca().xaxis.set_major_formatter(mticker.StrMethodFormatter('${x:,.0f}'))
plt.grid(True)
st.pyplot(plt)

# Scatter plot of house size vs. price
plt.figure(figsize=(8, 6))
plt.scatter(df['house_size'], df['price'], color='orange', alpha=0.7)
plt.xlabel('House Size')
plt.ylabel('Price')
plt.title('House Size vs. Price')
plt.gca().xaxis.set_major_formatter(mticker.StrMethodFormatter('{x:,.0f}'))
plt.gca().yaxis.set_major_formatter(mticker.StrMethodFormatter('${x:,.0f}'))
plt.grid(True)
st.pyplot(plt)

# Bar plot of the number of houses in each state (only showing states with at least 100 data points)
state_counts = df['state'].value_counts()
filtered_state_counts = state_counts[state_counts >= 100]
plt.figure(figsize=(8, 6))
filtered_state_counts.plot(kind='bar', color='green')
plt.xlabel('State')
plt.ylabel('Number of Houses')
plt.title('Number of Houses in Each State')
plt.gca().yaxis.set_major_formatter(mticker.StrMethodFormatter('{x:,.0f}'))
plt.grid(axis='y')
st.pyplot(plt)
