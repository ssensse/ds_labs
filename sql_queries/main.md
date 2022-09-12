# SQL запросы

База данных с которой я работал содержит информацию о венчурных фондах и инвестияциях в стартапы. 

Ниже приведена её ER-диаграмма:
![](Image.png)

В этом проекте будут несколько запросов, с используемыми в них различных функций.

## Агрегирующие функции. Группировка и сортировка данных.

**Задание.** \
Выгрузите таблицу с десятью самыми активными инвестирующими странами. Активность страны определите по среднему количеству компаний, в которые инвестируют фонды этой страны.

Для каждой страны посчитайте минимальное, максимальное и среднее число компаний, в которые инвестировали фонды, основанные с 2010 по 2012 год включительно.

Исключите из таблицы страны с фондами, у которых минимальное число компаний, получивших инвестиции, равно нулю. Отсортируйте таблицу по среднему количеству компаний от большего к меньшему, а затем по коду страны в лексикографическом порядке.

```sql
SELECT country_code,
       MAX(invested_companies),
       MIN(invested_companies),
       AVG(invested_companies)
FROM fund
WHERE EXTRACT(YEAR FROM founded_at) BETWEEN 2010 AND 2012
GROUP BY country_code
HAVING MIN(invested_companies) <> 0
ORDER BY AVG(invested_companies) DESC
LIMIT 10
```
Вывод получился в следующем формате:

|country_code	| max	| min	| avg |
|:-----------:|----:|----:|----:|
|BGR|35| 25|30 |
|CHL|29| 29| 29|
|UKR|10|8  |	9|
|LTU|	5|	5|	5|
|IRL|	5|	4|4.5|
|KEN|	3|	3|	3|

## Подзапросы и временные запросы. Объединение таблиц

**Задание.** <br>
Выведите среднее число учебных заведений (всех, не только уникальных), которые окончили сотрудники Facebook.

```sql
WITH 
  tb AS (SELECT DISTINCT co.id as co_id
         FROM company as co
         JOIN funding_round as fr ON co.id = fr.company_id
         WHERE co.name = 'Facebook'),
  tb2 AS (SELECT people.id,
                 COUNT(e.instituition) as inst
          FROM people
          JOIN education as e ON people.id = e.person_id
          GROUP BY people.id),
  tb3 AS (SELECT DISTINCT people.id,
                 tb2.inst
          FROM people
          JOIN tb ON tb.co_id = people.company_id
          JOIN tb2 ON tb2.id = people.id
          JOIN education as e ON e.person_id = people.id)

SELECT AVG(inst)
FROM tb3
```
|avg|
|:-:|
|1.51111|

**Задание.** <br>
Составьте сводную таблицу и выведите среднюю сумму инвестиций для стран, в которых есть стартапы, зарегистрированные в 2011, 2012 и 2013 годах. 

Данные за каждый год должны быть в отдельном поле. 

Отсортируйте таблицу по среднему значению инвестиций за 2011 год от большего к меньшему.

```sql
WITH
     inv_2011 AS (SELECT country_code,
				         AVG(funding_total) AS year_2011
				  FROM company
				  WHERE EXTRACT(YEAR FROM founded_at) = 2011
				  GROUP BY country_code),
	 inv_2012 AS (SELECT country_code,
				         AVG(funding_total) AS year_2012
				  FROM company
				  WHERE EXTRACT(YEAR FROM founded_at) = 2012
				  GROUP BY country_code),
	 inv_2013 AS (SELECT country_code,
				         AVG(funding_total) AS year_2013
				  FROM company
				  WHERE EXTRACT(YEAR FROM founded_at) = 2013
				  GROUP BY country_code)	
SELECT inv_2011.country_code,
       inv_2011.year_2011,
	   inv_2012.year_2012,
	   inv_2013.year_2013
FROM inv_2011 
INNER JOIN inv_2012 ON inv_2011.country_code = inv_2012.country_code
INNER JOIN inv_2013 ON inv_2012.country_code = inv_2013.country_code
ORDER BY inv_2011.year_2011 DESC
```
На выходе получили:

|country_code	|year_2011	|year_2012	|year_2013|
|:---|:---|:---|:---|
|PER	|4e+06	|41000	|25000|
|USA	|2.24396e+06	|1.20671e+06	|1.09336e+06|
|HKG	|2.18078e+06	|226227	|0|
|PHL	|1.75e+06	|4218.75	|2500|
|ARE	|1.718e+06	|197222	|35333.3|
|JPN	|1.66431e+06	|674720	|50000|