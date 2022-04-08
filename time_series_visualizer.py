import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import re
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

# Import data (Make sure to parse dates. Consider setting index column to 'date'.)
df = pd.read_csv('fcc-forum-pageviews.csv', index_col='date')

# Clean data
df = df[(df['value'] >= df['value'].quantile(0.025)) & (df['value'] <= df['value'].quantile(0.975))]


def draw_line_plot():
    # Draw line plot
    fig, ax = plt.subplots(figsize=(32, 10))
    x = df.index.values.tolist()
    y = df['value']

    ax.plot(x, y, linewidth=1.0, color = 'r')

    ax.set_title("Daily freeCodeCamp Forum Page Views 5/2016-12/2019")
    ax.set_xlabel('Date')
    ax.set_ylabel('Page Views')

    # Save image and return fig (don't change this part)
    fig.savefig('line_plot.png')
    return fig

def draw_bar_plot():
    # Copy and modify data for monthly bar plot
    df_bar = df.copy()
    df_bar['Year'] = [int(re.findall("(\d+)(-)(\d+)(-)(\d+)", val)[0][0]) for val in df.index.values.tolist()]
    df_bar['Month'] = [int(re.findall("(\d+)(-)(\d+)(-)(\d+)", val)[0][2]) for val in df.index.values.tolist()]
    months = {1:'January', 2:'February', 3:'March', 4:'April', 5:'May', 6:'June', 7:'July', 8:'August', 9:'September', 10:'October', 11:'November', 12:'December'}
    df_bar['Month'] = [months[val] for val in df_bar['Month']]
    df_bar = pd.DataFrame(df_bar.groupby(["Year", "Month"], sort=False)["value"].mean().round().astype(int)).rename(columns={"value": "Average Page Views"}).reset_index()

    # Draw bar plot
    fig, ax = plt.subplots(figsize=(7.22, 6.35))
  
    month_order = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
    sns.barplot(data=df_bar, x="Year", y="Average Page Views", hue="Month", hue_order=month_order, palette="tab10")
    fig.legend(loc ='upper left', title='Months')

    ax.set_xlabel('Years')
    ax.set_ylabel('Average Page Views')

    # Save image and return fig (don't change this part)
    fig.savefig('bar_plot.png')
    return fig

def draw_box_plot():
    # Prepare data for box plots (this part is done!)
    df_box = df.copy()
    df_box['Year'] = [int(re.findall("(\d+)(-)(\d+)(-)(\d+)", val)[0][0]) for val in df.index.values.tolist()]
    df_box['Month'] = [int(re.findall("(\d+)(-)(\d+)(-)(\d+)", val)[0][2]) for val in df.index.values.tolist()]
    months = {1:'Jan', 2:'Feb', 3:'Mar', 4:'Apr', 5:'May', 6:'Jun', 7:'Jul', 8:'Aug', 9:'Sep', 10:'Oct', 11:'Nov', 12:'Dec'}
    df_box['Month'] = [months[val] for val in df_box['Month']]

    # Draw box plots (using Seaborn)
    fig, axes = plt.subplots(1, 2, figsize=(32, 10), dpi=100)

    # Yearly boxplot
    sns.boxplot(data=df_box, x="Year", y="value", ax=axes[0])
    axes[0].set_title("Year-wise Box Plot (Trend)")
    axes[0].set_xlabel("Year")
    axes[0].set_ylabel("Page Views")

    # Monthly boxplot
    month_order = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    sns.boxplot(data=df_box, x="Month", y="value", order=month_order, ax=axes[1])
    axes[1].set_title("Month-wise Box Plot (Seasonality)")
    axes[1].set_xlabel("Month")
    axes[1].set_ylabel("Page Views")

    # Save image and return fig (don't change this part)
    fig.savefig('box_plot.png')
    return fig
