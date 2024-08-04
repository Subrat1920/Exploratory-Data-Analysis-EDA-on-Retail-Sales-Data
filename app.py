import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import streamlit as st
from wordcloud import WordCloud

# Load Datasets
retail_df = pd.read_csv('retail_sales_dataset.csv')

# Data Cleaning and Preparation
retail_df['Date'] = pd.to_datetime(retail_df['Date'])
retail_df['Age Group'] = pd.cut(retail_df['Age'], bins=[18, 30, 40, 50, 60, 70], labels=['18-30', '31-40', '41-50', '51-60', '61-70'])
retail_df['Month'] = retail_df['Date'].dt.to_period('M')

retail_df.set_index('Date', inplace=True)

monthly_sales=retail_df['Total Amount'].resample('M').sum()

menu_df=pd.read_csv('menu.csv')

# Define Streamlit App
st.title('Retail Sales Data Analysis')
st.header('Monthly Sales')
fig, ax = plt.subplots(figsize=(10, 6))
plt.plot(monthly_sales.index, monthly_sales.values, marker='o')
ax.set_title("Monthly Sales")
ax.set_xlabel('Date')
ax.set_ylabel('Total Amount')
plt.grid(True)
st.pyplot(fig)

rolling_mean=monthly_sales.rolling(window=3).mean()

st.header('Monthly Sales with Rolling Mean')
fig, ax = plt.subplots(figsize=(10, 6))
ax.plot(monthly_sales.index, monthly_sales.values, marker='o', label='Monthly Sales')
ax.plot(rolling_mean.index, rolling_mean.values, color='green', label='3-Months Rolling Mean')
ax.set_title("Monthly Sales with Rolling Mean")
ax.set_xlabel('Date')
ax.set_ylabel('Total Amount')
ax.grid(True)
ax.legend()
st.pyplot(fig)


# Age Distribution Plot
st.header('Distribution of Customer Ages')
fig, ax = plt.subplots(figsize=(10, 6))
sns.histplot(retail_df['Age'], bins=20, kde=True, color='blue', ax=ax)
ax.set_title('Distribution of Customer Ages')
ax.set_xlabel('Age')
ax.set_ylabel('Frequency')
st.pyplot(fig)



# Gender Distribution
st.header('Gender Distribution of Customers')
fig, ax = plt.subplots(figsize=(8, 5))
sns.countplot(x='Gender', data=retail_df, palette='viridis', ax=ax)
ax.set_title('Gender Distribution of Customers')
ax.set_xlabel('Gender')
ax.set_ylabel('Count')
st.pyplot(fig)


# Total Sales by Product Category
st.header('Total Sales by Product Category')
category_sales = retail_df.groupby('Product Category')['Total Amount'].sum().reset_index()
fig, ax = plt.subplots(figsize=(12, 6))
sns.barplot(x='Product Category', y='Total Amount', data=category_sales, palette='magma', ax=ax)
ax.set_title('Total Sales by Product Category')
ax.set_xlabel('Product Category')
ax.set_ylabel('Total Sales Amount')
ax.set_xticklabels(ax.get_xticklabels(), rotation=45)
st.pyplot(fig)




st.header('Categorical Count')
fig, ax=plt.subplots(figsize=(10,6))
sns.countplot(x='Category', data=menu_df)
ax.set_title('Categorical Count')
st.pyplot(fig)


st.header('Calories Versus Category')
fig, ax=plt.subplots(figsize=(10,6))
sns.lineplot(data=menu_df, x='Category', y='Calories')
st.pyplot(fig)


normal_value = ['Calories', 'Calories from Fat', 'Total Fat', 'Saturated Fat', 'Trans Fat', 'Cholesterol', 'Sodium', 'Carbohydrates', 'Dietary Fiber', 'Sugars', 'Protein']

# Melt the DataFrame
melted_df = pd.melt(menu_df, id_vars=['Category'], value_vars=normal_value, var_name='Nutrient', value_name='Value')

# Define Streamlit App
st.header('Line Plot of Nutritional Values')

# Create the plot
fig, ax = plt.subplots(figsize=(10, 6))
sns.lineplot(data=melted_df, x='Nutrient', y='Value', hue='Category', ax=ax)
ax.set_title('Nutritional Values by Category')
ax.set_xlabel('Nutrient')
ax.set_ylabel('Value')
ax.set_xticklabels(ax.get_xticklabels(), rotation=45)

# Display the plot in Streamlit
st.pyplot(fig)



daily_percent_value = ['Total Fat (% Daily Value)', 'Saturated Fat (% Daily Value)', 'Cholesterol (% Daily Value)', 'Sodium (% Daily Value)', 'Carbohydrates (% Daily Value)', 'Dietary Fiber (% Daily Value)', 'Vitamin A (% Daily Value)', 'Vitamin C (% Daily Value)', 'Calcium (% Daily Value)', 'Iron (% Daily Value)']

