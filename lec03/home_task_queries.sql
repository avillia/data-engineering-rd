/*
 Завдання на SQL до лекції 03.
 */


/*
1.
Вивести кількість фільмів в кожній категорії.
Результат відсортувати за спаданням.
*/

SELECT
    COUNT(film_category.film_id) as amount_of_films,
    category.name AS category_name
FROM film_category
JOIN public.category on film_category.category_id = category.category_id
GROUP BY category.name
ORDER BY amount_of_films DESC;

/*
2.
Вивести 10 акторів, чиї фільми брали на прокат найбільше.
Результат відсортувати за спаданням.
*/

SELECT
    actor.first_name,
    actor.last_name,
    COUNT(rental.inventory_id) as amount
FROM inventory
JOIN rental ON inventory.inventory_id = rental.inventory_id
JOIN film_actor ON film_actor.film_id = inventory.film_id
JOIN actor on film_actor.actor_id = actor.actor_id
GROUP BY actor.actor_id
ORDER BY amount DESC
LIMIT 10;

/*
3.
Вивести категорія фільмів, на яку було витрачено найбільше грошей
в прокаті
*/
-- SQL code goes here...



/*
4.
Вивести назви фільмів, яких не має в inventory.
Запит має бути без оператора IN
*/
-- SQL code goes here...


/*
5.
Вивести топ 3 актори, які найбільше зʼявлялись в категорії фільмів “Children”.
*/
-- SQL code goes here...
