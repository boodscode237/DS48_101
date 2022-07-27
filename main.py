# Core Python Data Analysis
from numpy.core.defchararray import index
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Plotting
from plotnine import (
    ggplot, aes,
    geom_col, geom_line, geom_smooth,
    facet_wrap,
    scale_y_continuous, scale_x_datetime,
    labs,
    theme, theme_minimal, theme_matplotlib,
    expand_limits,
    element_text
)

from mizani.breaks import date_breaks
from mizani.formatters import date_format, currency_format

# Misc
from os import mkdir, getcwd

from rich import pretty
pretty.install()

# import xlrd

# help(pd.read_excel)
# files_SPB_new = xlrd.open_workbook(r'bikes.xlsx')
bikes_df = pd.read_excel("bikes.xlsx")
bikeshops_df = pd.read_excel('bikeshops.xlsx')

orderlines_df = pd.read_excel(
    io = "orderlines.xlsx",
    converters= {'order.date': str}
)

orderlines_df.head()

s = bikes_df['description']

frequencies_count = s.value_counts()

frequencies_count.nlargest(5)
print(frequencies_count.nlargest(5))

top_5_bikes_series = bikes_df['description'].value_counts().nlargest(5)
fig_0 = pd.Series.plot(top_5_bikes_series)
fig_0
plt.show()
fig_1 = top_5_bikes_series.plot(kind="barh")
fig_1
plt.show()

fig_2 = top_5_bikes_series.plot(kind="barh")
fig_2.invert_yaxis()
fig_2
plt.show()

# orderlines_df = pd.Dataframe(orderlines_df)
print(orderlines_df.drop(columns='Unnamed: 0', axis=1))
print(bikes_df)

# merging orderlines with bikes
orderlines_df.drop(columns='Unnamed: 0', axis=1) \
    .merge(
        right = bikes_df,
        how='left',
        left_on='product.id',
        right_on='bike.id'
)

# merging orderlines with bikes with bikes shop
bikes_orderlines_joined_df = orderlines_df.drop(columns='Unnamed: 0', axis=1) \
    .merge(
        right = bikes_df,
        how='left',
        left_on='product.id',
        right_on='bike.id'
) \
    .merge(
            right = bikeshops_df,
            how='left',
            left_on='customer.id',
            right_on='bikeshop.id'
    )

print(bikes_orderlines_joined_df)
df = bikes_orderlines_joined_df
df2 = bikes_orderlines_joined_df.copy()
df

print(df['order.date'])
df['order.date'] = pd.to_datetime(df['order.date'])

bikes_orderlines_joined_df.info()
print(df.T)
temp_df = df['description'].str.split(pat=" - ", expand = True) #allows us to apply string methods
print(temp_df)

df['category.1'] = temp_df[0]
df['category.1']

df['category.2'] = temp_df[1]
df['category.2']

df['frame.material'] = temp_df[2]

df['frame.material']

print(df)

temp_df = df['location'].str.split(pat=', ', n = 1, expand = True)

print(temp_df)
df['city'] = temp_df[0]
df['state'] = temp_df[1]


df['total.price'] = df['quantity'] * df['price']
print(df)
df.sort_values('total.price', ascending=False)

cols_to_keep = [
    'order.id',
    'order.line',
    'order.date',
    'model',
    'quantity',
    'price',
    'total.price',
    'bikeshop.name',
    'category.1',
    'category.2',
    'frame.material',
    'city',
    'state'
]

df[cols_to_keep]

df = df[cols_to_keep]

print(df)
new_cols = df.columns.str.replace(pat='.', repl='_')

df.columns = new_cols
print(df)
bikes_orderlines_wrangled_df = df
# df = pd.Dataframe(df)
order_date_series = df['order_date']
order_date_series.dt.year
df[[ 'order_date', 'total_price' ]] \
    .set_index('order_date') \
    .resample(rule='YS') \
    .sum()
# Year start

df[[ 'order_date', 'total_price' ]] \
    .set_index('order_date') \
    .resample(rule='Y') \
    .sum()

df[[ 'order_date', 'total_price' ]] \
    .set_index('order_date') \
    .resample(rule='YS') \
    .aggregate(np.sum)

# sales by month
sales_by_months = df[[ 'order_date', 'total_price' ]] \
    .set_index('order_date') \
    .resample(rule='MS') \
    .aggregate(np.sum) \
    .reset_index()

# QUICK PLOT ----

sales_by_months.plot(x='order_date', y='total_price')
plt.show()

data_ = sales_by_months

ggplot(data=data_, mapping=aes(x='order_date', y="total_price")) + \
geom_line() + \
geom_smooth(method = "loess")
