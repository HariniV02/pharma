-- replacing empty values w Null 
select * from states_messy 
where state_id = '' 
or state_abbrev  = '' 
or state_name  = '' 
or sales_tax_rate = '' 
or regulatory_tier  = '' 

	update states_messy 
	SET state_id = NULL 
	WHERE state_id = ''

	update states_messy 
	SET state_abbrev = NULL 
	WHERE state_abbrev = ''

	update states_messy 
	SET state_name = NULL 
	WHERE state_name = ''

	update states_messy 
	SET sales_tax_rate = NULL 
	WHERE sales_tax_rate = ''
	
	update states_messy 
	SET regulatory_tier = NULL 
	WHERE regulatory_tier = ' '
	
	
-- state abbrev 
select distinct state_abbrev from states_messy 
where state_abbrev is not null 

	-- making all uppercase 
	UPDATE states_messy
	SET state_abbrev = UPPER(state_abbrev) -- making current values to uppercase 
	WHERE state_abbrev IS NOT NULL;
	
	-- checking length 
	SELECT state_abbrev, LENGTH(state_abbrev)
	FROM states_messy 
	WHERE state_abbrev IS NOT NULL;
	
	
-- state name 
select distinct state_name from states_messy 
where state_name is not null 
	
	-- make all uppercase
	UPDATE states_messy
	SET state_name = UPPER(SUBSTR(state_name, 1, 1)) || LOWER(SUBSTR(state_name, 2))
	WHERE state_name IS NOT NULL;
	

-- sales tax rate 
select distinct sales_tax_rate  from states_messy 
where sales_tax_rate is not null 

	-- add %
	update states_messy 
	set sales_tax_rate = round(cast(sales_tax_rate as real) * 100 , 1) || '%'
	WHERE sales_tax_rate IS NOT NULL;
	
	-- removing negatives 
	update states_messy 
	set sales_tax_rate = NULL 
	Where cast(sales_tax_rate as real) < 0
	
