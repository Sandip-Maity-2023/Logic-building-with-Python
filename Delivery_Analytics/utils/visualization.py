import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os


CHART_FOLDER = 'static/charts'


if not os.path.exists(CHART_FOLDER):
    os.makedirs(CHART_FOLDER)



def generate_charts(filepath):

    df = pd.read_csv(filepath)

    plt.figure(figsize=(8, 5))
    sns.countplot(x=df['listed_in(type)'])
    plt.xticks(rotation=45)
    plt.title('Restaurant Types')
    plt.tight_layout()
    plt.savefig(f'{CHART_FOLDER}/restaurant_types.png')
    plt.close()

    plt.figure(figsize=(8, 5))
    plt.hist(df['rate'], bins=5)
    plt.title('Rating Distribution')
    plt.xlabel('Ratings')
    plt.ylabel('Frequency')
    plt.tight_layout()
    plt.savefig(f'{CHART_FOLDER}/ratings_distribution.png')
    plt.close()

    plt.figure(figsize=(8, 5))
    sns.countplot(x=df['online_order'])
    plt.title('Online Order Availability')
    plt.tight_layout()
    plt.savefig(f'{CHART_FOLDER}/online_orders.png')
    plt.close()

    pivot = df.pivot_table(
        index='listed_in(type)',
        columns='online_order',
        aggfunc='size',
        fill_value=0
    )

    plt.figure(figsize=(8, 5))
    sns.heatmap(pivot, annot=True, cmap='YlGnBu', fmt='d')
    plt.title('Restaurant Distribution Heatmap')
    plt.tight_layout()
    plt.savefig(f'{CHART_FOLDER}/heatmap.png')
    plt.close()