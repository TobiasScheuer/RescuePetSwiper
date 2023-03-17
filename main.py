import requests
from bs4 import BeautifulSoup as bs4

#--# Goals #--#
# create tinder style app to find rescue pets
# how to find websites:
#    google maps: "tierheim
#    firstly: manual search, manual evaluation, manual adding of URL to DB
#



def parse_homepage(homepage_url:str) -> dict:
    categories = dict()
    categories["kleine Hunde"] = list()
    categories["mittlere Hunde"] = list()
    categories["grosse Hunde"] = list()
    categories["sachkundigen Hunde"] = list()
    categories["sonstige Hunde"] = list()
    home_page = requests.get(homepage_url)
    parsed_page = bs4(home_page.content, "html.parser")
    navigation_tags = parsed_page.find_all("nav")
    for counter, nav_tag in enumerate(navigation_tags):
        submenus = nav_tag.find_all(class_="sub-menu")
        for counter2, sub_menu_tag in enumerate(submenus):
            links = sub_menu_tag.find_all("li")
            for entries in links:
                span_text = entries.find("span").text
                if "Hund" in span_text or "hund" in span_text: #"Hund" also finds "Hunde" and other extended strings
                    hrefs = entries.find("a")
                    href = hrefs["href"]
                    if href == "#" or href == "None":
                        pass
                    else:   
                        if hrefs.text == "Große Hunde":
                            currentlist = categories["grosse Hunde"]
                            if href not in currentlist:
                                currentlist.append(href)
                                categories["grosse Hunde"] = currentlist
                        elif hrefs.text == "Mittlere Hunde":
                            currentlist = categories["mittlere Hunde"]
                            if href not in currentlist:
                                currentlist.append(href)
                                categories["mittlere Hunde"] = currentlist
                        elif hrefs.text == "Kleine Hunde":
                            currentlist = categories["kleine Hunde"]
                            if href not in currentlist:
                                currentlist.append(href)
                                categories["kleine Hunde"] = currentlist
                        elif hrefs.text == "Hunde für Sachkundige":
                            currentlist = categories["sachkundigen Hunde"]
                            if href not in currentlist:
                                currentlist.append(href)
                                categories["sachkundigen Hunde"] = currentlist
                        else:
                            currentlist = categories["sonstige Hunde"]
                            if href not in currentlist:
                                currentlist.append(href)
                                categories["sonstige Hunde"] = currentlist
                #elif "Katzen" ?
    return categories

def parse_category(category_url:str) -> dict:
    pet_dict = dict()
    category_page = requests.get(category_url)
    parsed_page = bs4(category_page.content, "html.parser")
    div_img = parsed_page.find_all("div", attrs={"class":"cmsms_img_rollover"})
    for counter, entry in enumerate(div_img):
        img_tag = entry.find("a", attrs={"class":"cmsms_image_link"})
        img_link = img_tag["href"]
        link_tag = entry.find("a", attrs={"class":"cmsms_open_link"})
        link = link_tag["href"]
        pet_name = link_tag["title"]
        pet_dict[link] = {"pet name": pet_name, "image link": img_link}
    return pet_dict

def main():
    pet_dictionary = dict()
    url = "https://www.tierheim-leipzig.de/"
    homepage_categories = parse_homepage(url)
    for counter, entry in enumerate(homepage_categories):
        new_pet_dict  = parse_category(homepage_categories[entry][0])
        for counter, pet_link in enumerate(new_pet_dict):
            if pet_link in pet_dictionary.keys():
                print(pet_link)
            else:
                pass

    print(homepage_categories) # hier weiter

if __name__ == "__main__":
    main()
