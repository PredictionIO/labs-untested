select
	(select count(*) from features where week_revenue > 5000) as "users with week_revenue>5000",
	(select count(*) from features where month_revenue > 5000) as "users with month_revenue>5000";

select 
	(select count(*) from features) as "users_count",
	(select count(*) from features where week_revenue > 0) as "users with week_revenue > 0",
	(select count(*) from features where month_revenue > 0) as "users with month_revenue > 0",
	(select count(*) from features where month_revenue - week_revenue > 0) as "users with month_revenue>week_revenue",
	(select count(*) from features where week_revenue = 0 and adds_count = 0 and month_revenue > 0) as "idle users with month_revenue > 0",
	(select count(*) from features where items_bought = 1 and month_revenue > week_revenue) as "users with items_bought = 0 and month_revenue > week_revenue";

