from utils.preprocessing import load_restaurant_data


def generate_charts(filepath):
    df = load_restaurant_data(filepath)
    return {
        "types": df["listed_in(type)"].value_counts().to_dict(),
        "ratings": df["rate"].round(1).value_counts().sort_index().to_dict(),
        "online_orders": df["online_order"].value_counts().to_dict(),
    }
