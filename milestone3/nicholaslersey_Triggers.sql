CREATE OR REPLACE FUNCTION updtUserReviews() RETURNS TRIGGER AS '
BEGIN
	UPDATE usertable
	SET review_count = (review_count + 1)
	WHERE usertable.user_id = NEW.user_id;
	RETURN NEW;
END
' LANGUAGE plpgsql;


CREATE TRIGGER newUserReview
AFTER INSERT ON review
FOR EACH ROW
EXECUTE PROCEDURE updtUserReviews();

CREATE OR REPLACE FUNCTION updtBusReviews() RETURNS TRIGGER AS '
BEGIN
	UPDATE business
	SET review_count = review_count + 1
	WHERE business.business_id = NEW.business_id;
	RETURN NEW;
END
' LANGUAGE plpgsql;

CREATE TRIGGER newBusReviews
AFTER INSERT ON review
FOR EACH ROW
EXECUTE PROCEDURE updtBusReviews();

CREATE OR REPLACE FUNCTION updtnumCheckin() RETURNS TRIGGER AS '
BEGIN
	UPDATE business
	SET numcheckin = numcheckin + 1
	WHERE business.business_id = NEW.business_id;
	RETURN NEW;
END
' LANGUAGE plpgsql;

CREATE TRIGGER newNumCheckin
AFTER INSERT ON checkins
FOR EACH ROW
EXECUTE PROCEDURE updtnumCheckin();

CREATE TRIGGER upcheckins
AFTER update ON checkins
FOR EACH ROW
EXECUTE PROCEDURE updtnumCheckin();

CREATE OR REPLACE FUNCTION updtTotalLikes() RETURNS TRIGGER AS '
BEGIN
	UPDATE usertable
	SET totallikes = totallikes + 1
	WHERE usertable.user_id = NEW.user_id;
	RETURN NEW;
END
' LANGUAGE plpgsql;
