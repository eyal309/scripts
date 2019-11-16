import os
import requests
import concurrent.futures
from bs4 import BeautifulSoup
from itertools import groupby


url = "https://en.wikipedia.org/wiki/List_of_animal_names"


def download_img(img_url: str):
    """
    method to download an image from a given url and save it in /temp/
    :param img_url: <class str.> url to image
    :return: None
    """
    img_link = requests.get(f"https://en.wikipedia.org/{img_url}").content
    soup = BeautifulSoup(img_link, 'html.parser')
    find_content = soup.find_all("table")[0]  # find the first table in page
    find_image = find_content.find_all("img")  # find the image inside
    img_link = requests.get(find_image[0]["src"].replace('//', 'http://')).content  # convert the link in src to valid
    img_name = f"{img_url.split('/')[-1]}.jpg"  # create var for the file name
    path = os.getcwd()  # get the current path
    try:
        os.mkdir(f"{path}/tmp")  # create tmp directory
    except FileExistsError:
        pass  # if its already exists continue
    with open(f"tmp/{img_name}", "wb") as img_file:
        img_file.write(img_link)  # download the image


def scrape_table_data(table_url: str):
    """
    method to get only the animals and collateral adjective from the web page
    and download all of their images
    :param table_url: <class str.> link to the web page
    :return: list of dictionaries [{"collateral_adjective": adjective, "animal": animal, "image_link": link}]
    """
    new_table = []
    image_links = []
    response = requests.get(table_url)  # connect to the web page
    soup = BeautifulSoup(response.content, 'html.parser')  # get the content of the page
    table = soup.find_all("table")[2]  # find the third table in the page
    rows = table.select("tbody tr")  # select the table rows
    for row in rows:
        data = [tr.text.rstrip() for tr in row.find_all("td")]  # get a list of all rows content
        img_links = [link.get("href") for link in row.find_all("a")]
        if data:
            try:
                animal = data[0].split()[0]  # get the animal name
                animal = animal.split('[')[0]
                img_link = img_links[0]
                if not data[5].split() or '?' in data[5].split():  # get the collateral adjective list
                    collateral_adjective = ["unknown"]
                else:
                    collateral_adjective = data[5].split()
            except IndexError:  # in case there is no collateral adjective in the row continue the loop
                continue

            for adjective in collateral_adjective:  # iter over the the collateral adjective list
                adjective = adjective.split('[')[0]
                obj = {"collateral_adjective": adjective, "animal": animal, "image_link": f"tmp/{img_link.split('/')[-1]}.jpg"}
                new_table.append(obj)  # create a list of dictionaries
                image_links.append(img_link)  # append the local path to image
                
    with concurrent.futures.ThreadPoolExecutor() as executor:  # create thread for each link
        executor.map(download_img, image_links)  # download the images simultaneously
        
    return new_table


def sort_table_data(data):
    """
    method to group and sort all of the uniq collateral adjectives and all of the animals belong to it
    :param data: <class list> list of dictionaries from the scrape_table_data func
    :return:list of dictionaries [{"collateral_adjective": adjective, "animal": [list of animal], "image_link": [links]}]
    """
    new_table = []
    key_func = lambda k: k["collateral_adjective"]  # create sort by collateral_adjective func
    for adj, k in groupby(sorted(data, key=key_func), key=key_func):
        # iter over the adjectives and the groupby generator
        obj = {"collateral_adjective": adj, "animal": [], "image_link": []}
        for adjective in k:  # iter over each adjective in the groupby generator
            if not obj["collateral_adjective"]:
                obj["collateral_adjective"] = adjective["collateral_adjective"]  # append the adjective
            obj["animal"].append(adjective["animal"])  # append the animal name to the names list
            obj["image_link"].append(adjective["image_link"])  # append the animal image link to the names list
        new_table.append(obj)
    return new_table


if __name__ == '__main__':
    
    data_to_sort = scrape_table_data(url)
    sorted_data = sort_table_data(data_to_sort)
    print(sorted_data)
