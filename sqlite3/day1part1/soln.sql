.mode csv
create table input(a INTEGER);
.import puzzle.in input

WITH numbered AS (
    SELECT
    ROW_NUMBER () OVER () rownum, a
    FROM input
)
SELECT count(*) as count_increased
FROM numbered former
JOIN numbered later
ON former.rownum + 1 = later.rownum
WHERE later.a > former.a;

