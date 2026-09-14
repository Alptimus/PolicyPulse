# PolicyPulse: RBI Repo Shocks and Nifty Volatility Regimes

## Abstract

This project examines the relationship between RBI repo-rate changes and Nifty 50 volatility over the period 2012–2025. The analysis combines monthly macro-financial data construction, exploratory correlation analysis, event-study methodology around MPC decisions, walk-forward validation for regime prediction, and GJR-GARCH modeling for daily return volatility. The objective is to determine whether repo-rate changes are informative about market volatility regimes and whether they can improve short-horizon prediction relative to simple baseline models. The results indicate that repo-rate changes are moderately inversely correlated with subsequent volatility, that cuts and hikes are associated with distinct abnormal volatility patterns, and that volatility forecasting is dominated by persistence rather than policy variables. Walk-forward validation shows that naive autoregressive persistence outperforms Logistic Regression and Random Forest classifiers, while GJR-GARCH confirms strong volatility clustering, asymmetry, and heavy tails. Overall, the evidence suggests that RBI policy is more useful for regime interpretation than for precise short-term forecasting.

## 1. Introduction

Monetary policy plays a central role in shaping financial market expectations, liquidity conditions, and risk appetite. In India, the RBI repo rate is the main policy instrument used to influence borrowing costs, inflation control, and broader economic conditions. Since equity markets absorb both the direct policy move and the underlying macroeconomic signal, changes in the repo rate may affect Nifty 50 returns, volatility, and regime behavior.

The present study investigates whether RBI repo-rate changes are associated with shifts in Nifty 50 volatility and whether these policy changes can be used to predict short-horizon market behavior. Rather than attempting to forecast the exact level of the index, the project focuses on volatility regimes, which is a more realistic objective for a small macro-financial dataset. The study is designed as a benchmark analysis using exploratory statistics, event-study methods, predictive modeling, and volatility modeling.

## 2. Benchmark Design and Data Construction

