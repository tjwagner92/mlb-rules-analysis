# MLB 2022-2023 Rule Changes Analysis 

## Overview
This is my first attempt at a project pipeline posted to Github in order to showcase what I have learned the past year regarding sports analytics and data science using various tools (Excel, Python, SQL, APIs, git, etc.).

The first project and set of scripts/notebooks is an exploration of MLB run-scoring for the season before (2022) and after (2023) several key rule changes were implemented (larger bases, pitch clock, no defensive shifts; https://www.baseball-almanac.com/rulechng.shtml) that would presumably increase game totals. 

## Key Findings
- Before changes (2022) avg runs/game: 8.57 -> After changes (2023): 9.23
    - Difference of +0.66 runs/game (7.7% increase) between years

## Data
- Regular season games only
- Sourced from MLB StatsAPI (https://github.com/toddrob99/MLB-StatsAPI)
- 4,860 total games (2,430 per season)

## How to run
### Install dependencies

```bash
pip install -r requirements.txt
```

### Fetch and clean data

```bash
python scripts/fetch_games.py
```

*this may take multiple requests for the official MLB API to work*

```bash
python scripts/clean_data.py
```

### Analyze runs/game differences

```bash
python scripts/analyze.py
```

### Or use Jupyter notebook

```bash
jupyter notebook notebooks/analysis.ipynb
```

## Skills Used
custom functions, pandas, matplotlib, numpy, data cleaning, data analysis, data visualization, Jupyter, git

## Challenges
The biggest challenge that I faced in the creation of this project was a mismatch between how many completed, regular-season games I was getting in the final dataset. I knew that each team in the MLB plays 162 games per season, there are 30 teams, and each game involves 2 teams, resulting in a total of 2,430 games/match-ups per season. No matter what I did, I kept getting 2,431 games for 2022 and 2,437 for 2023. In an attempt to minimize AI takeover of my project, this was one of my only consults to Claude Code, which confidently assured me the pulling of data, filtering, and overall pipeline was correct and that I should just move on with the analysis. Unsatisfied with that response, I remembered that in a previous exploration of the StatsAPI package there was a problem of game date mismatches for a very small subset of data that I had pinned down to be the rare occurrences of a game being started on one date, suspended while in-play, and then resumed and completed on another date. In these rare instances, the official MLB API actually duplicates the game with the exact same game_id (which should be unique in every game, even double-headers), and adds the fields resumeDate and resumeGameDate to the data on the 1st day of the game and resumedFrom and resumedFromDate to the 2nd day of the game. Thus, I chose to deduplicate based on game_id, which resulted in the correct number of games overall.