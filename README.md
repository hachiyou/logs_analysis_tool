# Logs Analysis Tool

Base on a given database 'news', answer the following questions:

* What are the most popular three articles of all time?  
Expand: What are the N most popular articles of all time? (N represents a positive number.)

* What are the most popular three authors of all time?  
Expand: What are the N most popular authors of all time? (N represents a positive number.)

* On which days did more than 1% of requests lead to errors?

## Getting Started

### Prerequisites

Since I wrote this in windows 10, all the software are windows based.  
The required softwares are:

1. [Python 3.6.5](https://wiki.python.org/moin/BeginnersGuide/Download)
2. [Vagrant 2.0.4](https://www.vagrantup.com/downloads.html)
3. [Virtual Box 5.2](https://www.virtualbox.org/wiki/Downloads)
4. [Git Bash](https://git-scm.com/downloads)

### Installation & Setup

1. Download and install all the required software.
2. Download the zip file from <https://github.com/udacity/fullstack-nanodegree-vm> and extract the zip file.
3. Navigate to this folder in Bash using `cd`. Change directory to <b>vagrant</b>
4. Run the command `vagrant up` to download the linux box, run command `vagrant ssh` after successful installation of linux.
5. Anytime after should you want to invoke vagrant, you just have to run the command `vagrant ssh` under the directory vagrant.
5. Download the files in this repository, unzip and place this folder under vagrant.
6. Run the command `python news.py` and you will be greet with the starting page.


## Built With

* Python 3.6.5


#### View Definitions
I had created two views for ease of viewing the data required to parse.  
The view will be created in the py file so you don't have to create them on your own.  
The definitions are as followed:

###### Article details view
```CREATE OR REPLACE VIEW articles_access_view AS
SELECT au.name AS author, ar.title AS article_title, aa.number_of_access AS most_accessed
FROM articles AS ar, authors AS au, (
        SELECT path, count(id) as number_of_access
        FROM log
        WHERE path != '/' AND status = '200 OK'
        GROUP BY path
        ORDER BY number_of_access DESC
    ) as aa
    WHERE aa.path LIKE ('%' || ar.slug) AND ar.author = au.id;
```

###### Error details view
```
CREATE OR REPLACE VIEW daily_error_percentage_view AS
SELECT DATE(l.time) AS access_date, COUNT(status) AS erroneous_access, t.total_access
FROM log AS l, (
    SELECT date(time) as access_date, COUNT(status) as total_access
    FROM log
    GROUP BY DATE(time)
    ) AS t
WHERE status = '404 NOT FOUND' AND DATE(l.time) = t.access_date
GROUP BY DATE(l.time), t.total_access;
```
