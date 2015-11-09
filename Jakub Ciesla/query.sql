
--create features: user_id, first_week, first_month

DROP TABLE features;

CREATE TABLE features(user_id int, first_week int, first_month);

INSERT into features (user_id, 0) (
	SELECT user_id FROM users 
);

--first week purchases in $
UPDATE features SET
    first_week = subquery.first_week
FROM (
     SELECT u.user_id, SUM(c.quantity*c.price) as first_week from conversions c RIGHT JOIN users u ON c.user_id = u.user_id WHERE c.conv_time::date - u.register_time::date <= 7 AND c.conv_time::date - u.register_time::date >= 0 GROUP BY u.user_id
) AS subquery
WHERE features.user_id = subquery.user_id;

UPDATE features
SET first_week = 0
WHERE first_week is null;

--first months purchases in $
UPDATE features SET
    first_month = subquery.first_month
FROM (
     SELECT u.user_id, SUM(c.quantity*c.price) as first_month from conversions c RIGHT JOIN users u ON c.user_id = u.user_id WHERE c.conv_time::date - u.register_time::date <= 30 AND c.conv_time::date - u.register_time::date >= 0 GROUP BY u.user_id
) AS subquery
WHERE features.user_id = subquery.user_id;

UPDATE features
SET first_month = 0
WHERE first_month is null;

--first week items
ALTER TABLE features ADD COLUMN items int;

UPDATE features SET
    items = subquery.items
FROM (
     SELECT B.user_id, COUNT(B.user_id)as items from conversions A LEFT JOIN users B ON A.user_id = B.user_id WHERE A.conv_time::date - B.register_time::date <= 7 AND A.conv_time::date - B.register_time::date >= 0 GROUP BY B.user_id
) AS subquery
WHERE features.user_id = subquery.user_id;

UPDATE features
SET items = 0
WHERE items is null;

--first week views
ALTER TABLE features ADD COLUMN views int;

UPDATE features SET
    views = subquery.v
FROM (
     SELECT B.user_id, COUNT(B.user_id) as v from views A LEFT JOIN users B ON A.user_id = B.user_id WHERE A.view_time::date - B.register_time::date <= 7 AND A.view_time::date - B.register_time::date >= 0 GROUP BY B.user_id
) AS subquery
WHERE features.user_id = subquery.user_id;

UPDATE features
SET views = 0
WHERE views is null;

