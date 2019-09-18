
all_works_from_someone = """
SELECT H.human_name,C.creative_work_name, C.creative_work_type, P.role_name 
FROM creative_works C, humans H, participations P
WHERE P.human_id = H.human_id
AND C.creative_work_id = P.creative_work_id
AND H.human_name like '%{}%'
"""



most_creative_works = """
SELECT H.human_id, H.human_name, C.creative_work_type, COUNT(*) AS CNT FROM creative_works C, humans H, participations P where
P.human_id = H.human_id AND C.creative_work_id = P.creative_work_id
GROUP BY (H.human_name, H.human_id, C.creative_work_type)
ORDER BY CNT DESC
"""

partition_creative_works = """
SELECT human_id, human_name, creative_work_type, cnt, sum(cnt) over (PARTITION BY human_id) as snct FROM (
                                                    SELECT H.human_id,
                                                           H.human_name,
                                                           C.creative_work_type,
                                                           COUNT(*) AS CNT
                                                    FROM creative_works C,
                                                         humans H,
                                                         participations P
                                                    where P.human_id = H.human_id
                                                      AND C.creative_work_id = P.creative_work_id
                                                    GROUP BY (H.human_name, H.human_id, C.creative_work_type)
                                                    ORDER BY CNT DESC
                                                ) T
ORDER BY snct desc
"""


all_works_from_ogg = """
SELECT H.human_name,C.creative_work_name, C.creative_work_type, P.role_name FROM creative_works C,
                                                         humans H,
                                                         participations P
                                                    where P.human_id = H.human_id
                                                      AND C.creative_work_id = P.creative_work_id

                                                      AND H.human_name like  '%Steven Ogg%'
"""

all_works_from_villaggio = """
SELECT H.human_name,C.creative_work_name, C.creative_work_type, P.role_name FROM creative_works C,
                                                         humans H,
                                                         participations P
                                                    where P.human_id = H.human_id
                                                      AND C.creative_work_id = P.creative_work_id

                                                      AND H.human_name like  '%Paolo Villaggio%'
"""

all_works_from_eddie_murphy = """
SELECT H.human_name,C.creative_work_name, C.creative_work_type, P.role_name FROM creative_works C,
                                                         humans H,
                                                         participations P
                                                    where P.human_id = H.human_id
                                                      AND C.creative_work_id = P.creative_work_id

                                                      AND H.human_name like  '%Eddie Murphy%'
"""



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
    [("Adriano Celentano", 50, {"MOVIE", "SONG", "TVSHOW"}),
    ("Steven Ogg", 3, {"MOVIE", "VIDEOGAME", "TVSHOW"}),
    ("Eddie Murphy", 40, {"ANIMATEDMOVIE", "MOVIE", "SONG"}),
    ("Bryan Cranston", 40, {"ANIMATEDMOVIE", "MOVIE", "TVSHOW"}),
    ("Ashley Johnson", 30, {"ANIMATEDMOVIE", "MOVIE", "TVSHOW", "VIDEOGAME"})]



def execute_counts(cur):
    for table, count in all_test_count_tables:
        query = "SELECT COUNT(*) FROM {}".format(table)
        cur.execute(query)
        result = cur.fetchall()
        row_count = result[0][0]
        print("Asserting {} rows in {} >= {}".format(row_count, table, count))
        assert row_count >= count


def execute_verify_creative_work_type(cur):
    for human, count, work_types in all_verify_works_from_someone:
        query = all_works_from_someone.format(human)
        cur.execute(query)
        result = cur.fetchall()
        work_found, rows_found = set(), 0
        for row in result:
            rows_found += 1
            work_type = row[2]
            work_found.add(work_type)
        print("Asserting {} rows for {}  >= {}".format(rows_found, human, count))
        assert rows_found >= count
        print("Asserting {} rows for {} contains {}".format(work_found, human, work_types))
        assert all([work in work_found for work in work_types])


def execute_tests(cur):
    print("Executing tests on data...")
    print("Executing test on tables size...")
    execute_counts(cur)
    print("Executing test on creative_work_type...")
    execute_verify_creative_work_type(cur)



