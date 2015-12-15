------------------------------------------------------------------
--********************* Cleaning the data ******************------
------------------------------------------------------------------

-- conversions cleaning:
-- here we are removing conversions which happened before user registration
DELETE FROM conversions WHERE (user_id, conv_time) IN ( SELECT c.user_id, c.conv_time FROM conversions c INNER JOIN users u ON c.user_id = u.user_id WHERE c.conv_time < u.register_time);

-- views cleaning
-- here we are removing views which happened before user registration
DELETE FROM views WHERE (user_id, view_time) IN ( SELECT v.user_id, v.view_time FROM views v INNER JOIN users u ON v.use
r_id = u.user_id WHERE v.view_time < u.register_time);

------------------------------------------------------------------
--**************** Dumping features table to csv file ******------
------------------------------------------------------------------
\copy features to './features.csv' WITH DELIMITER '|' NULL '';

------------------------------------------------------------------
--********************* Initialization *********************------
------------------------------------------------------------------

-- lets create a features vector for every user
INSERT INTO features (user_id) SELECT user_id from users;

------------------------------------------------------------------------
--********************* Conversions related features *****************--
------------------------------------------------------------------------

-- results - how much money user spent during the first 30 days after registration
-- features column: y
UPDATE features SET
    y = subquery.y
FROM (
    SELECT c.user_id, SUM(c.quantity*c.price) as y
    FROM conversions c INNER JOIN users u ON c.user_id = u.user_id
    WHERE c.conv_time::date - u.register_time::date <= 30
    GROUP BY c.user_id
) AS subquery
WHERE features.user_id = subquery.user_id;


-- how much money user spent during the first week after registration
-- features column: first_week
UPDATE features SET
    first_week = subquery.first_week
FROM (
     SELECT u.user_id, SUM(c.quantity*c.price) as first_week from conversions c RIGHT JOIN users u ON c.user_id = u.user_id WHERE c.conv_time::date - u.register_time::date <= 7 GROUP BY u.user_id
) AS subquery
WHERE features.user_id = subquery.user_id;


-- the number of conversions made by user during the first week after registration
-- features column: conv_count
UPDATE features SET
    conv_count = subquery.conv_count
FROM (
     SELECT u.user_id, COUNT(*) as conv_count from conversions c RIGHT JOIN users u ON c.user_id = u.user_id WHERE c.conv_time::date - u.register_time::date <= 7 GROUP BY u.user_id
) AS subquery
WHERE features.user_id = subquery.user_id;


-- an average value of conversions done by user
-- features column: avg_conv_price
UPDATE features SET
    avg_conv_price = subquery.avg_conv_price
FROM (
     SELECT u.user_id, AVG(price*quantity) as avg_conv_price from conversions c RIGHT JOIN users u ON c.user_id = u.user_id WHERE c.conv_time::date - u.register_time::date <= 7 GROUP BY u.user_id
) AS subquery
WHERE features.user_id = subquery.user_id;


-- money spent during the first day after registration
-- features column: first_day
UPDATE features SET
    first_day = subquery.first_day
FROM (
     SELECT u.user_id, SUM(c.quantity*c.price) as first_day from conversions c RIGHT JOIN users u ON c.user_id = u.user_id WHERE c.conv_time::date - u.register_time::date <= 1 GROUP BY u.user_id
) AS subquery
WHERE features.user_id = subquery.user_id;

-- average time of conversion (in minutes) - during the day
-- features column: avg_conv_time
UPDATE features SET
    avg_conv_time = subquery.avg_conv_time
FROM
(
SELECT u.user_id, AVG(extract(hours from c.conv_time::time)*60 + extract(minutes from c.conv_time::time)) as avg_conv_time
    FROM conversions c RIGHT JOIN users u ON c.user_id = u.user_id
    WHERE c.conv_time::date - u.register_time::date <= 7
    GROUP BY u.user_id
) AS subquery
WHERE features.user_id = subquery.user_id;

------------------------------------------------------------------
--********************* Views related features *****************--
------------------------------------------------------------------

-- Number of views done by user during the first week
-- features column: views_count
UPDATE features SET
    views_count = subquery.views_count
FROM
(
    SELECT u.user_id, COUNT(*) as views_count
    FROM views v RIGHT JOIN users u on u.user_id = v.user_id
    WHERE v.view_time::date - u.register_time::date <= 7
    GROUP BY u.user_id
) AS subquery
WHERE features.user_id = subquery.user_id;

-- average price of viewed item during the first week after registration
-- features column: avg_view_price
UPDATE features SET
    avg_view_price = subquery.avg_view_price
FROM
(
SELECT u.user_id, AVG(price) as avg_view_price
    FROM (SELECT * from views v INNER JOIN items i ON i.item_id = v.item_id) vi INNER JOIN users u ON u.user_id = vi.user_id
    WHERE vi.view_time::date - u.register_time::date <= 7
    GROUP BY u.user_id
) AS subquery
WHERE features.user_id = subquery.user_id;

