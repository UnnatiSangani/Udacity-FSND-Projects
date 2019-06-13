#!/usr/bin/env python3

# Queries on the newsdata database for the Project Logs Analysis

import psycopg2

DB_NAME = "news"


def get(query):
    db = psycopg2.connect(database=DB_NAME)
    cursor = db.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    db.close()
    return results


QUERY_THREE_MOST_POPULAR_ARTICLES = """
SELECT
    articles.title,
    article_vw_summ.view_count
FROM
    articles
JOIN
    article_vw_summ ON articles.slug = article_vw_summ.log_slug limit 3;
"""
QUERY_MOST_POPULAR_AUTHORS = """
SELECT
    authors.name as author_name,
    sum(article_vw_summ.view_count) as author_vw_count
FROM
    article_vw_summ
JOIN
    articles ON article_vw_summ.log_slug = articles.slug
JOIN
    authors ON articles.author = authors.id
GROUP BY
    author_name
ORDER BY
    author_vw_count desc;
"""

QUERY_DAYS_WITH_HIGH_ERRORS = """
SELECT
    TO_CHAR(log_date, 'Mon DD, YYYY'),\
    round((vw_log.err_req * 100.0)/ vw_log.total_req ) as err_per
FROM
    vw_log
WHERE
    ((vw_log.err_req * 100.0)/ vw_log.total_req ) > 1;
"""


def get_three_most_popular_articles():
    return get(QUERY_THREE_MOST_POPULAR_ARTICLES)


def get_most_popular_authors():
    return get(QUERY_MOST_POPULAR_AUTHORS)


def get_days_with_higher_errors():
    return get(QUERY_DAYS_WITH_HIGH_ERRORS)


def answer_question_1():
    print ("\nTHE THREE MOST POPULAR ARTICLES OF ALL THE TIME")
    print ("-------------------------------------------------------")
    rows = get_three_most_popular_articles()
    for row in rows:
        print ("{article} - {count} views".format(article=row[0], count=row[1]))


def answer_question_2():
    print("\nTHE MOST POPULAR ARTICLE AUTHORS OF ALL THE TIME")
    print ("-------------------------------------------------------")
    rows = get_most_popular_authors()
    for row in rows:
        print ("{author} - {count} views".format(author=row[0], count=row[1]))


def answer_question_3():
    print ("\nDAYS WHICH HAS REQUESTS ERROR MORE THAN 1% ")
    print ("-------------------------------------------------------")
    rows = get_days_with_higher_errors()
    for row in rows:
        print ("{date} - {count} % errors".format(date=row[0], count=row[1]))


if __name__ == '__main__':
    answer_question_1()
    answer_question_2()
    answer_question_3()
