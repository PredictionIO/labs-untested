-- użytkownicy wydający w ciągu 30 dni od rejestracji

select users."userId",sum(
 case 
  when ("timestamp"<=users."signupTime" + interval '30 days') and
       ("timestamp">=users."signupTime")
   then price*quantity 
  else 
   0 
 end) as revenue
from users join conversions on (users."userId"=conversions."userId")
group by users."userId";