-- the number of views of items which where then bought by user
-- during the first week
-- features column: viewed_bought_count
UPDATE features SET
    viewed_bought_count = subquery.viewed_bought_count
FROM
(
SELECT u.user_id, COUNT(*) as viewed_bought_count
    FROM
        (SELECT c.item_id, c.user_id, v.view_time, c.conv_time
            FROM views v INNER JOIN conversions c ON (c.item_id, c.user_id) = (v.item_id, v.user_id)) vi
    INNER JOIN users u ON u.user_id = vi.user_id
    WHERE vi.view_time::date - u.register_time::date <= 7
        AND vi.conv_time::date - u.register_time::date <=7
        AND vi.view_time < vi.conv_time
    GROUP BY u.user_id
) AS subquery
WHERE features.user_id = subquery.user_id;


------------------------------------------------------------------
--********************* users_ads related features *************--
------------------------------------------------------------------

-- 1 - if user has seen any ads before
-- 0 otherwise
-- features column: has_seen_ad
UPDATE features SET
    has_seen_ad = subquery.has_seen_ad
FROM
(
SELECT u.user_id, COUNT(*) has_seen_ad
    FROM users u INNER JOIN user_ads a
    ON u.user_id = a.user_id
    GROUP BY u.user_id
) AS subquery
WHERE features.user_id = subquery.user_id;


------------------------------------------------------------------
--********************* Users related features *************------
------------------------------------------------------------------

-- features columnt: country
UPDATE features SET
    country = subquery.country
FROM
( SELECT user_id, country FROM users ) AS subquery
WHERE features.user_id = subquery.user_id;

-- the day of the year of registration
-- column: regist_day_of_year
UPDATE features SET
    regist_day_of_year = subquery.regist_day_of_year
FROM
( SELECT user_id,
       (30.5 * (extract(month from u.register_time::date) - 1) + extract(day from u.register_time::date))::int
          as regist_day_of_year
    FROM users u
) AS subquery
WHERE features.user_id = subquery.user_id;


-- how much money user spent during the first week after registration
-- features column: first_week
UPDATE features SET
    first_week = subquery.first_week
FROM (
     SELECT u.user_id, SUM(c.quantity*c.price) as first_week from conversions c RIGHT JOIN users u ON c.user_id = u.user_id WHERE c.conv_time::date - u.register_time::date <= 7 GROUP BY u.user_id
) AS subquery
WHERE features.user_id = subquery.user_id;


-- the number of conversions made by user during the first week after registration
-- features column: conv_count
UPDATE features SET
    conv_count = subquery.conv_count
FROM (
     SELECT u.user_id, COUNT(*) as conv_count from conversions c RIGHT JOIN users u ON c.user_id = u.user_id WHERE c.conv_time::date - u.register_time::date <= 7 GROUP BY u.user_id
) AS subquery
WHERE features.user_id = subquery.user_id;


-- an average value of conversions done by user
-- features column: avg_conv_price
UPDATE features SET
    avg_conv_price = subquery.avg_conv_price
FROM (
     SELECT u.user_id, AVG(price*quantity) as avg_conv_price from conversions c RIGHT JOIN users u ON c.user_id = u.user_id WHERE c.conv_time::date - u.register_time::date <= 7 GROUP BY u.user_id
) AS subquery
WHERE features.user_id = subquery.user_id;


-- money spent during the first day after registration
-- features column: first_day
UPDATE features SET
    first_day = subquery.first_day
FROM (
     SELECT u.user_id, SUM(c.quantity*c.price) as first_day from conversions c RIGHT JOIN users u ON c.user_id = u.user_id WHERE c.conv_time::date - u.register_time::date <= 1 GROUP BY u.user_id
) AS subquery
WHERE features.user_id = subquery.user_id;

-- average time of conversion (in minutes) - during the day
-- features column: avg_conv_time
UPDATE features SET
    avg_conv_time = subquery.avg_conv_time
FROM
(
SELECT u.user_id, AVG(extract(hours from c.conv_time::time)*60 + extract(minutes from c.conv_time::time)) as avg_conv_time
    FROM conversions c RIGHT JOIN users u ON c.user_id = u.user_id
    WHERE c.conv_time::date - u.register_time::date <= 7
    GROUP BY u.user_id
) AS subquery
WHERE features.user_id = subquery.user_id;

------------------------------------------------------------------
--********************* Views related features *****************--
------------------------------------------------------------------

-- Number of views done by user during the first week
-- features column: views_count
UPDATE features SET
    views_count = subquery.views_count
FROM
(
    SELECT u.user_id, COUNT(*) as views_count
    FROM views v RIGHT JOIN users u on u.user_id = v.user_id
    WHERE v.view_time::date - u.register_time::date <= 7
    GROUP BY u.user_id
) AS subquery
WHERE features.user_id = subquery.user_id;

