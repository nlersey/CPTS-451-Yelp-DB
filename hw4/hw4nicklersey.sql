--Q1
SELECT distinct C.courseNo, C.credits
FROM Course C, Enroll E, Student S
WHERE C.courseno = E.courseno AND E.sID = S.sID 
   AND S.major='CptS' AND S.trackcode = 'SYS'
   ORDER BY C.courseNo;

--Q2
SELECT S.sName,S.sID,S.major, S.trackcode, SUM(credits)
FROM Course C, Enroll E, Student S
WHERE E.sID=S.sID AND C.courseno = E.courseno
GROUP BY s.sID
HAVING SUM(credits)>18
ORDER BY S.sName,S.sID;

--Q3
SELECT distinct E1.courseNo 
FROM Student S1, Enroll E1
WHERE S1.sid = E1.sid AND S1.trackcode='SE' AND S1.major='CptS'  
AND (E1.courseno, S1.Major) NOT IN 
  ( SELECT E2.courseno,S2.Major
    FROM Student S2, Enroll E2
    WHERE S2.sid = E2.sid AND NOT (S2.trackcode = 'SE' AND S2.major = 'CptS') )
ORDER BY E1.courseno;

--Q4
SELECT DISTINCT S2.sname, s2.sID
FROM Student S1, Student S2, Enroll E1,Enroll E2, Course C
WHERE S1.sname='Diane' and E1.sID=S1.sID and E2.sID=S2.sID AND E1.grade=E2.grade and E1.courseno=E2.courseno AND S1.sID != S2.sID

--q5
SELECT DISTINCT s.sname, s.sid
FROM Student s, Enroll e
WHERE  s.sID NOT IN (SELECT sID FROM ENROLL ) and s.major='CptS'
order by s.sname

--q6
SELECT c.courseno, c.enroll_limit
FROM Course c
WHERE c.classroom like 'Sloan%' AND c.enroll_limit <
	(
		SELECT Count(sid)
		FROM Enroll e
		WHERE e.courseno = c.courseno
	)


--q7
SELECT DISTINCT s.sname, s.sID, e.courseno
FROM Enroll e, Prereq p, Student s, Enroll e2
WHERE e2.grade < 2 AND e.sID = s.sID AND e.courseno = p.CourseNo AND e2.courseno =p.precourseno AND e.sID=e2.sid

--q8
SELECT group1.courseno,group2.passCount*100/group1.allCount as passRate
FROM
( SELECT courseno, COUNT(*) as allCount
  FROM Enroll
  WHERE grade IS NOT NULL
  GROUP BY courseno ) as group1,
( SELECT courseno, COUNT(*) as passCount
  FROM Enroll
  WHERE grade IS NOT NULL  AND grade >=2
  GROUP BY courseno ) as group2
 WHERE group1.courseno = group2.courseno AND group1.courseno like 'CptS%'

