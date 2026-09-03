import pandas as pd
import numpy as np
from scipy.stats import ttest_ind, levene, mannwhitneyu
import matplotlib.pyplot as plt

def summary_statistics(df):
    """
    Calculate and print summary stats by year
    
    Args:
        df: dataframe of cleaned MLB games
    
    Returns:
        summary statistics of total_score by year
    """
    df = df.copy()

    summary_df = df.groupby('year').agg(
        n_games = ('total_score', 'count'),
        total_runs = ('total_score', 'sum'),
        avg_runs = ('total_score', 'mean'),
        std_runs = ('total_score', 'std')
    )

    return summary_df

def create_visualizations(df):
    """
    Create key visualizations
    
    Args:
        df: dataframe of cleaned MLB games
    
    Returns:
        histogram, box plot, bar chart
    """

    fig, axes = plt.subplots(2, 2, figsize=(12, 10))

    # Histogram of runs/game
    axes[0,0].hist(df[df['year'] == 2022]['total_score'], 
                   bins=15, alpha=0.5,
                   label='2022', color='blue', density=True,)
    axes[0,0].hist(df[df['year'] == 2023]['total_score'], 
                   bins=15, alpha=0.5,
                   label='2023', color='red', density=True,)
    axes[0,0].set_xlabel('Total Runs Per Game')
    axes[0,0].set_ylabel('Density')
    axes[0,0].set_title('Distribution of Runs Per Game')
    axes[0,0].legend()

    # Violin plot of quartiles
    parts = axes[0,1].violinplot([df[df['year'] == 2022]['total_score'],
                                df[df['year'] == 2023]['total_score']],
                                positions=[0, 1], showmeans=False, showmedians=True)
    axes[0,1].set_xticks([0, 1])
    axes[0,1].set_xticklabels(['2022', '2023'])
    axes[0,1].set_ylabel('Total Runs Per Game')
    axes[0,1].set_title('Distribution & Median Runs Per Game')

    # Mean runs per year bar
    summary = summary_statistics(df)
    print("Summary dataframe:")
    print(summary)
    print("Index:", summary.index.tolist())
    axes[1,0].bar([0, 1], summary['avg_runs'],
                  yerr=summary['std_runs'],
                  color=['blue', 'red'],
                  width=0.5,
                  capsize=5,
                  error_kw={'elinewidth': 2, 'linewidth': 2})
    axes[1,0].set_ylabel('Average runs Per Game')
    axes[1,0].set_title('Mean Runs Comparison')
    axes[1,0].set_xticks([0, 1])
    axes[1,0].set_xticklabels(['2022', '2023'])

    # 4. Cumulative runs over season
    for year in [2022, 2023]:
        year_data = df[df['year'] == year].sort_values('date')
        axes[1,1].plot(range(len(year_data)), year_data['total_score'].cumsum(),
                    label=str(year), linewidth=2)
        axes[1,1].set_xlabel('Game Number')
        axes[1,1].set_ylabel('Cumulative Runs')
        axes[1,1].set_title('Total Runs Over Season')
        axes[1,1].legend()
        axes[1,1].grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig('results/analysis.png')
    plt.show()

def run_stats(df):
    df = df.copy()
    """
    Run simple stats tests
    
    Args:
        df: dataframe of cleaned MLB games
    
    Returns:
        Assumption checks and ttest results
    """

    # Separate samples
    runs_2022 = df[df['year'] == 2022]['total_score']
    runs_2023 = df[df['year'] == 2023]['total_score']

    # Test equal variance
    stat, p_value = levene(runs_2022, runs_2023)
    print(f"Levene's test p-value: {p_value:.4f}")
    if p_value > 0.05:
        print("✓ Equal variances assumption holds")
        t_stat, p_value = ttest_ind(runs_2022, runs_2023, equal_var=True)
        print("t-test:")
        print(f"    T-statistic: {t_stat:.4f}")
        print(f"    P-value: {p_value:.2e}")
    else:
        print("✗ Unequal variances - use Welch's t-test instead")
        t_stat, p_value = ttest_ind(runs_2022, runs_2023, equal_var=False)
        print("t-test:")
        print(f"    T-statistic: {t_stat:.4f}")
        print(f"    P-value: {p_value:.2e}")

    # Non-parametric test (doesn't assume normality)
    stat, p_value = mannwhitneyu(runs_2022, runs_2023, alternative='two-sided')
    print(f"Mann-Whitney U test:")
    print(f"    U-statistic: {stat:.2f}")
    print(f"    P-value: {p_value:.2e}")

if __name__ == "__main__":
    df = pd.read_csv('data/games_clean.csv')
    print(summary_statistics(df))
    create_visualizations(df)
    run_stats(df)