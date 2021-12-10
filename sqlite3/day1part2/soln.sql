--
-- Usage:
--     sqlite3 < soln.sql > puzzle.out
--
-- Tested using:
--     SQLite version 3.27.2 2019-02-25 16:06:06
--
.mode csv
create table input(a INTEGER);
.import puzzle.in input

WITH numbered AS (
    SELECT
        ROW_NUMBER () OVER () rownum,
        a as value
    FROM input
), numbered_rolling_sum_with_garbage AS (
    SELECT
        rownum,
        SUM(value) OVER (ROWS BETWEEN 1 PRECEDING AND 1 FOLLOWING) as moving_avg
    FROM numbered
), numbered_rolling_sum AS (
    SELECT *
    FROM numbered_rolling_sum_with_garbage
    WHERE rownum > 1 AND rownum < (SELECT MAX(rownum) FROM numbered)
)
SELECT count(*) as count_increased
FROM numbered_rolling_sum former
JOIN numbered_rolling_sum later
ON former.rownum + 1 = later.rownum
WHERE later.moving_avg > former.moving_avg;

