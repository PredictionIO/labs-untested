-- użytkownicy wydający w ciągu 30 dni od rejestracji

select users."userId",sum(
 case 
  when ("timestamp"<=users."signupTime" + interval '30 days') and
       ("timestamp">=users."signupTime")
   then price*quantity 
  else 
   0 
 end) as revenue_in_30days,
 sum(
 case 
  when ("timestamp"<=users."signupTime" + interval '7 days') and
       ("timestamp">=users."signupTime")
   then price*quantity 
  else 
   0 
 end) as revenue_in_7days
from users left join conversions on (users."userId"=conversions."userId")
group by users."userId";