.mode csv
create table foo(a);
.import puzzle.in foo

WITH RECURSIVE powers_of_two(n, result) as (
    values(0, 1)
    union all
    select (n+1) as n, result * 2
    from powers_of_two
    limit 20
), cnt(x) AS (
     SELECT 1
     UNION ALL
     SELECT x+1 FROM cnt
      LIMIT 100000
), bit_num AS (
    select x from cnt where x <= (select length(a) from foo limit 1)
), most_common AS (
    select bit_num.x,
        (
            select substr(a, bit_num.x, 1) as bit
            from foo
            group by bit
            order by count(*) desc
        ) as most_common
    from bit_num
), ir1 as (
    select ((select length(a) from foo limit 1) - x) as val, most_common
    from most_common
), ir2 as (
    select sum(
        CASE
        WHEN most_common = '1'
        THEN (select result from powers_of_two where n = val)
        ELSE 0
        END
    ) as result
    from ir1
), least_common as (
    select x, (
        CASE
        WHEN most_common = '1'
        THEN '0'
        ELSE '1'
        END
    ) as least_common
    from most_common
), ir3 as (
    select ((select length(a) from foo limit 1) - x) as val, least_common
    from least_common
), ir4 as (
    select sum(
        CASE
        WHEN least_common = '1'
        THEN (select result from powers_of_two where n = val)
        ELSE 0
        END
    ) as result
    from ir3
)
select ((select result from ir2) * (select result from ir4)) as answer;