The benchmark dataset is constructed by combining RBI<sup>[[1](https://data.rbi.org.in/#/dbie/home)]</sup> repo-rate data with daily Nifty 50 market data. In the data-preparation pipeline, the RBI series is loaded from `data/rbi_rates.csv`, the “Effective Date” column is converted to datetime format, and the repo-rate series is sorted chronologically. The repo-rate data is then resampled to month-end frequency using forward fill so that each month reflects the active policy rate at the end of that month. In parallel, daily Nifty 50 closing prices are downloaded using `yfinance`<sup>[[2](https://github.com/ranaroussi/yfinance)]</sup>, daily log returns are computed, and monthly realized volatility is calculated from daily returns. The monthly RBI and Nifty series are then merged on year-month to create the final master dataset. 

This benchmark design supports three complementary tasks. First, it allows exploratory analysis of the relationship between repo-rate changes and realized volatility. Second, it supports an event-study framework around MPC decisions. Third, it provides a dataset for walk-forward classification and regression benchmarks. The main limitation is that the analysis is constrained by monthly frequency, which reduces the sample size and makes precise forecasting more difficult.

## 3. Proposed Methodology

The methodology consists of four steps.

First, exploratory analysis is used to examine the broad relationship between repo-rate changes and Nifty volatility. Correlation is computed using rate changes rather than rate levels, since level correlations can be misleading in macro-financial settings.

Second, an event-study approach is applied around MPC announcements. The aim is to measure abnormal volatility before and after policy events, with separate treatment for hikes and cuts.

Third, predictive benchmarks are evaluated using walk-forward validation. A naive autoregressive baseline is compared with Logistic Regression and Random Forest classification models to determine whether policy-related features improve regime prediction. A similar benchmark is used for volatility forecasting.

Fourth, a GJR-GARCH model is fitted to daily Nifty returns to capture time-varying volatility, asymmetry, persistence, and fat-tailed behavior. This is a more suitable framework than standard regression for modeling financial return variance.

Because macro controls such as CPI inflation, crude oil, and USD/INR are not included, the results should be interpreted as policy-volatility evidence rather than a full causal macroeconomic model.

## 4. Experiments, Results & Discussion

### 4.1 Exploratory Relationship Between Repo-Rate Changes and Volatility

The initial analysis measures the correlation between repo-rate changes and realized volatility. The observed correlation is -0.3084, indicating a moderate inverse relationship.

Table 1. Correlation Between Repo-Rate Changes and Volatility

| Measure                                 |   Value |
| --------------------------------------- | ------: |
| Correlation (Repo Change vs Volatility) | -0.3084 |

This result suggests that larger tightening moves are associated with lower forward volatility in the sample. The interpretation is not strictly causal; rather, it indicates that volatility tends to be lower in periods following tightening cycles or that tightening occurs after uncertainty has already started to normalize. The result is therefore more consistent with a regime-based relationship than with a direct one-step transmission effect.

### 4.2 Event-Study Analysis Around MPC Decisions

To understand short-run market responses to policy actions, abnormal volatility is measured around MPC events. The analysis compares pre-event and post-event abnormal volatility separately for cuts and hikes.

Table 2. Abnormal Volatility Around MPC Events (Annualized)

| Regime | Pre_Abnormal | Post_Abnormal |
| ------ | -----------: | ------------: |
| Cut    |     0.035796 |     -0.002555 |
| Hike   |    -0.025718 |     -0.027988 |

The event-study results show distinct behavior across policy regimes. Cuts are associated with elevated pre-event abnormal volatility followed by normalization after the event. Hikes, on the other hand, are associated with negative abnormal volatility both before and after the event. This suggests that cuts tend to occur during more stressed periods, while hikes are associated with a comparatively calmer volatility regime.

The correct interpretation is not that hikes mechanically reduce volatility, but that policy regimes and volatility conditions are jointly structured. In other words, repo-rate decisions appear to be informative about the volatility environment, even if they do not produce a simple one-directional effect.

### 4.3 Walk-Forward Validation for Regime Prediction

A walk-forward validation design is used to evaluate whether the current volatility regime can predict the next regime. This procedure respects the temporal ordering of the data and is therefore more appropriate than random train-test splitting for financial time series.

Table 3. Walk-Forward Classification Results

| Model                         | Average Accuracy | Average F1-Score |
| ----------------------------- | ---------------: | ---------------: |
| Naive Autoregressive Baseline |           0.7040 |           0.6564 |
| Logistic Regression           |           0.5440 |           0.5053 |
| Random Forest Classifier      |           0.4400 |           0.4033 |

The naive autoregressive baseline substantially outperforms the machine learning models. This indicates that the volatility regime is highly persistent and that the current regime already contains most of the information needed to predict the next regime. In other words, regime continuation is a stronger signal than the policy-related features included in the model. This is a useful finding because it shows that short-horizon market behavior is dominated by persistence rather than by a complex predictive relationship with repo-rate variables.

### 4.4 Volatility Forecasting and Feature Importance

A regression benchmark is also used to predict next-period realized volatility. The naive baseline is compared with a Random Forest regressor.

Table 4. Volatility Forecasting Performance

| Model                   |      MAE |      R² |
| ----------------------- | -------: | ------: |
| Naive Baseline          | 0.012536 | -0.7531 |
| Random Forest Regressor | 0.011661 | -0.2765 |

The Random Forest slightly improves mean absolute error but still produces a negative R². This means the model does not explain volatility variation well enough to outperform a simple benchmark. The feature importance profile explains why.

Table 5. Feature Importance in Volatility Forecasting

| Feature     | Importance |
| ----------- | ---------: |
| Volatility  |   0.771233 |
| Repo        |   0.174859 |
| Repo_Change |   0.053907 |

Lagged volatility dominates the model, accounting for most of the predictive power. This confirms volatility clustering, one of the core stylized facts of financial markets. Repo-rate level and repo-rate change contribute some explanatory power, but their marginal impact is relatively small. The regression results therefore reinforce the conclusion that policy variables matter, but the short-horizon volatility process is largely driven by its own recent history.

### 4.5 GJR-GARCH Analysis of Daily Returns

To better capture the conditional variance process, a GJR-GARCH model is estimated on daily Nifty returns. This is an appropriate choice for financial data because it allows for asymmetric volatility responses and fat-tailed distributions.

Table 6. GJR-GARCH Parameter Estimates

| Parameter |   Estimate | Interpretation              |
| --------- | ---------: | --------------------------- |
| mu        |     0.0546 | Mean return                 |
| omega     |     0.0232 | Long-run variance component |
| alpha[1]  | 0.00058796 | Short-run shock effect      |
| gamma[1]  |     0.1265 | Asymmetry / leverage effect |
| beta[1]   |     0.9083 | Volatility persistence      |
| nu        |     7.6089 | Heavy-tailed distribution   |

The GJR-GARCH results provide strong evidence of persistent and asymmetric volatility dynamics. The high value of beta[1] implies that volatility shocks decay slowly over time, which is characteristic of financial return series. The significant positive gamma[1] indicates an asymmetry or leverage effect, meaning that negative shocks have a larger impact on future volatility than positive shocks of comparable magnitude. The degrees of freedom parameter also indicates heavy tails, which is consistent with equity return distributions.

This model is the strongest technical result in the study because it confirms that the Nifty return process is not homoskedastic and is better understood through a volatility-clustering framework.

### 4.6 Summary of Findings

The empirical evidence leads to a consistent interpretation. RBI repo-rate changes are associated with meaningful shifts in Nifty volatility regimes, but the relationship is not strong enough to support exact short-horizon prediction using standard machine learning models. The event-study analysis reveals distinct abnormal volatility patterns around cuts and hikes, while walk-forward validation shows that simple regime persistence outperforms Logistic Regression and Random Forest. The GJR-GARCH model further confirms that Nifty returns exhibit clustering, asymmetry, and heavy tails.

Overall, RBI policy is more informative as a regime-level indicator than as a precise forecasting variable. That makes the project valuable as a macro-financial analysis of policy and volatility, even though it does not produce a highly predictive model.

## 5. Conclusion

This project investigated the relationship between RBI repo-rate changes and Nifty 50 volatility using exploratory analysis, event studies, predictive benchmarks, and GJR-GARCH modeling. The findings show that repo-rate changes are moderately inversely related to volatility and that cuts and hikes are associated with different abnormal volatility patterns. However, standard machine learning models do not outperform a naive persistence baseline, suggesting that short-horizon regime behavior is highly stable and difficult to predict from policy variables alone.

The GJR-GARCH results provide the strongest quantitative support for the study by demonstrating volatility clustering, asymmetry, and fat-tailed return behavior. Taken together, the results suggest that RBI policy is useful for understanding volatility regimes, but not for exact short-term prediction. This makes the project a strong macro-financial benchmark study with realistic and defensible conclusions.

## References

[1] RBI official data portal for repo rates and other macroeconomic indicators - [Database on Indian Economy (DBIE)](https://data.rbi.org.in/#/dbie/home)  
[2] Yahoo Finance API for Nifty 50 historical data - [yfinance GitHub repository](https://github.com/ranaroussi/yfinance)