1. number_of_new_users_per_month():
Displays a number of registrations per month.
Data:
-Table Users; Columns: 'signupTime', 'userId'.
Properties:
-dropped 'Nan' and 'None' values from 'signupTime' in Users.
Actions:
-performing count() operation on 'userId', grouped by year and month in 'signupTime',
-sorting 'signupTime' by year and month.
Axes:
-x: year and month of registration,
-y: number of regsitrations.

2. number_of_conversions_per_month():
Data:
-Table Conversions; Columns: 'timestamp'.
Properties:
-dropped 'Nan' and 'None' values from 'timestamp' in Conversions.
Actions:
-performing count() operation on rows grouped by year and month,
-sorting 'timestamp' by year and month.
Axes:
-x: year and month of conversion,
-y: number of conversions.

3. number_of_items_purchased_per_month():
Data:
-Table Conversions; Columns: 'timestamp', 'quantity'.
Properties:
-dropped 'Nan' and 'None' values from 'timestamp' and 'quantity' in Conversions.
Actions:
-performing sum() operation on 'quantity', grouped by year and month of conversion,
-sorting 'timestamp' by year and month.
Axes:
-x: year and month of conversion,
-y: number of purchased items.

4. income_per_month():
Data:
-Table Conversions; Columns: 'timestamp', 'price'.
Properties:
-dropped 'Nan' and 'None' values from 'timestamp' and 'price' in Conversions.
Actions:
-performing sum() operation on 'price', grouped by year and month of conversion,
-sorting 'timestamp' by year and month.
Axes:
-x: year and month of conversion,
-y: income.

5. number_of_items_purchased_per_user_in_the_first_week_after_sign_in():
Data:
-Table Conversions; Columns: 'timestamp', 'userId', 'quantity',
-Table Users; Columns: 'signupTime', 'userId'
Properties:
-dropped 'Nan' and 'None' values from 'timestamp', 'userId', 'quantity' in Conversions,
-dropped 'Nan' and 'None' values from 'signupTime', 'userId' in Users,
Actions:
-joining Conversions and Users on 'userId',
-adding additional column to joined structure: 'week_after' - date week after signing in,
-filter 'timestamp' - rows only with 'timestamp' <= 'week_after' preserved,
-performing sum() operation on 'quantity', grouped by 'userId'.
Axes:
-x: user id,
-y: quantity of purchased products.

6. number_of_items_purchased_from_particular_category_grouped_by_country():
Data:
-Table Conversions; Columns: 'itemId', 'userId', 'quantity',
-Table Items; Columns: 'itemId', 'category',
-Table Users; Columns: 'userId', 'registerCountry'.
Properties:
-dropped 'Nan' and 'None' values from 'category' in Items,
-dropped 'Nan' and 'None' values from 'quantity' in Conversions,
-dropped 'Nan' and 'None' values from 'registerCountry' in Users.
Actions:
-joining items and conversions on 'itemId' and futher with users on 'userId',
-filtering joined data on 'category' property,
-performing sum on 'quantity' in rows grouped by 'registerCountry'.
Axes:
-x: country,
-y: number of purchased items.



 - Displays number of items from particular category purchased by people from all countries.
7. number_of_items_purchased_in_particular_country_grouped_by_category(country) - Displays number of items from all cattegories purchased in particular country.
8. number_of_purchased_items_grouped_by_categories_in_all_countries() - Displays general view on sum of purchased items grouped by country and category.
