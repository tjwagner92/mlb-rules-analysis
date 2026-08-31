# Use the statsapi MLB API wrapper to get the scheduled games from
# 2022 and 2023 seasons, extracting only necessary data and 
# converting to a dataframe

import statsapi
import pandas as pd
import os

def fetch_games(start_date, end_date):
    """
    Fetch all games between start_date and end_date.
    
    Args:
        start_date: formatted 'mm/dd/yyyy'
        end_date: same as above
    
    Returns:
        list of game data dictionaries
    """
    games = statsapi.schedule(start_date=start_date, end_date=end_date)
    return games

if __name__ == "__main__":
    games_2022 = fetch_games('01/01/2022', '12/31/2022')
    games_2023 = fetch_games('01/01/2023', '12/31/2023')
    print(f"Fetched {len(games_2022)} games in 2022")
    print(f"Fetched {len(games_2023)} games in 2023")

    reg_season_games_2022 = [game for game in games_2022 
                             if game['game_type'] =='R' and
                             (game['status'].startswith('Final') or
                              game['status'].startswith('Completed Early'))]
    print(f"Fetched {len(reg_season_games_2022)} complete, regular season games in 2022")
    reg_season_games_2023 = [game for game in games_2023 
                             if game['game_type'] =='R' and
                             (game['status'].startswith('Final') or
                              game['status'].startswith('Completed Early'))]
    print(f"Fetched {len(reg_season_games_2023)} complete, regular season games in 2023")

    reg_season_games = reg_season_games_2022 + reg_season_games_2023

    cleaned_games = [
        {
            'game_id': game['game_id'],
            'date': game['game_date'],
            'home_team': game['home_name'],
            'away_team': game['away_name'],
            'home_score': game['home_score'],
            'away_score': game['away_score'],
        }
        for game in reg_season_games
    ]

    sample_game = cleaned_games[0]
    print("Sample Game:")
    print(f"{sample_game['away_team']}:{sample_game['away_score']} @ "
          f"{sample_game['home_team']}:{sample_game['home_score']}")

    df = pd.DataFrame(cleaned_games)
    df = df.drop_duplicates(subset=['game_id'], keep='first')

    data_path = 'data/games.csv'
    full_path = os.path.abspath(data_path)
    df.to_csv(data_path, index=False)
    print(f"Saved {len(df)} games to {full_path}")
    