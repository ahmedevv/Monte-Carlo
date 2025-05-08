import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm

file_path = 'D:/Work/csvs/4B_Backtest.xlsx'
df = pd.read_excel(file_path, sheet_name='backtest_results_latest')

df_bt = df.copy()

# Convert datetime
df_bt["open_datetime"] = pd.to_datetime(df_bt["open_datetime"])
df_bt["close_datetime"] = pd.to_datetime(df_bt["close_datetime"])

# Add 'R' (R-multiple) column: profit / assumed fixed risk of $250
RISK_PER_TRADE = 250.0
df_bt["R"] = df_bt["profit"] / RISK_PER_TRADE

# Include only valid trades (non-zero volume and valid profit)
df_bt = df_bt[df_bt["volume"] > 0]
df_bt = df_bt[~df_bt["profit"].isna()]

# Preview after processing
df_bt[["symbol", "open_datetime", "order_type", "profit", "R"]].head()

# Ensure correct types
df_bt["PnL"] = df_bt["profit"].astype(float)
df_bt["R"] = df_bt["R"].astype(float)


# 1. Expectancy & Expectancy Score
def calculate_expectancy(df_bt):
    win_trades = df_bt[df_bt["PnL"] > 0]
    loss_trades = df_bt[df_bt["PnL"] < 0]
    win_rate = len(win_trades) / len(df_bt)
    avg_win = win_trades["PnL"].mean()
    avg_loss = abs(loss_trades["PnL"].mean())
    
    expectancy = win_rate * avg_win - (1 - win_rate) * avg_loss
    expectancy_score = expectancy / df_bt["PnL"].std()
    return expectancy, expectancy_score

# 2. Edge Ratio
def calculate_edge_ratio(df_bt):
    afe = df_bt[df_bt["R"] > 0]["R"].mean()
    aae = abs(df_bt[df_bt["R"] < 0]["R"].mean())
    return afe / aae if aae != 0 else np.nan



# 4. Time-of-Day / Pair Performance
def analyze_grouping(df_bt):
    df_bt["Hour"] = df_bt["open_datetime"].dt.hour
    hourly_stats = df_bt.groupby("Hour")["PnL"].agg(["count", "sum", "mean"])
    pair_stats = df_bt.groupby("symbol")["PnL"].agg(["count", "sum", "mean"]).sort_values("sum", ascending=False)

    print("\nHourly Performance:\n", hourly_stats)
    print("\nPair Performance:\n", pair_stats)

# Run analysis
expectancy, expectancy_score = calculate_expectancy(df_bt)
edge_ratio = calculate_edge_ratio(df_bt)

print(f"Expectancy: ${expectancy:.2f}")
print(f"Expectancy Score: {expectancy_score:.2f}")
print(f"Edge Ratio: {edge_ratio:.2f}")

analyze_grouping(df_bt)




def monte_carlo_simulation(profit_list, n_simulations=1000, n_trades=None):
    if n_trades is None:
        n_trades = len(profit_list)

    simulations = []
    for _ in range(n_simulations):
        sampled_returns = np.random.choice(profit_list, size=n_trades, replace=True)
        equity_curve = np.cumsum(sampled_returns)
        simulations.append(equity_curve)

    return np.array(simulations)

# Run simulation
profit_list = df_bt["profit"].values
simulated_curves = monte_carlo_simulation(profit_list, n_simulations=1000)

# Plot
plt.figure(figsize=(12, 6))
for curve in simulated_curves[:100]:  # Plot only first 100 to reduce clutter
    plt.plot(curve, color='blue', alpha=0.1)

plt.title("Monte Carlo Simulation of Equity Curve (100 paths)")
plt.xlabel("Trades")
plt.ylabel("Cumulative Profit ($)")
plt.grid(True)
plt.axhline(0, color='black', linestyle='--', linewidth=0.8)
plt.show()
final_profits = simulated_curves[:, -1]

# Summary stats
print(f"Median Final Profit: ${np.median(final_profits):,.2f}")
print(f"Max Final Profit:    ${np.max(final_profits):,.2f}")
print(f"Min Final Profit:    ${np.min(final_profits):,.2f}")
print(f"5th Percentile:       ${np.percentile(final_profits, 5):,.2f}")
print(f"95th Percentile:      ${np.percentile(final_profits, 95):,.2f}")