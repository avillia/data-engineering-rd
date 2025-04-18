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

SELECT
    category.name,
    SUM(payment.amount) as money_spent
FROM payment
JOIN rental ON payment.rental_id = rental.rental_id
JOIN inventory ON inventory.inventory_id = rental.inventory_id
JOIN film on inventory.film_id = film.film_id
JOIN film_category on film.film_id = film_category.film_id
JOIN category on category.category_id = film_category.category_id
GROUP BY category.name
ORDER BY money_spent DESC
LIMIT 1;

/*
4.
Вивести назви фільмів, яких не має в inventory.
Запит має бути без оператора IN
*/

SELECT
    film.title
FROM inventory
RIGHT JOIN film ON film.film_id = inventory.film_id
WHERE inventory.film_id IS NULL
GROUP BY film.film_id;

/*
5.
Вивести топ 3 актори, які найбільше зʼявлялись в категорії фільмів “Children”.
*/
-- SQL code goes here...
