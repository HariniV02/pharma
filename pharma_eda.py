import pandas as pd 
import matplotlib as mp
import pandas as pd
import seaborn as sb

# reading combined csv file 
combined = pd.read_csv('pharma_combined.csv')

# dropping duplicate columns 
combined = combined.drop(columns=['state_id:1', 'payment_id:1'])

# % is messing with data - dropping it 
combined['sales_tax_rate'] = combined['sales_tax_rate'].str.replace('%', '').astype(float) / 100
    #float converts it back to a number, 100 included since it was multiplied when cleaning it up 

# converting order_date to date
combined['order_date'] = pd.to_datetime(combined['order_date'], errors='coerce')
    # some invalid dates are still in the dataset - coerce makes them null and ignores 

# testing 
print(combined.shape)
print(combined.dtypes)
print(combined.head())

