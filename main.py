import os
from pathlib import Path

import feedparser

def main():
    CURRENT_DIR = str(Path.cwd().absolute())
    FEED_URL = "https://heg-uelzen.de/hpp/rss.xml"

    feed = feedparser.parse(FEED_URL)

    feeditems = feed['entries']

    # create directory for later downloaded data
    datapath = os.path.join(CURRENT_DIR, "data")
    print(datapath)

    # iterate over feed items to fetch them
    for item in feeditems:
        # create directory for the post
        dirname = item.title.replace(" ", "_")
        newpath = os.path.join(datapath, dirname)
        try: 
            os.makedirs(newpath, 0o666)
            print("Directory '% s' created" % newpath)
        except OSError as error: 
            print(error)  

        # write post content to (txt) file

        # get image of the post and download it into the directory

    


if __name__ == "__main__":
    main()