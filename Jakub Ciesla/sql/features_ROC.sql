CREATE TABLE features_ROC(user_id int, first_week int, first_month int, equal bit);

INSERT into features_ROC (user_id) (
	SELECT user_id FROM users 
);

--first week purchases in $
UPDATE features_ROC SET
    first_week = subquery.first_week
FROM (
     SELECT u.user_id, SUM(c.quantity*c.price) as first_week from conversions c RIGHT JOIN users u ON c.user_id = u.user_id WHERE c.conv_time::date - u.register_time::date <= 7 AND c.conv_time::date - u.register_time::date >= 0 GROUP BY u.user_id
) AS subquery
WHERE features_ROC.user_id = subquery.user_id;

UPDATE features_ROC
SET first_week = 0
WHERE first_week is null;

--first months purchases in $
UPDATE features_ROC SET
    first_month = subquery.first_month
FROM (
     SELECT u.user_id, SUM(c.quantity*c.price) as first_month from conversions c RIGHT JOIN users u ON c.user_id = u.user_id WHERE c.conv_time::date - u.register_time::date <= 30 AND c.conv_time::date - u.register_time::date >= 0 GROUP BY u.user_id
) AS subquery
WHERE features_ROC.user_id = subquery.user_id;

UPDATE features_ROC
SET first_month = 0
WHERE first_month is null;

--first_week == first_month
UPDATE features_ROC SET
    equal = CAST(CASE WHEN first_week = first_month THEN 1 ELSE 0 END AS BIT);

--first week items
ALTER TABLE features_ROC ADD COLUMN items int;

UPDATE features_ROC SET
    items = subquery.items
FROM (
     SELECT B.user_id, COUNT(B.user_id)as items from conversions A LEFT JOIN users B ON A.user_id = B.user_id WHERE A.conv_time::date - B.register_time::date <= 7 AND A.conv_time::date - B.register_time::date >= 0 GROUP BY B.user_id
) AS subquery
WHERE features_ROC.user_id = subquery.user_id;

UPDATE features_ROC
SET items = 0
WHERE items is null;

--first week views
ALTER TABLE features_ROC ADD COLUMN views int;

UPDATE features_ROC SET
    views = subquery.v
FROM (
     SELECT B.user_id, COUNT(B.user_id) as v from views A LEFT JOIN users B ON A.user_id = B.user_id WHERE A.view_time::date - B.register_time::date <= 7 AND A.view_time::date - B.register_time::date >= 0 GROUP BY B.user_id
) AS subquery
WHERE features_ROC.user_id = subquery.user_id;

UPDATE features_ROC
SET views = 0
WHERE views is null;

--first week collection views
ALTER TABLE features_ROC ADD COLUMN collection_views int;

UPDATE features_ROC SET
    collection_views = subquery.v
FROM (
     SELECT B.user_id, COUNT(B.user_id) as v from views A LEFT JOIN users B ON A.user_id = B.user_id WHERE A.pagetype = 'Collection' AND A.view_time::date - B.register_time::date <= 7 AND A.view_time::date - B.register_time::date >= 0 GROUP BY B.user_id
) AS subquery
WHERE features_ROC.user_id = subquery.user_id;

UPDATE features_ROC
SET collection_views = 0
WHERE collection_views is null;

--first week product views 
ALTER TABLE features_ROC ADD COLUMN product_views int;

UPDATE features_ROC SET
    product_views = subquery.v
FROM (
     SELECT B.user_id, COUNT(B.user_id) as v from views A LEFT JOIN users B ON A.user_id = B.user_id WHERE A.pagetype = 'Product' AND A.view_time::date - B.register_time::date <= 7 AND A.view_time::date - B.register_time::date >= 0 GROUP BY B.user_id
) AS subquery
WHERE features_ROC.user_id = subquery.user_id;

UPDATE features_ROC
SET product_views = 0
WHERE product_views is null;

--country
ALTER TABLE features_ROC ADD COLUMN country int;

create function h_int(text) returns int as $$
 select ('x'||substr(md5($1),1,8))::bit(32)::int;
$$ language sql;

UPDATE features_ROC SET
	country = h_int(subquery.v)
FROM (
     SELECT user_id, country as v FROM users
) AS subquery
WHERE features_ROC.user_id = subquery.user_id;

UPDATE features_ROC
SET country = h_int('unknown')
WHERE country is null;

--ads saw before signing up
ALTER TABLE features_ROC ADD COLUMN user_ads int;

UPDATE features_ROC SET
    user_ads = subquery.v
FROM (
     SELECT B.user_id, COUNT(B.user_id) as v from user_ads A LEFT JOIN users B ON A.user_id = B.user_id GROUP BY B.user_id
) AS subquery
WHERE features_ROC.user_id = subquery.user_id;

UPDATE features_ROC
SET user_ads = 0
WHERE user_ads is null;

--create file with features
Copy (Select * From features_ROC) To '/tmp/test_ROC.csv' With CSV;
