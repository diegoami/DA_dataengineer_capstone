



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

all_works_from_celentano = """
SELECT H.human_name,C.creative_work_name, C.creative_work_type, P.role_name FROM creative_works C,
                                                         humans H,
                                                         participations P
                                                    where P.human_id = H.human_id
                                                      AND C.creative_work_id = P.creative_work_id

                                                      AND H.human_name like  '%Adriano Celentano%'
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


all_test_queries = [most_creative_works, partition_creative_works, all_works_from_celentano, all_works_from_ogg, all_works_from_villaggio, all_works_from_eddie_murphy]

def execute_tests(cur):
    print("Executing tests on data...")
    for query in all_test_queries:
        cur.execute(query)
        result = cur.fetchall()
        for row in result:
            print(row)