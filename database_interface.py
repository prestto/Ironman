import sqlite3 as sql

conn = sql.connect("./database/ironbase.db")

c = conn.cursor()

req = c.execute("""
              create table race_times (
              id integer primary key,
              name NVARCHAR(100), 
              country NVARCHAR(100), 
              datetime TEXT, 
              swim TEXT, 
              bike TEXT, 
              run TEXT, 
              gen_rank NVARCHAR(10), 
              ovr_rank NVARCHAR(10), 
              div_rank NVARCHAR(10), 
              total NVARCHAR(10), 
              points NVARCHAR(10),
              parent_url NVARCHAR(200)
              );
              """)


# # Check that links page exists, if not create it
# tb_exists = "SELECT name FROM sqlite_master WHERE type='table' AND name='link_page'"

# if not co.execute(tb_exists).fetchone():
#     req = c.execute("""
#                   create table link_page (
#                   id integer primary key,
#                   link NVARCHAR(200),
#                   event_name nvarchar(100),
#                   datetime text,
#                   city NVARCHAR(100),
#                   country NVARCHAR(100),
#                   year_table int,
#                   location_table NVARCHAR(100),
#                   distance NVARCHAR(50),
#                   format NVARCHAR(50)
#                   );
#                   """)
    
# tb_exists = "SELECT name FROM sqlite_master WHERE type='table' AND name='results_page'"
# if not co.execute(tb_exists).fetchone():
#     req = c.execute("""
#                 ADD RESULTS PAGE HERE
#               );
#               """)


# c.execute("""
#           select count(link)
#           from link_page
#           where link = :link
#           """,
#           {"link" : "http://eu.ironman.com/triathlon/coverage/detail.aspx?race=bariloche70.3&y=2018"})

# c.execute("drop table link_page")
# c.execute("drop table results_page")


# c.execute("""insert into link_page ('link', 'year_link', 'location_link', 'year_table', 'location_table', 'distance', 'format') values
#           ('http://eu.ironman.com/triathlon/coverage/detail.aspx?race=florida70.3&y=2008'
#           , '2008', 'florida', '2008', 'florida', 'IRONMAN', 'TABLE')
#           """)

# c.execute("select * from link_page")

# print(c.fetchone()[0])

conn.commit()
conn.close()


