﻿select count(*) from ((select "userId" from users) union (select "userId" from conversions) union select "userId" from user_ads union select cast("userId" as bigint) from views where "userId" !='deleted') userIds;