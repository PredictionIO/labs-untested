-- Data pierwszego zakupu każdego użytkownika

select users."userId", min("timestamp") as "first_buy"
from users left join conversions on (users."userId"=conversions."userId")
group by users."userId"
