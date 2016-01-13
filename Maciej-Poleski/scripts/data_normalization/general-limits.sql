SELECT min("signupTime"),max("signupTime") from users union 
select min(views."timestamp"),max(views."timestamp") from views union 
select min(conversions."timestamp"),max(conversions."timestamp")
  FROM conversions;
