-- replacing empty values w Null 
select * from orders_messy 
where order_id is NULL 
OR payment_id is NULL 
OR state_id is NULL 
OR drug is NULL 
OR quantity is NULL 
OR unit_price_usd is NULL 
OR order_date is NULL 
OR order_status is NULL 


-- cleaning drug column 

SELECT DISTINCT drug, COUNT(*) as count 
FROM orders_messy 
WHERE drug IS NOT NULL
GROUP BY drug
ORDER BY drug;
-- Lisinopril 
UPDATE orders_messy SET drug = 'Lisinopril 10mg'
WHERE LOWER(REPLACE(drug, ' ', '')) LIKE '%lisinop%';
-- Atorvastatin
UPDATE orders_messy SET drug = 'Atorvastatin 20mg'
WHERE LOWER(REPLACE(drug, ' ', '')) LIKE '%atorva%';
-- Metformin
UPDATE orders_messy SET drug = 'Metformin 500mg'
WHERE LOWER(REPLACE(drug, ' ', '')) LIKE '%metfor%';
-- Albuterol
UPDATE orders_messy SET drug = 'Albuterol Inhaler'
WHERE LOWER(REPLACE(drug, ' ', '')) LIKE '%albut%';
-- Sertraline
UPDATE orders_messy SET drug = 'Sertraline 50mg'
WHERE LOWER(REPLACE(drug, ' ', '')) LIKE '%sertra%';
-- leading spaces 
UPDATE orders_messy SET drug = TRIM(drug) WHERE drug IS NOT NULL;



-- cleaning up date column 
SELECT DISTINCT order_date FROM orders_messy
WHERE order_date IS NOT NULL
ORDER BY order_date;

UPDATE orders_messy
SET order_date = CASE
    -- MM/DD/YYYY → e.g. 10/31/2024
    WHEN order_date LIKE '__/__/____' 
    THEN SUBSTR(order_date,7,4)||'-'||SUBSTR(order_date,1,2)||'-'||SUBSTR(order_date,4,2)
    -- (7,4) - year starts in the 7th position and has 4 characters 
    -- (1,2) - month starts in the 1st position and has 2 characters
    -- (4,2) - day starts in the 4th positin and has 2 characters 
    -- the '-' in between replaces the / w -
    -- DD-MM-YYYY → e.g. 31-10-2024
    WHEN order_date LIKE '__-__-____'
    THEN SUBSTR(order_date,7,4)||'-'||SUBSTR(order_date,4,2)||'-'||SUBSTR(order_date,1,2)
    -- same as above, switching month and date 
    -- YYYY/MM/DD → e.g. 2024/10/31
    WHEN order_date LIKE '____/__/__'
    THEN REPLACE(order_date, '/', '-')
    -- replacing / w - 
    -- Mon DD YYYY → e.g. Oct 31 2024
    WHEN order_date LIKE '___  __  ____' OR order_date LIKE '___ __ ____'
    THEN SUBSTR(order_date,8,4)||'-'||
         CASE SUBSTR(order_date,1,3)
             WHEN 'Jan' THEN '01' WHEN 'Feb' THEN '02' WHEN 'Mar' THEN '03'
             WHEN 'Apr' THEN '04' WHEN 'May' THEN '05' WHEN 'Jun' THEN '06'
             WHEN 'Jul' THEN '07' WHEN 'Aug' THEN '08' WHEN 'Sep' THEN '09'
             WHEN 'Oct' THEN '10' WHEN 'Nov' THEN '11' WHEN 'Dec' THEN '12'
         END||'-'||SUBSTR(order_date,5,2)
     -- when it is spelled out instead of numbers, year is in 8th, 4 chars long , case within is saying which month is what number 
    -- DD Month YYYY → e.g. 31 October 2024
    WHEN order_date LIKE '__ % ____'
    THEN SUBSTR(order_date, LENGTH(order_date)-3, 4)||'-'||
         CASE 
             WHEN order_date LIKE '%January%'   THEN '01'
             WHEN order_date LIKE '%February%'  THEN '02'
             WHEN order_date LIKE '%March%'     THEN '03'
             WHEN order_date LIKE '%April%'     THEN '04'
             WHEN order_date LIKE '%May%'       THEN '05'
             WHEN order_date LIKE '%June%'      THEN '06'
             WHEN order_date LIKE '%July%'      THEN '07'
             WHEN order_date LIKE '%August%'    THEN '08'
             WHEN order_date LIKE '%September%' THEN '09'
             WHEN order_date LIKE '%October%'   THEN '10'
             WHEN order_date LIKE '%November%'  THEN '11'
             WHEN order_date LIKE '%December%'  THEN '12'
         END||'-'||SUBSTR(order_date,1,2)
        -- same logic, different order
    -- Already YYYY-MM-DD, leave it alone
    ELSE order_date
END
WHERE order_date IS NOT NULL;

-- orderstatus 
select distinct order_status 
from orders_messy 
where order_status is not NULL 

UPDATE orders_messy SET order_status = TRIM(order_status) WHERE drug IS NOT NULL;

UPDATE orders_messy
SET order_status = UPPER(SUBSTR(order_status, 1, 1)) || LOWER(SUBSTR(order_status, 2)) -- changing it from all upper to first upper, rest lower 
-- (os, 1, 1) - first character, length of 1 
-- (os, 2) - second character, specific length not needed
WHERE order_status IS NOT NULL;

UPDATE orders_messy SET order_status = 'Processing'
WHERE LOWER(order_status) LIKE '%procesing%'; -- adding lower make clause case-blind

UPDATE orders_messy SET order_status = 'Shipped'
WHERE LOWER(order_status) LIKE '%shiped%';

UPDATE orders_messy SET order_status = 'Completed'
WHERE LOWER(order_status) LIKE '%completd%' OR LOWER(order_status) LIKE '%complete%';

UPDATE orders_messy SET order_status = 'Refunded'
WHERE LOWER(order_status) LIKE '%refundd%';

UPDATE orders_messy SET order_status = "Canceled"
WHERE LOWER(order_status) LIKE '%cancelled'; 


-- unit price 

select unit_price_usd 
from orders_messy
where unit_price_usd  is not NULL 


update orders_messy SET unit_price_usd = REPLACE(unit_price_usd, '$', '') -- removing the $ from any values 
WHERE unit_price_usd LIKE '$%'; -- ensures only the ones w $ 

-- removing neg values 
UPDATE orders_messy
SET unit_price_usd = NULL
WHERE CAST(unit_price_usd AS REAL) < 0; -- the cast as real is needed because its currently a text value but we need to read it as a number before comparing 

SELECT unit_price_usd FROM orders_messy
WHERE CAST(unit_price_usd AS REAL) < 0; -- makes sure statement above worked 


-- quantity 

select quantity from orders_messy 
where cast(quantity AS real) <= 0; 

update orders_messy 
set quantity = NULL
where cast(quantity AS real) <= 0; 


-- order id 
select order_id from orders_messy 
where order_id like '%ORD%' -- finding orders starting w ord 

UPDATE orders_messy
SET order_id = TRIM(REPLACE(order_id, 'ORD-', '')) -- replacing ORD w empty 
WHERE order_id LIKE '%ORD-%';

