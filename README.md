📊 Features
Loads and processes trade data from an Excel file

Computes key performance metrics:

Expectancy & Expectancy Score

Edge Ratio

Analyzes trade performance by:

Time of Day

Trading Symbol

Performs Monte Carlo Simulations to visualize the range of potential equity curves

Provides summary statistics of simulated outcomes

📂 File Input
The script reads data from the following Excel file:

bash
Copy
Edit
D:/Work/csvs/4B_Backtest.xlsx
Sheet: backtest_results_latest

Expected columns in the dataset:

symbol

open_datetime

close_datetime

order_type

volume

profit

⚙️ Assumptions
Fixed risk per trade: $250

Trades with zero volume or missing profit values are excluded from analysis.

📈 Key Metrics
Expectancy
Indicates the average expected return per trade.

Expectancy Score
Risk-adjusted expectancy based on the standard deviation of profits.

Edge Ratio
Compares the average gain on winning trades to the average loss on losing trades.

Time and Symbol Performance
Groups and displays statistics by:

Hour of the trade

Trading symbol (currency pair, index, etc.)

Monte Carlo Simulation
Simulates 1,000 equity curve paths by randomly sampling the list of profits with replacement. This provides a range of possible outcomes based on your historical data.

📌 Output
Console Output:

Expectancy, Edge Ratio, Expectancy Score

Hourly and symbol-level trade summaries

Monte Carlo profit distribution stats: median, min, max, 5th/95th percentiles

Plot:

A chart showing 100 simulated equity curves to visualize potential performance variability.

🛠 Dependencies
Install required Python libraries using:

bash
Copy
Edit
pip install pandas numpy matplotlib scipy openpyxl
📄 How to Use
Adjust the file_path variable to match your Excel file path and sheet name.

Run the script using any Python interpreter.

Review the printed stats and chart for insights into your trading strategy's robustness and risk profile.

![image](https://github.com/user-attachments/assets/afcfd273-8d64-4de8-93a1-20f3b5372139)
