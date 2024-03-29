:question: \
По какой-то причине клиенты стали уходить из телекомпании, кто уйдет в этот раз? <br> 
У нас есть персональные данные клиента, данные о договоре и тарифах. \
Я должен построить и обучить модель, прогнощирующую отток клиентов.

:unlock: \
[main.ipynb](https://github.com/ssensse/training_projects/blob/main/Client%20outflow/main.ipynb) - сам проект с кодом. \
[report.ipynb](https://github.com/ssensse/training_projects/blob/main/Client%20outflow/report.ipynb) содержит отчет по проекту.

:wrench: \
Какие инструменты были использованы?
1. На этапе предобработки данных я использовал **pandas** и сделал следующее:
    + обработка названий столбцов
    + обработка типов столбцов
    + заполнение пропусков
    + поиск дубликатов
    + формирование целеовго признака
2. На EDA я использовал: **pandas, seaborn, matplotlib, [phik](https://pypi.org/project/phik/), scikit-learn**. Предпринял следующие шаги:
    + объединение таблиц методом `merge()`
    + выявление выбросов и аномальных значений графиками *гистограмм*, *ящиков с усами*
    + для кодировки признаков использовал `sklearn.preprocessing.OrdinalEncoder()`
    + библиотекой *phik* обнаружил **мультиколлинеарность**
    + устранил дисбаланс классов методом **upsampling**
3. На этапе построения и обучения моделей я использовал следующие модели: **RandomForest, LightGBM, Keras**. 
    + гиперпараметры были подобраны инструментом **OptunaSearchCV**
    + тестирование проводилось на валидационной выборке
    + построили график **важности признаков** по наиболее точной модели
4. Провели тестирование и построили график *roc_auc кривой*

*ROC-AUC = 0.908*