# Melt the DataFrame
melted_df = pd.melt(menu_df, id_vars=['Category'], value_vars=daily_percent_value, var_name='Nutrient', value_name='Value')

# Define Streamlit App

st.header('Line Plot of Nutritional Percentage')

# Create the plot
fig, ax = plt.subplots(figsize=(10, 6))
sns.lineplot(data=melted_df, x='Nutrient', y='Value', hue='Category', ax=ax)
ax.set_title('Nutritional Percentage by Category')
ax.set_xlabel('Nutrient Percentage Per Day')
ax.set_ylabel('Value')
ax.set_xticklabels(ax.get_xticklabels(), rotation=45)

# Display the plot in Streamlit
st.pyplot(fig)



numeric_cols = retail_df.select_dtypes(include='number')

# Calculate the correlation matrix
corr_matrix = numeric_cols.corr()

# Define Streamlit App

st.header('Correlation Heatmap')

# Create the heatmap
fig, ax = plt.subplots(figsize=(14, 10))
sns.heatmap(corr_matrix, annot=True, fmt='.2f', cmap='coolwarm', ax=ax)
ax.set_title('Correlation Heatmap of Retail Sales Data')

# Display the heatmap in Streamlit
st.pyplot(fig)





# Average Total Sales per Customer by Age Group
st.header('Average Total Sales per Customer by Age Group')
age_group_sales = retail_df.groupby('Age Group')['Total Amount'].mean().reset_index()
fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(x='Age Group', y='Total Amount', data=age_group_sales, palette='cubehelix', ax=ax)
ax.set_title('Average Total Sales per Customer by Age Group')
ax.set_xlabel('Age Group')
ax.set_ylabel('Average Total Sales Amount')
st.pyplot(fig)

# # Sales Trend Over Time
# st.header('Monthly Sales Trend')
# monthly_sales = retail_df.groupby('Month')['Total Amount'].sum().reset_index()
# fig, ax = plt.subplots(figsize=(14, 7))
# sns.lineplot(x='Month', y='Total Amount', data=monthly_sales, marker='o', color='green', ax=ax)
# ax.set_title('Monthly Sales Trend')
# ax.set_xlabel('Month')
# ax.set_ylabel('Total Sales Amount')
# ax.set_xticklabels(ax.get_xticklabels(), rotation=45)
# st.pyplot(fig)



sentences = menu_df['Category'].tolist()
sentence_as_a_string = ' '.join(sentences)

# Define Streamlit App
st.title('Word Cloud of Categories')

# Create the Word Cloud
wordcloud = WordCloud(width=2000, height=2000, background_color='white').generate(sentence_as_a_string)

# Create the plot
fig, ax = plt.subplots(figsize=(20, 20))
ax.imshow(wordcloud, interpolation='bilinear')
ax.axis('off')  # Hide the axes

# Display the Word Cloud in Streamlit
st.pyplot(fig)

# Analysis Insights
st.header('Analysis Insights')
st.write("""
1. **Age Distribution**: The age of customers ranges from 18 to 64, with a higher concentration between 30 and 50.
2. **Gender Distribution**: There are more male customers compared to female customers.
3. **Product Categories**: Electronics and Clothing generate the highest total sales.
4. **Average Sales by Gender**: Male customers tend to spend more on average than female customers.
5. **Average Sales by Age Group**: Customers aged 31-50 have the highest average spending.
6. **Sales Trend**: There are noticeable peaks in sales during certain months, indicating possible seasonal trends or promotional periods.
""")

st.header('Recommendation')
st.write("""
1. **Increase Inventory for High-Selling Product Categories:** Based on the sales data, certain product categories consistently generate higher revenue. Increasing inventory for these categories can meet customer demand and boost sales.

2. **Target Marketing Campaigns Based on Customer Demographics:** The gender and age distribution analysis provides insights into the primary customer base. Tailoring marketing campaigns to these demographics can improve customer engagement and sales.

3. **Analyze Monthly Sales Trends:** Seasonal patterns and monthly sales trends can help forecast demand and adjust inventory levels accordingly. Promotions can be timed to coincide with high-demand periods to maximize sales.

4. **Improve Product Mix:** By analyzing the correlation between different product categories and sales, the product mix can be optimized to include more profitable items and reduce less popular ones.

5. **Enhance Customer Experience:** Understanding customer purchasing behavior and preferences can help in enhancing the overall customer experience. Personalized offers and loyalty programs can be designed to retain customers and increase repeat purchases.
""")
