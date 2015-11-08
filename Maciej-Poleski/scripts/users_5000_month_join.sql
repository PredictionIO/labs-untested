-- użytkownicy wydający więcej niż 5000 w ciągu 30 dni od rejestracji

select users."userId"
from users join conversions on (users."userId"=conversions."userId")
group by users."userId"
having sum(
 case 
  when ("timestamp"<=users."signupTime" + interval '30 days') and
       ("timestamp">=users."signupTime")
   then price*quantity 
  else 
   0 
 end)>5000;