❓ Чтобы привлечь больше водителей во время пиковой нагрузки, необходимо спрогнозировать количество заказов такси на следующий час. \
В нашем распоряжении временной ряд заказов такси за каждые 10 минут начиная с *01.03.2018* по *31.08.2018*.
Задача: построить регрессионную модель, прогнозирующую количество заказов такси на следующий час.

🔓:
[main.ipynb](https://github.com/ssensse/training_projects/blob/main/Taxi%20forecast/main.ipynb) - проект с кодом.

🔧 План проекта и какие инструменты были использованы.

1. Загрузка и подготовка данных.
    * ряд был проверен на монотонность и заресемплен до одного часа
2. Анализ временного ряда. 
    * ряд был проверен на стационарность **тестом Дики-Фулера**. *p-value = 0.0289* - ряд не стационарен - преобразование не потребовалось
    * инструментом декомпозиции был выявлен положительный линейный **тренд**, а также **сезонность** по часам и дням недели
3. Обучение моделей.
    * написали функцию по созданию признаков для обучения: календарных, отстающих значений, скользящего среднего
    * были использованы такие модели как: *LinearRegression, RandomForest, CatBoost, LightGBM*
    * циклом подбирались параметры **наилучшего набора признаков**, параллельно с этим модели учились на каждой из них и в итоге отбирался наилучший набор для каждой модели.
    * среди всех моделей была выбрана линейная регрессия как наименее переобученная, быстрая и с хорошей точностью
4. Тестирование. 
    * ***RMSE = 41.5***

![download](https://user-images.githubusercontent.com/102548885/193137824-a96112e9-a5a2-4a74-b0aa-b5aaaba86d65.png)
