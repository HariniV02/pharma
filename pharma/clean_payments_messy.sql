-- replacing empty values w Null 
select * from payments_messy 
where payment_id = '' 
or payment_method = '' 
or processor_network = '' 
or approval_code = '' 
or billing_zip = '' 

	update payments_messy 
	SET payment_id = NULL 
	WHERE payment_id = ''

	update payments_messy 
	SET payment_method = NULL 
	WHERE payment_method = ''

	update payments_messy 
	SET processor_network = NULL 
	WHERE processor_network = ''

	update payments_messy 
	SET approval_code = NULL 
	WHERE approval_code = ''

update payments_messy 
SET billing_zip = NULL 
WHERE billing_zip = ''

select * from payments_messy 
where payment_id is NULL
or payment_method is NULL 
or processor_network is NULL
or approval_code is NULL
or billing_zip is NULL


-- payment_method
select distinct payment_method
from payments_messy

	-- spelling 
	UPDATE payments_messy SET payment_method = 'Insurance'
	WHERE LOWER(payment_method) LIKE '%ins%'; -- adding lower make clause case-blind
	
	-- upper and lowercase 
	UPDATE payments_messy SET payment_method = UPPER(SUBSTR(payment_method, 1, 1)) || LOWER(SUBSTR(payment_method, 2))
	where payment_method is not NULL
	
	-- medicare values 
	SELECT payment_method, LENGTH(payment_method) 
	FROM payments_messy
	WHERE LOWER(TRIM(payment_method)) = 'medicare';
	
	UPDATE payments_messy
	SET payment_method = TRIM(payment_method)
	WHERE payment_method IS NOT NULL;
	
	-- credit card 
	select payment_method 
	from payments_messy 
	where payment_method like '%credit%'
	
	UPDATE payments_messy
	SET payment_method = 'Credit Card' -- sets all variants to one type 
	WHERE LOWER(REPLACE(payment_method, ' ', '')) LIKE '%creditcard%'; -- removes spaces, fixes casing 
	
	
-- billing 
select distinct billing_zip 
from payments_messy

	select distinct billing_zip 
	from payments_messy
	where billing_zip like '%N%' 
	
	UPDATE payments_messy
	SET billing_zip = NULL 
	WHERE billing_zip = 'N/A'
	
	
	



