import pandas as pd


def handle_rate(value):
    try:
        value = str(value).split('/')[0]
        return float(value)
    except:
        return 0


def preprocess_data(filepath):

    df = pd.read_csv(filepath)

    if 'rate' in df.columns:
        df['rate'] = df['rate'].apply(handle_rate)

    df.dropna(inplace=True)

    df.to_csv(filepath, index=False)