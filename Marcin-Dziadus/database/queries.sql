select conversions.user_id, item_id, price, quantity
into hour_conversions
from conversions
join users
on conversions.user_id=users.user_id and conversions.timestamp >= users.signup_time and conversions.timestamp - users.signup_time <= '1 hour';

select conversions.user_id, item_id, price, quantity
into week_conversions
from conversions
join users
on conversions.user_id=users.user_id and conversions.timestamp >= users.signup_time and conversions.timestamp - users.signup_time <= '7 days';

select conversions.user_id, item_id, price, quantity
into month_conversions
from conversions
join users
on conversions.user_id=users.user_id and conversions.timestamp >= users.signup_time and conversions.timestamp - users.signup_time <= '30 days';

select user_id, sum(price*quantity) as week_revenue
into feature1
from week_conversions
group by user_id;

select user_id, sum(price*quantity) as month_revenue
into feature2
from month_conversions
group by user_id;

select user_id, sum(price*quantity) as hour_revenue
into feature3
from hour_conversions
group by user_id;

select user_id, count(user_id) as items_count
into feature4
from week_conversions
where quantity > 0
group by user_id;

select views.user_id, item_id, page_type
into week_views
from views
join users
on views.user_id=users.user_id and views.timestamp >= users.signup_time and views.timestamp - users.signup_time <= '7 days';

select user_id, count(user_id) as adds_count
into feature5
from week_views
group by user_id;

select week_conversions.user_id, count(week_conversions.user_id) as categories_bought
into feature6
from week_conversions
join items
on week_conversions.item_id=items.item_id
group by user_id, items.category;

select user_id, count(user_id) as categories_seen
into feature7
from(
	select week_views.user_id
	from week_views
	join items
	on week_views.item_id=items.item_id
	group by user_id, items.category
) as inner_select
group by user_id;

select user_id, count(user_id) as discounted_bought
into discounted_conversions
from week_conversions
join items
on week_conversions.item_id=items.item_id and items.price - week_conversions.price > 0.1
group by user_id;

select discounted_conversions.*, discounted_conversions.discounted_bought::float/feature4.items_count as discount_ratio
into feature8
from discounted_conversions
join feature4
on discounted_conversions.user_id=feature4.user_id;

update features
set hour_revenue=feature3.hour_revenue
from feature3
where features.user_id=feature3.user_id;

update features
set  month_revenue=feature2.month_revenue
from feature2
where features.user_id=feature2.user_id;

update features
set week_revenue=feature1.week_revenue
from feature1
where features.user_id=feature1.user_id;

update features
set items_bought=feature4.items_count
from feature4
where features.user_id=feature4.user_id;

update features
set adds_count=feature5.adds_count
from feature5
where features.user_id=feature5.user_id;

update features
set categories_bought=feature6.categories_bought
from feature6
where features.user_id=feature6.user_id;

update features
set categories_bought=feature7.categories_seen
from feature7
where features.user_id=feature7.user_id;

update features
set discount_ratio=feature8.discount_ratio
from feature8
where features.user_id=feature8.user_id;

update features
set
	hour_revenue=round(coalesce(hour_revenue,0)::numeric,4),
	week_revenue=round(coalesce(week_revenue,0)::numeric,4),
	items_bought=coalesce(items_bought,0),
	adds_count=coalesce(adds_count,0),
	categories_bought=coalesce(categories_bought,0),
	categories_seen=coalesce(categories_seen,0),
	discount_ratio=coalesce(discount_ratio,0),
	month_revenue=round(coalesce(month_revenue,0)::numeric,4);


