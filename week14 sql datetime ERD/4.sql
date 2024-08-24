--1
-- SELECT title , release_year , rental_rate FROM film
-- WHERE release_year=2006 AND rental_rate>=4;

--2
-- SELECT title,length FROM film
-- ORDER BY length ASC
-- LIMIT 10;

--3
-- SELECT country.country, COUNT(customer.customer_id) AS customer_count
-- FROM customer
-- JOIN address ON customer.address_id = address.address_id
-- JOIN city ON address.city_id = city.city_id
-- JOIN country ON city.country_id = country.country_id
-- GROUP BY country.country
-- ORDER BY country.country ASC;

--4
-- SELECT 
-- film.title , 
-- SUM(EXTRACT(DAY FROM COALESCE(rental.return_date, CURRENT_DATE) - rental.rental_date)) AS days_rented,
-- ROUND(AVG(payment.amount), 2) AS average_rate
-- FROM film 
-- JOIN inventory ON film.film_id = inventory.film_id
-- JOIN rental ON inventory.inventory_id = rental.inventory_id
-- JOIN payment ON payment.rental_id = rental.rental_id
-- GROUP BY film.title
-- ORDER BY film.title ASC

--5
-- SELECT 
-- customer.first_name||' '||customer.last_name AS customer_name,
-- COUNT(rental_id) AS rent_times
-- FROM customer
-- JOIN rental ON rental.customer_id=customer.customer_id
-- GROUP BY customer.customer_id
-- ORDER BY rent_times DESC
-- LIMIT 10

--6
-- SELECT customer.customer_id, customer.first_name , country.country
-- FROM customer
-- JOIN address ON customer.address_id = address.address_id
-- JOIN city ON address.city_id = city.city_id
-- JOIN country ON city.country_id = country.country_id
-- WHERE country.country = 'United States' and customer.first_name LIKE 'A%'

--7
-- SELECT title , rental_duration , replacement_cost FROM film
-- WHERE rental_duration>5 AND replacement_cost<15
