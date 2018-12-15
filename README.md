# MF803_proj_Barra
> In recent years the investment management industry has adjusted to continuing changes—theoretical advances, technological developments, and market growth. To address these challenges, investment managers and ﬁnancial institutions require the most advanced and powerful analytical tools available.  
> Mean-variance analysis has always been an effective way to construct and analyze portfolios. One direct way is to estimate the mean and variance of each asset with historic data. However, for large portfolios, it becomes computationally costly to estimate all the parameters. 
Multi-factor model helps us significantly reduce the dimension of our covariance matrix. Multiple-factor models (MFMs) are formal statements about the relationships among security returns in a portfolio. The basic premise of MFMs is that similar stocks should display similar returns. When we attribute source of risks and returns to several common factors, we do not need to estimate pairwise behavior between stocks, but the just the common factor instead. Afterwards, we use factor covariance to estimate stock covariance. Before building a factor model, we need to define our factors. Here we reference MSCI Barra factors. The factors are mainly constructed from fundamental stock data.  

# In this repo
> To fulfill the implementation goal for our MFMs, we separate the procedure into three phases.
* `prep` is the part for **Phase I: Data Aggregate and Factor Construction**
> Phase I defines data structure for the project and calculates factor loadings.
* `regr_app` is the part for **Phase II: Factor Return Estimation** and **Phase III: Analysis**
> Phase II & III complete the project by doing regression of stock returns on factor loadings, then, derive the results of MFMs for portfolio construction and analysis.
