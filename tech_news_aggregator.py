import sqlite3
import feedparser
import tldextract
import requests


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
            # If there is a value in image_url field, the condition gets the value from the URL
            # If an error arises, a message is assigned to the variable
            try:
                if image_url:
                    image_url = image_url[0]["url"]
                else:
                    image_url = "Data not present"
            except (KeyError, TypeError):
                image_url = "Data not present"
            print("image_url=", image_url)
            published_at = feed_data.get("published", "Data not present")

            conn = sqlite3.connect("tech_news.db")
            cursor = conn.cursor()

            data_exists_in_table = cursor.execute(
                "SELECT EXISTS(SELECT * from tech_news_data WHERE website_id=?)",
                (website_id,),
            ).fetchone()[0]
            print("data", data_exists_in_table)
            if data_exists_in_table == 0:
                cursor.execute(
                    """INSERT INTO tech_news_data VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                    (
                        website_id,
                        author,
                        title,
                        content,
                        website_url,
                        website_name,
                        image_url,
                        published_at,
                    ),
                )
                conn.commit()
            else:
                pass

    # The n value is added to the existing iteration in the iteration file
    iteration += n
    with open(iteration_file, "w", encoding="utf-8") as f:
        f.write(str(iteration))


def fetch_rss_feed_from_file(sites_file="sites.txt"):
    """
    Fetches RSS feed URLs from a file containing website URLs

    """
    website_rss_feed = []

    try:
        with open(sites_file, "r", encoding="utf-8") as f:
            website_data = f.readlines()
            if website_data:
                for data in website_data:
                    rss_feed_url = fetch_rss_feed(data.strip("\n"))
                    if rss_feed_url:
                        if rss_feed_url not in website_rss_feed:
                            website_rss_feed.append(rss_feed_url)
                        elif rss_feed_url in website_rss_feed:
                            pass
                    else:
                        print(f"No RSS Feed URL found for {data}")
    except FileNotFoundError:
        print("File sites.txt not found.")
    except Exception as e:
        print(f"An error occurred: {e}")
    return website_rss_feed


def fetch_rss_feed(url):
    """
    Fetches the RSS feed URL from a given website URL.

    """
    try:
        response = requests.get(url)
        response.raise_for_status()

        html_content = response.text
        target_string = '<link rel="alternate" type="application/rss+xml"'
        start_index = html_content.find(target_string)

        if start_index != -1:
            end_index = html_content.find(">", start_index)
            link_element = html_content[start_index : end_index + 1]
            href_start = link_element.find('href="') + len('href="')
            href_end = link_element.find('"', href_start)
            rss_feed_url = link_element[href_start:href_end]
            return rss_feed_url
        else:
            print("No RSS Feed URL found in the HTML.")
            return None

    except requests.exceptions.RequestException as e:
        print(f"Error fetching RSS feed from {url}: {e}")
        return None


def main():
    """
    main function
    """
    website_rss_feed = fetch_rss_feed_from_file(sites_file="sites.txt")
    print(website_rss_feed)
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
