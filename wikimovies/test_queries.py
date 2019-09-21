
# Template of query to retrive all crative works from someone
ALL_WORKS_FROM_SOMEONE_QUERY = """
SELECT H.human_name,C.creative_work_name, C.creative_work_type, P.role_name 
FROM creative_works C, humans H, participations P
WHERE P.human_id = H.human_id
AND C.creative_work_id = P.creative_work_id
AND H.human_name like '%{}%'
"""

# Query to retrieve the human who realized the most creative works
MOST_CREATIVE_WORKS_QUERY = """
SELECT H.human_id, H.human_name, C.creative_work_type, COUNT(*) AS CNT 
FROM creative_works C, humans H, participations P 
WHERE P.human_id = H.human_id 
AND C.creative_work_id = P.creative_work_id
GROUP BY (H.human_name, H.human_id, C.creative_work_type)
ORDER BY CNT DESC
"""

# The human who has realized the most creative works
MOST_CREATIVE_HUMAN = "Ilaiyaraaja"


# Query to retrieve the human most versatile in realization of works
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

# The human who has realized the most creative works of different types
MOST_VERSATILE_HUMAN_WORKS = "Leonard Nimoy"


# Query to retrieve the human most versatile in covering several roles
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

# The human who has realized the most creative works in different roles
MOST_VERSATILE_HUMAN_ROLES = "Robert Rodriguez"


# All tests to verify the minimum expected count in tables
ALL_TEST_COUNT_TABLES = [("humans", 1500000),
                         ("roles", 15),
                         ("movies", 200000),
                         ("songs", 100000),
                         ("animatedmovies", 5000),
                         ("books", 90000),
                         ("tvshows", 5000),
                         ("videogames", 38000),
                         ("animatedmovie_roles", 28000),
                         ("book_roles", 60000),
                         ("movie_roles", 1400000),
                         ("song_roles", 120000),
                         ("tvshow_roles", 90000),
                         ("videogame_roles", 2000),
                         ("creative_works", 500000),
                         ("participations", 1500000)]


# All test to check creative works amount, types and roles in it from someone
ALL_VERIFY_WORKS_FROM_SOMEONE = \
    [("Adriano Celentano", 50, {"MOVIE", "SONG", "TVSHOW"}, {"cast member", "performer"}),
    ("Steven Ogg", 3, {"MOVIE", "VIDEOGAME", "TVSHOW"}, {"cast member", "voice actor"}),
    ("Paolo Villaggio", 40, {"MOVIE", "BOOK"}, {"cast member", "screenwriter", "author"}),
    ("Eddie Murphy", 40, {"ANIMATEDMOVIE", "MOVIE", "SONG"}, {"cast member", "performer", "voice actor"}),
    ("Bryan Cranston", 40, {"ANIMATEDMOVIE", "MOVIE", "TVSHOW"}, {"cast member", "voice actor", "director"}),
    ("Ashley Johnson", 30, {"ANIMATEDMOVIE", "MOVIE", "TVSHOW", "VIDEOGAME"}, {"cast member", "voice actor"})]


def execute_tests_most_creative(cur):
    """
    assert tests to check on most creative users
    :param cur: postgres cursor
    """

    def compare_human_with_queryresult(cur, query, target_human, quality):
        cur.execute(query)
        result = cur.fetchall()
        human_creative = result[0][1]
        print("Asserting most {} human {} == {}".format(quality, human_creative, target_human))
        assert (target_human == human_creative)

    compare_human_with_queryresult(cur, MOST_CREATIVE_WORKS_QUERY, MOST_CREATIVE_HUMAN, "creative")
    compare_human_with_queryresult(cur, MOST_VERSATILE_WORKS_QUERY, MOST_VERSATILE_HUMAN_WORKS, "versatile in works")
    compare_human_with_queryresult(cur, MOST_VERSATILE_ROLES_QUERY, MOST_VERSATILE_HUMAN_ROLES, "versatile in roles")


def execute_test_counts(cur):
    """
    assert tests for checking amount of records in tables
    :param cur: postgres cursor
    """
    for table, count in ALL_TEST_COUNT_TABLES:
        query = "SELECT COUNT(*) FROM {}".format(table)
        cur.execute(query)
        result = cur.fetchall()
        row_count = result[0][0]
        print("Asserting {} rows in {} >= {}".format(row_count, table, count))
        assert row_count >= count


def execute_verify_creative_works_person(cur):
    """
    assert tests to verify the amount of creative works of a person, their type and their role in these
    :param cur: postgres cursor
    """
    for human, count, work_types, roles in ALL_VERIFY_WORKS_FROM_SOMEONE:
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
    """
    execute all tests
    :param cur: postgres cursor
    """
    print("Executing tests on data...")
    print("Executing test on tables size...")
    execute_test_counts(cur)
    print("Executing test on creative_work_type...")
    execute_verify_creative_works_person(cur)
    print("Executing aggregation tests")
    execute_tests_most_creative(cur)



