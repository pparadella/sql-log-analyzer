# Python 2.7.12

import psycopg2
import datetime

DBName = "news"


def get_articles():
    db = psycopg2.connect(database=DBName)
    c = db.cursor()
    c.execute("select title, views from views order by views desc limit 3;")
    return c.fetchall()
    db.close()


def get_authors():
    db = psycopg2.connect(database=DBName)
    c = db.cursor()
    c.execute("select authors.name, sum(views) as views from authors,views " +
              "where authors.id = views.author group by authors.name " +
              "order by views desc;")
    return c.fetchall()
    db.close()


def get_httperror():
    db = psycopg2.connect(database=DBName)
    c = db.cursor()
    c.execute("select time, " +
              "(cast(ocurr as float)*100)/cast(total as float) as error " +
              "from httpreq where status like '404%' and " +
              "(cast(ocurr as float)*100)/cast(total as float) > 1;")
    return c.fetchall()
    db.close()


def format_date(date):
    date = datetime.datetime.strptime(date, "%Y-%m-%d")
    month = {
        1: 'January',
        2: 'February',
        3: 'March',
        4: 'April',
        5: 'May',
        6: 'June',
        7: 'July',
        8: 'August',
        9: 'September',
        10: 'October',
        11: 'November',
        12: 'December'
        }.get(date.month, '0')
    return month + " " + str(date.day) + ", " + str(date.year)


print('\nTop 3 articles:')
for i in get_articles():
    print('* "' + i[0] + '" -- ' + str(i[1]) + " views")

print('\nTop Authors:')
for i in get_authors():
    print('* ' + i[0] + ' -- ' + str(i[1]) + " views")

print('\nHttp requisitions errors greater than 1%:')
for i in get_httperror():
    print('* ' + format_date(str(i[0])) +
          ' -- ' + str('%.1f' % i[1]) + "% errors\n")
