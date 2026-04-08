CREATE TABLE pharma_combined AS
SELECT *
FROM orders_messy o
JOIN states_messy s ON o.state_id = s.state_id
JOIN payments_messy p ON o.payment_id = p.payment_id;

