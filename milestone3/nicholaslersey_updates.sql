update usertable set review_count=num
 from (SELECT user_id, COUNT(*) as num
      FROM review 
      group by user_id) x
  where usertable.user_id = x.user_id;

 SELECT * FROM usertable
 WHERE review_count <> 0;


 UPDATE business
 SET review_count = (SELECT COUNT(*)
 			   from review
 			  where business.business_id = review.business_id
 			  group by business_id);

 UPDATE business
 SET review_count = 0
 where review_count is NULL;

 SELECT * FROM business
 WHERE review_count <> 0;

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