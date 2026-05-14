import pandas as pd



def recommend_restaurants(filepath, cuisine):

    df = pd.read_csv(filepath)

    if 'listed_in(type)' not in df.columns:
        return []

    recommendations = df[
        df['listed_in(type)'].str.contains(cuisine, case=False, na=False)
    ]

    recommendations = recommendations.sort_values(
        by=['rate', 'votes'],
        ascending=False
    )

    return recommendations[['name', 'rate', 'votes']].head(10).to_dict(orient='records')