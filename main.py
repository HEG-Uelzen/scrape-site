import os
from pathlib import Path
import requests

from bs4 import BeautifulSoup
import feedparser

def main():
    CURRENT_DIR = str(Path.cwd().absolute())
    FEED_URL = "https://heg-uelzen.de/hpp/rss.xml"

    feed = feedparser.parse(FEED_URL)

    feeditems = feed['entries']

    # create directory for later downloaded data
    datapath = "./data" # os.path.join(CURRENT_DIR, "data")

    # iterate over feed items to fetch them
    for item in feeditems:
        # create directory for the post
        dirname = item.id.replace(" at https://heg-uelzen.de/hpp", "") + "--" + item.title.replace(" ", "_") 
        newpath = datapath + "/" + dirname # os.path.join(datapath, dirname)
        try: 
            os.makedirs(newpath, 0o777)
            print("Created Directory '% s' " % newpath)
        except OSError as error: 
            print(error)

        # get & write post content to (txt) file
        res = requests.get(item.link)
        soup = BeautifulSoup(res.content, 'html.parser')
        title = soup.title.text.replace(" | Herzog-Ernst-Gymnasium", "")
        content = soup.find('div', class_="node__content")

        try:
            with open(newpath + "/" + "_post.html", "w+") as output_file:
                output_file.write(str(content))
                output_file.close()
                print("Wrote output file for '% s'" % title)
        except OSError as error:
            print(error)


        # get files included in the post
        link_elements = content.find_all('a')
        for element in link_elements:
            # extraction of pdf files
            if ".pdf" in element.get('href'):
                link = "https://heg-uelzen.de" + element.get('href')
                filename = link.split("/")[-1]
                response = requests.get(link)
                pdf = open(newpath + "/" +filename, "wb")
                pdf.write(response.content)
                pdf.close()
                print("File " + filename + " downloaded")

            # TODO: extraction of image files

    print("Finished!")
    


if __name__ == "__main__":
    main()