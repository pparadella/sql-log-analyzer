#!/usr/bin/env python

import psycopg2
import datetime

DBName = "news"


def get_articles():
    c = db.cursor()
    c.execute("select title, views from views order by views desc limit 3;")
    return c.fetchall()


def get_authors():
    c = db.cursor()
    c.execute("select authors.name, sum(views) as views from authors,views " +
              "where authors.id = views.author group by authors.name " +
              "order by views desc;")
    return c.fetchall()


def get_httperror():
    c = db.cursor()
    c.execute("select time, " +
              "(cast(ocurr as float)*100)/cast(total as float) as error " +
              "from httpreq where status like '404%' and " +
              "(cast(ocurr as float)*100)/cast(total as float) > 1;")
    return c.fetchall()


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


try:
    db = psycopg2.connect(database=DBName)
except Exception:
    db = False
    print("\nUnable to connect to the database")


if db:
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
    db.close()
else:
    print("Couldn't fetch data because was unable to connect to the database.")
