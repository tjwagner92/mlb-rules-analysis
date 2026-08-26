# Prepare the raw data be analyzed by getting year and total, as well
# as ensuring data quality for all variables

import pandas as pd
import os

def clean_games(df):
    """
    Clean and prepare 2022 + 23 MLB data for analysis.
    - ensure date column is datetime object
    - extract 'year' from date
    - home_score+away_score = total_score
    
    Args:
        df: dataframe of MLB games
    
    Returns:
        cleaned version of df
    """
    df = df.copy()

    # Convert date to datetime and get year
    df['date'] = pd.to_datetime(df['date'])
    df['year'] = df['date'].dt.year

    # Get total_score
    df['total_score'] = df['home_score'] + df['away_score']

    return df

if __name__ == "__main__":
    # Load raw data
    df = pd.read_csv('data/games.csv')
    print(f"Loaded {len(df)} games")

    # Clean it
    df_clean = clean_games(df)
    print(df_clean.info())
    print(f"Missing values:\n{df_clean.isnull().sum()}")

    # Save it
    data_path = 'data/games_clean.csv'
    full_path = os.path.abspath(data_path)
    df_clean.to_csv(data_path, index=False)
    print(f"Saved {len(df)} games to {full_path}")