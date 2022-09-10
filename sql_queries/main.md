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
