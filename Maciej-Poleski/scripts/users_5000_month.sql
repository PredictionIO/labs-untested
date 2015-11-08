select "userId" from users as source where 
 (select sum(price*quantity) 
  from conversions 
  where ("userId"=source."userId") and ("timestamp"<=source."signupTime" + interval '30 days')
 )>5000;