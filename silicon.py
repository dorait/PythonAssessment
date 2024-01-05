import feedparser
import re
import sqlite3
conn = sqlite3.connect('tech_news.db')
c = conn.cursor()

c.execute("""CREATE TABLE IF NOT EXISTS tech_news_data(
          id varchar(255),
          author TEXT,
          title TEXT,
          content TEXT,
          summary str,
          url varchar(255),
          image_url varchar(255),
          published_at str
          
)""")

iteration_file = 'iteration.txt'
try:
    with open(iteration_file, 'r') as f:
        iteration = int(f.read().strip())
except FileNotFoundError:
    iteration = 0

url = "https://siliconangle.com/feed/"
feed = feedparser.parse(url)

for i in range(iteration,iteration+10):
    id = feed['entries'][i]['id']
    author = feed['entries'][i]['author']
    title = feed['entries'][i]['title']
    content = feed['entries'][i]['title']
    summary = feed['entries'][i]['summary']
    url = feed['entries'][i]['link']
    image_url = list(re.findall(r'<img[^>]+src="([^">]+)"', summary))[0]
    published_at = feed['entries'][i]['published']
    c.execute("INSERT INTO tech_news_data VALUES (?, ?, ?, ?, ?, ?, ?, ?)",(id, author, title, content, summary, url, image_url, published_at))
    conn.commit()

iteration += 10
with open(iteration_file, 'w') as f:
    f.write(str(iteration))

