select users."userId", least("signupTime", first_buy) as first_action
from users left join users_firstbuy on (users."userId"=users_firstbuy."userId")
