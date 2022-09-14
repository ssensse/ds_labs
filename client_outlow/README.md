:question: \
In some reason customers started leaving the company. Who this time? \
I have to build a classification model predicting client outflow from telecom.

:unlock: \
[main.ipynb](https://github.com/ssensse/ClientOutflow/blob/main/client_outlow/main.ipynb) - project itself with code. \
[report.ipynb](https://github.com/ssensse/ClientOutflow/blob/main/client_outlow/report.ipynb) contains more information about data and my methods.

:wrench: \
Which tools did I used?
1. On the data preprocessing I used **pandas** and did some actions with datasets:
    + column names preprocessing
    + data type preprocessing
    + filling NaN values
    + searching for diplicates
    + creating the target feature
2. On the EDA I used libraries: **pandas, seaborn, matplotlib, [phik](https://pypi.org/project/phik/), scikit-learn**. The following steps I made:
    + merging tables by `merge()`
    + outliers/inliers analysis by plotting *histograms*, *boxplots*
    + for encoding features I used `sklearn.preprocessing.OrdinalEncoder()`
    + by *phik* I detected **multicollinearity**
    + settled up class disbalance by **upsampling**
3. I used the following models: **RandomForest, LightGBM, Keras**. 
    + hyperparameters were found by **OptunaSearchCV**
    + the models were tested on a validation sample
    + we took **feature importances** from the best model
4. In the final step I made testing and build *roc_auc curve*

*ROC-AUC = 0.908*
