import os
from pathlib import Path
import requests
import wget

from bs4 import BeautifulSoup
import feedparser


def main():
    GET_EXTENDED_FEED = input("Do you want to get the latest 20 instead of 10 posts? ").lower()
    CURRENT_DIR = str(Path.cwd().absolute())
    FEED_URL = "https://heg-uelzen.de/hpp/rss.xml"

    feed = feedparser.parse(FEED_URL)

    feeditems = feed['entries']

    # create directory for later downloaded data
    datapath = "./data"  # os.path.join(CURRENT_DIR, "data")

    # iterate over feed items to fetch them
    for item in feeditems:
        # create directory for the post
        dirname = item.id.replace(
            " at https://heg-uelzen.de/hpp", "") + "--" + item.title.replace(" ", "_").replace("/", "-").replace("!", "")
        newpath = datapath + "/" + dirname  # os.path.join(datapath, dirname)
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
                pdf = open(newpath + "/" + filename, "wb")
                pdf.write(response.content)
                pdf.close()
                print("File " + filename + " downloaded")

        # extraction of image files
        image_elements = content.find_all('img')
        for image in image_elements:
            image_link = "https://heg-uelzen.de" + \
                image.get('src').split("?")[0]
            img_filename = image_link.split("/")[-1]
            img_download = wget.download(
                image_link, out=newpath + "/" + img_filename)
            print("\nDownloaded image: " + img_download)

        print("\n")

    if GET_EXTENDED_FEED.startswith("y") or GET_EXTENDED_FEED.startswith("j"):
        print("Getting extended feed...")
        NEWSPAGE_TWO = "https://heg-uelzen.de/hpp/?page=1"

        page_two_res = requests.get(NEWSPAGE_TWO)
        page_two_soup = BeautifulSoup(page_two_res.content, 'html.parser')
        page_two_list = page_two_soup.find_all('div', class_="views-row")

        for post in page_two_list:
            post_title = post.find('span', class_="field field--name-title field--type-string field--label-hidden").text
            
            post_id = post.find('article', class_="node node--type-article node--promoted node--view-mode-teaser").get('data-history-node-id')

            dirname = post_id + "--" + post_title.replace(" ", "_").replace("/", "-").replace("!", "")
            newpath = datapath + "/" + dirname

            try:
                os.makedirs(newpath, 0o777)
                print("Created Directory '% s' " % newpath)
            except OSError as error:
                print(error)
            page_url = "https://heg-uelzen.de/hpp/node/" + str(post_id)
            page = requests.get(page_url)
            
            page_soup = BeautifulSoup(page.content, 'html.parser')
            title = page_soup.title.text.replace(" | Herzog-Ernst-Gymnasium", "")
            content = page_soup.find('div', class_="node__content")

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
                    pdf = open(newpath + "/" + filename, "wb")
                    pdf.write(response.content)
                    pdf.close()
                    print("File " + filename + " downloaded")

            # extraction of image files
            image_elements = content.find_all('img')
            for image in image_elements:
                image_link = "https://heg-uelzen.de" + image.get('src').split("?")[0]
                img_filename = image_link.split("/")[-1]
                try:
                    img_download = wget.download(image_link, out=newpath + "/" + img_filename)
                    print("\nDownloaded image: " + img_download)
                except Exception as err:
                    print("ERROR: "+ str(err))


    print("\nFinished!")


if __name__ == "__main__":
    main()
