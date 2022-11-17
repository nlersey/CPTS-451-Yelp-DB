CREATE OR REPLACE FUNCTION updtUserTips() RETURNS TRIGGER AS '
BEGIN
	UPDATE user_
	SET tipCount = (tipCount + 1)
	WHERE user_.user_id = NEW.user_id;
	RETURN NEW;
END
' LANGUAGE plpgsql;


CREATE TRIGGER newUserTips
AFTER INSERT ON tip
FOR EACH ROW
EXECUTE PROCEDURE updtUserTips();

CREATE OR REPLACE FUNCTION updtBusTips() RETURNS TRIGGER AS '
BEGIN
	UPDATE business
	SET numtips = numTips + 1
	WHERE business.business_id = NEW.business_id;
	RETURN NEW;
END
' LANGUAGE plpgsql;

CREATE TRIGGER newBusTips
AFTER INSERT ON tip
FOR EACH ROW
EXECUTE PROCEDURE updtBusTips();

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

CREATE OR REPLACE FUNCTION updtTotalLikes() RETURNS TRIGGER AS '
BEGIN
	UPDATE user_
	SET totallikes = totallikes + 1
	WHERE user_.user_id = NEW.user_id;
	RETURN NEW;
END
' LANGUAGE plpgsql;


CREATE TRIGGER newTotalLikes
AFTER UPDATE ON tip
FOR EACH ROW
EXECUTE PROCEDURE updtTotalLikes();