#!/usr/bin/env python3.6.5

import psycopg2

# Database name we are connecting to.
DBNAME = "news"

# Query Sections

# String holding the sql code for creating view
CREATE_ARTICLE_ACCESS_VIEW = '''
CREATE OR REPLACE VIEW articles_access_view AS
SELECT au.name AS author, ar.title AS article_title, aa.number_of_access AS most_accessed
FROM articles AS ar, authors AS au,
    (
        SELECT path, count(id) as number_of_access
        FROM log
        WHERE path != '/' AND status = '200 OK'
        GROUP BY path
        ORDER BY number_of_access DESC
    ) as aa
    WHERE aa.path LIKE ('%' || ar.slug) AND ar.author = au.id;
'''  # noqa

# String holding the sql code for creating view
CREATE_DAILY_ERROR_VIEW = '''
CREATE OR REPLACE VIEW daily_error_percentage_view AS
SELECT DATE(l.time) AS access_date, COUNT(status) AS erroneous_access, t.total_access
FROM log AS l, (
    SELECT date(time) as access_date, COUNT(status) as total_access
    FROM log
    GROUP BY DATE(time)
    ) AS t
WHERE status = '404 NOT FOUND' AND DATE(l.time) = t.access_date
GROUP BY DATE(l.time), t.total_access;'''  # noqa

# String holding the sql code for fetching all the article in the database.
SELECT_ALL_ARTICLES = '''SELECT * FROM articles_access_view;'''

# String holding the sql code for fetching all the authors in the database.
SELECT_ALL_AUTHORS = '''
SELECT author, count(author) as number_of_articles, sum(most_accessed) AS total_access
FROM articles_access_view
GROUP BY author
ORDER BY Total_Access DESC;'''  # noqa

# String holding the sql code for fetching all the dates in the database.
SELECT_ERROR_DATE = '''
SELECT access_date, 100 * erroneous_access::FLOAT / total_access AS error_percentage
FROM daily_error_percentage_view
WHERE (100 * erroneous_access::FLOAT / total_access) > 1;'''  # noqa


def __create_view():
    """Create two views name "articles_access_view" and "daily_error_percentage_view"
    to use for skimming through data
    """  # noqa

    # Access the database
    db = psycopg2.connect(database=DBNAME)

    # Get the cursor for fetching data
    c = db.cursor()

    # Execute queries
    c.execute(CREATE_ARTICLE_ACCESS_VIEW)
    c.execute(CREATE_DAILY_ERROR_VIEW)

    # Close the connection after completing execution
    db.close()


def execute_query(sqlToExecuted, topN='0'):
    """ Execute the pass-in SQL query and return the result.
    Select the top N most result to display if topN parameter is given.

    Args:
        sqlToExecuted (str): SQL query
        topN (str) : an input taken from user to tell
            the database how many result should be display.
    """  # noqa

    # Access the database
    db = psycopg2.connect(database=DBNAME)

    # Get the cursor for fetching data
    c = db.cursor()

    # Execute queries
    if int(topN) > 0:
        query = sqlToExecuted[:-1] + " LIMIT " + str(topN) + ";"
    else:
        query = sqlToExecuted
    c.execute(query)
    r = c.fetchall()

    # Close the connection after completing execution
    db.close()

    return r
