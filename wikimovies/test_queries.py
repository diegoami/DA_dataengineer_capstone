
ALL_WORKS_FROM_SOMEONE_QUERY = """
SELECT H.human_name,C.creative_work_name, C.creative_work_type, P.role_name 
FROM creative_works C, humans H, participations P
WHERE P.human_id = H.human_id
AND C.creative_work_id = P.creative_work_id
AND H.human_name like '%{}%'
"""

MOST_CREATIVE_WORKS_QUERY = """
SELECT H.human_id, H.human_name, C.creative_work_type, COUNT(*) AS CNT 
FROM creative_works C, humans H, participations P 
WHERE P.human_id = H.human_id 
AND C.creative_work_id = P.creative_work_id
GROUP BY (H.human_name, H.human_id, C.creative_work_type)
ORDER BY CNT DESC
"""

MOST_CREATIVE_HUMAN = "Ilaiyaraaja"

MOST_VERSATILE_WORKS_QUERY = """
SELECT human_id, human_name, creative_work_type, cnt, 
SUM(cnt) OVER (PARTITION BY human_id) as snct, 
COUNT(cnt) OVER (PARTITION BY human_id) ccnt FROM (
    SELECT H.human_id,
           H.human_name,
           C.creative_work_type,
           COUNT(*) AS CNT
    FROM creative_works C,
         humans H,
         participations P
    WHERE P.human_id = H.human_id
      AND C.creative_work_id = P.creative_work_id
    GROUP BY (H.human_name, H.human_id, C.creative_work_type)
    ORDER BY CNT DESC
) CREATIVE_WORKS
ORDER BY ccnt DESC, snct DESC
"""

MOST_VERSATILE_HUMAN_WORKS = "Leonard Nimoy"

MOST_VERSATILE_ROLES_QUERY = """
SELECT human_id, human_name, role_name, cnt, 
SUM(cnt) over (PARTITION BY human_id) as snct, 
COUNT(cnt) over (PARTITION BY human_id) ccnt FROM (
    SELECT H.human_id,
           H.human_name,
           P.role_name,
           COUNT(*) AS CNT
    FROM humans H,
         participations P
    where P.human_id = H.human_id

    GROUP BY (H.human_name, H.human_id, P.role_name)
    ORDER BY CNT DESC
) CREATIVE_ROLES
ORDER BY ccnt desc, snct desc
"""

MOST_VERSATILE_HUMAN_ROLES = "Robert Rodriguez"



all_test_count_tables = [("humans", 2000000),
                         ("roles", 15),
                         ("movies", 200000),
                         ("songs", 100000),
                         ("animatedmovies", 6000),
                         ("books", 90000),
                         ("tvshows", 50000),
                         ("videogames", 38000),
                         ("animatedmovie_roles", 28000),
                         ("book_roles", 60000),
                         ("movie_roles", 1400000),
                         ("song_roles", 140000),
                         ("tvshow_roles", 110000),
                         ("videogame_roles", 2000),
                         ("creative_works", 560000),
                         ("participations", 1700000)]


all_verify_works_from_someone = \
    [("Adriano Celentano", 50, {"MOVIE", "SONG", "TVSHOW"}, {"cast member", "performer"}),
    ("Steven Ogg", 3, {"MOVIE", "VIDEOGAME", "TVSHOW"}, {"cast member", "voice actor"}),
    ("Paolo Villaggio", 40, {"MOVIE", "BOOK"}, {"cast member", "screenwriter", "author"}),
    ("Eddie Murphy", 40, {"ANIMATEDMOVIE", "MOVIE", "SONG"}, {"cast member", "performer", "voice actor"}),
    ("Bryan Cranston", 40, {"ANIMATEDMOVIE", "MOVIE", "TVSHOW"}, {"cast member", "voice actor", "director"}),
    ("Ashley Johnson", 30, {"ANIMATEDMOVIE", "MOVIE", "TVSHOW", "VIDEOGAME"}, {"cast member", "voice actor"})]


def execute_most_creative(cur):

    def compare_human_with_queryresult(cur, query, target_human, quality):
        cur.execute(query)
        result = cur.fetchall()
        human_creative = result[0][1]
        print("Asserting most {} human {} == {}".format(quality, human_creative, target_human))
        assert (target_human == human_creative)

    compare_human_with_queryresult(cur, MOST_CREATIVE_WORKS_QUERY, MOST_CREATIVE_HUMAN, "creative")
    compare_human_with_queryresult(cur, MOST_VERSATILE_WORKS_QUERY, MOST_VERSATILE_HUMAN_WORKS, "versatile in works")
    compare_human_with_queryresult(cur, MOST_VERSATILE_ROLES_QUERY, MOST_VERSATILE_HUMAN_ROLES, "versatile in roles")


def execute_counts(cur):
    for table, count in all_test_count_tables:
        query = "SELECT COUNT(*) FROM {}".format(table)
        cur.execute(query)
        result = cur.fetchall()
        row_count = result[0][0]
        print("Asserting {} rows in {} >= {}".format(row_count, table, count))
        assert row_count >= count


def execute_verify_creative_work_type(cur):
    for human, count, work_types, roles in all_verify_works_from_someone:
        query = ALL_WORKS_FROM_SOMEONE_QUERY.format(human)
        cur.execute(query)
        result = cur.fetchall()
        rows_found, works_found, roles_found = 0, set(), set()
        for row in result:
            rows_found += 1
            work_type, role = row[2], row[3]
            works_found.add(work_type)
            roles_found.add(role)
        print("Asserting {} rows for {}  >= {}".format(rows_found, human, count))
        assert rows_found >= count
        print("Asserting {} rows for {} contains {}".format(works_found, human, work_types))
        assert all([work in works_found for work in work_types])
        print("Asserting {} rows for {} contains {}".format(roles_found, human, roles))
        assert all([role in roles_found for role in roles])


def execute_tests(cur):
    print("Executing tests on data...")
    print("Executing test on tables size...")
    execute_counts(cur)
    print("Executing test on creative_work_type...")
    execute_verify_creative_work_type(cur)
    print("Executing aggregation tests")
    execute_most_creative(cur)



