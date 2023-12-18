import sqlite3
import feedparser
import tldextract
import pandas as pd


def database_setup():
    """A function to setup database"""
    conn = sqlite3.connect("tech_news.db")
    cursor = conn.cursor()
    cursor.execute(
        """CREATE TABLE IF NOT EXISTS tech_news_data(
                      website_id varchar(255),
                      author TEXT,
                      title TEXT,
                      content TEXT,
                      website_url varchar(255),
                      website_name TEXT,
                      image_url varchar(255),
                      published_at str
            )"""
    )
    print("tech_news Database created")


def parsing(website_rss_feed, iteration_file, n, iteration):
    """function parsing takes in the website rss feed, iterates 
    through the dictionary with iteration value of n"""
    print("Current value of iteration from the file is ", iteration)
    web_data_list = []
    for feed in website_rss_feed:
        len_of_feeddata = len(feedparser.parse(feed).entries)
        print("length of feed list :", len_of_feeddata)
        for i in range(
            min(iteration, len_of_feeddata - 1), min(iteration + n, len_of_feeddata)
        ):
            print("starting parsing of ", feed)
            feed_data = feedparser.parse(feed)["entries"][i]
            print("feed_data is ", feed_data)
            print(
                "Extracts the dictionary value in the position of the current iteration",
                i,
            )
            website_id = feed_data.get("id", "Data not present")
            author = feed_data.get("author", "Data not present")
            title = feed_data.get("title", "Data not present")
            content = feed_data.get("summary", "Data not present")
            website_url = feed_data.get("link", "Data not present")
            website_name = tldextract.extract(feed).domain
            image_url = feed_data.get("media_thumbnail")
            # If there is value in image_url field,the condition gets the value from url
            # if error arises, a message is assigned to the variable"
            try:
                if image_url:
                    image_url = image_url[0]["url"]
                else:
                    image_url = "Data not present"
            except (KeyError, TypeError):
                image_url = "Data not present"
            print("image_url=", image_url)
            published_at = feed_data.get("published", "Data not present")

            web_data_list.append(
                (
                    website_id,
                    author,
                    title,
                    content,
                    website_url,
                    website_name,
                    image_url,
                    published_at,
                )
            )
    web_data = pd.DataFrame(
        web_data_list,
        columns=[
            "website_id",
            "author",
            "title",
            "content",
            "website_url",
            "website_name",
            "image_url",
            "published_at",
        ],
    )
    print(" ")
    print("The data to be inserted to the table is shown below")
    print(web_data)
    conn = sqlite3.connect("tech_news.db")
    cursor = conn.cursor()

    data_exists_in_table = cursor.execute(
        "SELECT EXISTS(SELECT * from tech_news_data WHERE website_id=?)", (website_id,)
    ).fetchone()[0]
    print("data", data_exists_in_table)
    if data_exists_in_table == 0:
        cursor.executemany(
            """INSERT INTO tech_news_data VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
            web_data_list,
        )
        conn.commit()
    else:
        pass

    # The n value is added to the existing iteration in iteration file
    iteration += n
    with open(iteration_file, "w", encoding="utf-8") as f:
        f.write(str(iteration))


def main():
    """
    main function
    """
    website_rss_feed = [
        "https://siliconangle.com/feed/",
        "https://www.wired.com/feed/rss",
        "https://techcrunch.com/feed/",
    ]
    iteration_file = "iteration.txt"
    try:
        with open(iteration_file, "r", encoding="utf-8") as f:
            iteration = int(f.read().strip())
    except FileNotFoundError:
        iteration = 0

    database_setup()
    parsing(website_rss_feed, iteration_file, 3, iteration)


if __name__ == "__main__":
    main()