-- average price of viewed item during the first week after registration
-- features column: avg_view_price
UPDATE features SET
    avg_view_price = subquery.avg_view_price
FROM
(
SELECT u.user_id, AVG(price) as avg_view_price
    FROM (SELECT * from views v INNER JOIN items i ON i.item_id = v.item_id) vi INNER JOIN users u ON u.user_id = vi.user_id
    WHERE vi.view_time::date - u.register_time::date <= 7
    GROUP BY u.user_id
) AS subquery
WHERE features.user_id = subquery.user_id;

-- the number of views of items which where then bought by user
-- during the first week
-- features column: viewed_bought_count
UPDATE features SET
    viewed_bought_count = subquery.viewed_bought_count
FROM
(
SELECT u.user_id, COUNT(*) as viewed_bought_count
    FROM
        (SELECT c.item_id, c.user_id, v.view_time, c.conv_time
            FROM views v INNER JOIN conversions c ON (c.item_id, c.user_id) = (v.item_id, v.user_id)) vi
    INNER JOIN users u ON u.user_id = vi.user_id
    WHERE vi.view_time::date - u.register_time::date <= 7
        AND vi.conv_time::date - u.register_time::date <=7
        AND vi.view_time < vi.conv_time
    GROUP BY u.user_id
) AS subquery
WHERE features.user_id = subquery.user_id;


------------------------------------------------------------------
--********************* users_ads related features *************--
------------------------------------------------------------------

-- 1 - if user has seen any ads before
-- 0 otherwise
-- features column: has_seen_ad
UPDATE features SET
    has_seen_ad = subquery.has_seen_ad
FROM
(
SELECT u.user_id, COUNT(*) has_seen_ad
    FROM users u INNER JOIN user_ads a
    ON u.user_id = a.user_id
    GROUP BY u.user_id
) AS subquery
WHERE features.user_id = subquery.user_id;


------------------------------------------------------------------
--********************* Users related features *************------
------------------------------------------------------------------

-- features columnt: country
UPDATE features SET
    country = subquery.country
FROM
( SELECT user_id, country FROM users ) AS subquery
WHERE features.user_id = subquery.user_id;

-- the day of the year of registration
-- column: regist_day_of_year
UPDATE features SET
    regist_day_of_year = subquery.regist_day_of_year
FROM
( SELECT user_id,
       (30.5 * (extract(month from u.register_time::date) - 1) + extract(day from u.register_time::date))::int
          as regist_day_of_year
    FROM users u
) AS subquery
WHERE features.user_id = subquery.user_id;

---- some categorical features -----------------------------------
---- for one hot encoding ----------------------------------------

-- utm_source
-- features column: utm_source
UPDATE features SET
    utm_source = subquery.utm_source
FROM (
    SELECT a.user_id, a.utm_source as utm_source
    FROM user_ads a INNER JOIN users u ON a.user_id = u.user_id
) AS subquery
WHERE features.user_id = subquery.user_id;

-- utm_campaign, utm_medium, utm_content;
UPDATE features SET
    utm_campaign = subquery.utm_campaign,
    utm_medium = subquery.utm_medium,
    utm_content = subquery.utm_content
FROM (
    SELECT a.user_id, a.utm_campaign as utm_campaign, a.utm_medium as utm_medium, a.utm_content as utm_content
    FROM user_ads a INNER JOIN users u ON a.user_id = u.user_id
) AS subquery
WHERE features.user_id = subquery.user_id;


---- some categorical features -----------------------------------
---- items related -----------------------------------------------
-- these are groups and types of items user bought within 7 days after registration
-- with respect to:
-- * personality
-- * style
-- * category
-- * theme
-- this query will be used to build vectors of features counting the number of
-- time user bought from some category, personality, style, theme
-- it is saved to csv for further processing

SELECT u.user_id, i.personality, i.style, i.theme, i.category
    FROM users u INNER JOIN conversions c ON u.user_id = c.user_id
    INNER JOIN items i ON c.item_id = i.item_id
    WHERE c.conv_time::date - u.register_time::date <= 7
    ORDER BY u.user_id;


------------------------------------------------------------------
--********************* Interesting queries ****************------
------------------------------------------------------------------

-- the number of items views but not in the database anymore
SELECT COUNT(*) FROM
    (select v.item_id, COUNT(*)
        FROM views v LEFT JOIN items i
        ON i.item_id = v.item_id WHERE i.item_id IS NULL AND v.pagetype = 'Product'
        GROUP BY v.item_id) q;

------------------------------------------------------------------
--********************* Interesting queries ****************------
------------------------------------------------------------------

-- the number of items views but not in the database anymore
SELECT COUNT(*) FROM
    (select v.item_id, COUNT(*)
        FROM views v LEFT JOIN items i
        ON i.item_id = v.item_id WHERE i.item_id IS NULL AND v.pagetype = 'Product'
        GROUP BY v.item_id) q;
