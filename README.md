# Stock Portfolio Performance Comparison

This repository contains a Python project developed to compare the accumulated performance of multiple stock portfolios over time.

The script reads investment records from Excel files, retrieves historical stock prices using Yahoo Finance and calculates each portfolio’s accumulated return through a quota-based methodology. The result is displayed as a comparative performance chart.

## Objective

Compare the profitability of two or more stock portfolios, considering different purchase dates, assets and contribution amounts.

The project was created to make portfolio performance analysis simpler and more visual, allowing users to evaluate how different investment strategies performed over time.

## Features

* Reads portfolio data from `.xlsx` files
* Downloads adjusted stock prices with `yfinance`
* Calculates accumulated position by asset
* Uses a quota-based method to account for new contributions
* Compares multiple portfolios in the same chart
* Plots accumulated portfolio profitability over time
* Supports comparison with the Ibovespa index through Yahoo Finance

## Input File

Each portfolio must be stored in an Excel file with the following structure:

```text
Data | Ativo | Quantidade
```

Example:

```text
Data       | Ativo   | Quantidade
2023-01-10 | PETR4.SA | 100
2023-02-15 | VALE3.SA | 50
2023-03-20 | ITUB4.SA | 80
```

The file name must be entered without the `.xlsx` extension when running the script.

Example:

```text
carteira_1
```

For a file named:

```text
carteira_1.xlsx
```

## Methodology

The script follows these main steps:

1. Reads each portfolio from an Excel file.
2. Organizes transactions by date and asset.
3. Downloads historical adjusted closing prices.
4. Reindexes the portfolio according to available market dates.
5. Calculates accumulated quantities for each asset.
6. Multiplies asset quantities by adjusted prices.
7. Calculates total portfolio value over time.
8. Applies a quota-based calculation to adjust for new contributions.
9. Plots the accumulated return of each portfolio.

## Requirements

Install the main dependencies:

```bash
pip install pandas numpy yfinance matplotlib openpyxl
```

## Usage

Run the script:

```bash
python portfolio_comparison.py
```

Then enter the number of portfolios to analyze:

```text
Quantas carteiras deseja analisar?
```

After that, enter the name of each `.xlsx` file without the extension:

```text
Digite o nome do 1º arquivo xlsx:
Digite o nome do 2º arquivo xlsx:
```

## Output

The script generates a line chart comparing the accumulated profitability of each portfolio.

The chart includes:

* Portfolio return over time
* Horizontal reference line at `1`
* Legend identifying each portfolio
* Date on the x-axis
* Accumulated profitability on the y-axis

## Applications

* Comparing investment portfolios
* Evaluating stock-picking strategies
* Tracking accumulated profitability
* Visualizing portfolio performance over time
* Comparing different allocation strategies
* Educational financial analysis with Python

## Notes

The project uses adjusted closing prices from Yahoo Finance through the `yfinance` library. Results may vary depending on data availability, asset tickers and market calendar.

This project is intended for educational and analytical purposes and does not constitute investment advice.

## Authorship

This project was developed by Peterson Oliveira Florindo.

The use, study, adaptation and sharing of this code are allowed, as long as proper credit is given to the author. This project is made available for educational, academic and research purposes.
