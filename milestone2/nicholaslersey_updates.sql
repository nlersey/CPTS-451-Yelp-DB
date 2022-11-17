update user_ set tipcount=num
 from (SELECT user_id, COUNT(*) as num
      FROM tip 
      group by user_id) x
  where user_.user_id = x.user_id;

 SELECT * FROM user_
 WHERE tipcount <> 0;


 UPDATE business
 SET numTips = (SELECT COUNT(*)
 			   from tip
 			  where business.business_id = tip.business_id
 			  group by business_id);

 UPDATE business
 SET numtips = 0
 where numtips is NULL;

 SELECT * FROM business
 WHERE numTips <> 0;

 UPDATE business
 SET numcheckin = (SELECT COUNT(business_id)
 			  from checkins
			  where business.business_id = checkins.business_id
 			  group by business_id);

 UPDATE business
 SET numcheckin = 0
 where numcheckin is NULL;

 SELECT * FROM business
 WHERE numcheckin <> 0;