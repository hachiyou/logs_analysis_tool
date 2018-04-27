import psycopg2

DBNAME = "news"

"""Query Section"""
CREATE_VIEW =
'''
CREATE OR REPLACE VIEW articles_access_data AS
SELECT au.name AS author, ar.title AS article_title, aa.number_of_access AS most_accessed  # noqa
FROM articles AS ar, authors AS au,
    (
        SELECT path, count(id) as number_of_access
        FROM log
        WHERE path != '/' AND status = '200 OK'
        GROUP BY path
        ORDER BY number_of_access DESC
    ) as aa
    WHERE aa.path LIKE ('%' || ar.slug) AND ar.author = au.id;
'''

SELECT_FAV_AUTHOR =
'''
SELECT author, count(author) as number_of_articles, sum(most_accessed) AS total_access  # noqa
FROM articles_access_data
GROUP BY author
ORDER BY Total_Access DESC;
'''

DISPLAY_ERROR_PERCENT =
'''
SELECT DATE(l.time) AS access_date, COUNT(status) AS erroneous_access, t.total_access, TO_CHAR(100 * COUNT(status)::FLOAT / total_access, '0D99%') AS error_percentage  # noqa
FROM log AS l, (
    SELECT date(time) as access_date, COUNT(status) as total_access
    FROM log
    GROUP BY DATE(time)
    ) AS t
WHERE status = '404 NOT FOUND' AND DATE(l.time) = t.access_date
GROUP BY DATE(l.time), t.total_access
ORDER BY error_percentage DESC;
'''
"""============================================================="""


def __create_view():
    """
    Create a view name "articles_access_data"
    to use for skimming through data
    """
    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()
    c.execute(CREATE_VIEW)
    db.close()


def get_most_accessed(topN=0):
    """
    Return top N most accessed article fetch from the database.
    0 or negative to fetch all the articles.
    """
    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()
    query = "SELECT * FROM articles_access_data"
    if topN > 0:
        query += " LIMIT " + topN + ";"
    else:
        query += ";"
    c.execute(query)
    r = c.fetchall()
    db.close()
    return r


def get_most_popular(topN=0):
    """
    Return top N most popular authors.
    0 or negative to fetch all the authors.
    """
    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()
    if topN > 0:
        query = SELECT_FAV_AUTHOR[:-1]
        + " LIMIT " + topN + ";"
    else:
        query = SELECT_FAV_AUTHOR
    c.execute(query)
    r = c.fetchall()
    db.close()
    return r


def get_error_percentage(topN=0):
    """
    Return the top N date with the most erroneous access.
    0 or negative to fetch all the date.
    """
    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()
    if topN > 0:
        query = DISPLAY_ERROR_PERCENT[:-1] + " LIMIT " + topN + ";"
    else:
        query = DISPLAY_ERROR_PERCENT
    c.execute(query)
    r = c.fetchall()
    db.close()
    return r
