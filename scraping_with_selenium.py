"""
This class is reading immoweb ads.
Most of the methods are private, use them only internally

"""
import time
import os

# from curses import KEY_DOWN, KEY_ENTER
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.common.exceptions import TimeoutException
from selenium import webdriver

# from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

# from selenium.webdriver.support.ui import Select

driver = webdriver.Firefox()


def open_web_page() -> None:
    """Opens a web page for predefined address.
    This module is reading only immoweb ads
    """
    url = "https://www.immoweb.be/en/advanced-search/house/for-sale?\
    countries=BE&page=1&orderBy=relevance"
    driver.implicitly_wait(2)
    driver.get(url)


def select_apartments() -> None:  # TÄMÄKÄÄN EI ENÄÄ TOIMI
    """From drobdown bow we are interested in only 'House' and 'Apartments'
    'House' is selected by default. Call this method if you want to select
    'Apartments'"""
    drop_down = driver.find_element(By.XPATH, "//*[@id='propertyTypes']")
    drop_down.click()
    selection = driver.find_element(By.XPATH, "//*[@id='propertyTypes-item-1']")
    selection.click()


def accept_cookies() -> None:
    """In the website has a dialog that ask us to accept cookies. We have to close
    it. Otherwise is will distract our search"""
    time.sleep(5)
    button = driver.find_elements(By.XPATH, "//*[@id='uc-btn-accept-banner']")
    if button:
        button[0].click()


def exclude_life_annuity_sales() -> None:
    """From drobdown we want to exclude 'life annyuity sales' - items'
    By calling this method, they will be excluded (there are only 135 of them).
    """
    time.sleep(2)
    driver.execute_script(  # The element is not visible on the screen, we have to roll down
        "window.scrollTo(0, document.body.scrollHeight/3.5);"
    )
    time.sleep(2)
    drop_down = driver.find_element(By.XPATH, "//*[@id='isALifeAnnuitySale']")
    drop_down.click()
    time.sleep(2)
    selection = driver.find_element(By.XPATH, "//*[@id='isALifeAnnuitySale-item-1']")
    selection.click()


def read_count() -> int:
    """In the immoweb site is information about how many properties
    are found with current criterias. We need to get that information,
    because it's useful when testing the result that we collected from
    the site. This value is used for testing. We can make sure that we
    have exactly correct amount of html addresses.
    :return: immoweb search result count
    """
    count = driver.find_element(By.XPATH, "//span[@class='button__label-count']")
    value = count.get_attribute("innerHTML")
    value = value.replace("(", "")
    value = value.replace(")", "")
    value = value.replace(",", "")
    value = int(value)
    return value


def select_checkbox(sub_type: str) -> None:
    """
    There is a subtype under housing type. This method selects the checkbox. There
    is one parameter that descripes the subtype name.
    :sub_type: a string that descripes sub_type name. This should be as it's written
    in the immoweb website html code
    """
    time.sleep(2)
    driver.execute_script(  # The element is not visible on the screen, we have to roll
        "window.scrollTo(0, document.body.scrollHeight/7);"
    )
    time.sleep(2)
    check_box = driver.find_element(By.XPATH, f"//label[@for='{sub_type}']")
    check_box.click()
    if check_box.is_selected:  # just to make sure it's really selected
        print("Check box selected:", sub_type)
    else:
        print(f"{sub_type} is not selected, let's try once more")
        check_box.click()


def show_more_sub_type() -> None:
    """In the immoweb site there is a link that opens more
    sub types. It should be opened in order to have access to them
    """
    time.sleep(2)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight/7);")
    print("siirretään ikkunaa!!")
    time.sleep(2)
    show_more = driver.find_element(
        By.XPATH,
        "//*[@class='read-toggle__button button--text read-toggle__button--more']",
    )
    show_more.click()


def press_search() -> None:
    """Locate 'SEARCH'-button and press it."""
    python_button = driver.find_element(
        By.XPATH, "//button[@class='button button--primary form__field-submit__button']"
    )
    python_button.click()
    print("=" * 100, "SEARCH has been pressed")


def __collect_real_ads() -> list:
    """Collect all the links to ads, returns the list. There
    should be 30 ads in one set of links (except in the last page)
    :return : links to the ads"""
    links_to_ads = []
    selenium_results = driver.find_elements(
        By.XPATH,
        "//*[@class='card__title card--result__title']//a[@class='card__title-link']",
    )
    for i in selenium_results:
        links_to_ads.append(i.get_property("href"))
    return links_to_ads


def __open_next_page() -> bool:
    """Moving to the next search page.
    :return: returns false, If there are no more pages. otherwise returns 'True'"""
    next_pages = driver.find_elements(
        By.XPATH,
        "//a[@class='pagination__link pagination__link--next \
            button button--text button--size-small']",
    )
    if not next_pages:
        return False
    url = next_pages[0].get_property("href")
    driver.get(url)
    return True


def save_data(ads: list, apartments: bool, sub_type: str, append: bool = True) -> int:
    """
    this method saves the data to a file
    :ads: list of the https addresses that this class has collected
    :apartments: A boolean value wheter we search apartments of houses
    :sub_type: housing type subtype (checkbox)
    :append: if False, we will delete the file before writing. Otherwise
    append the data to the end of the file
    :return:  returns how many http addresses were saved. This is used
    later to compare the information from web-site.
    """
    housing_type = ""
    if apartments:
        housing_type = "APARTMENT"
    else:
        housing_type = "HOUSE"

    filename = f"{housing_type}_{sub_type}.txt"
    destination_file = os.path.join("data", filename)
    tmp_list = []
    for i in ads:
        tmp_list.append(f"{housing_type}<#COL>{sub_type}<#COL>{i}<#END>")
    if append:
        with open(destination_file, "a", encoding="UTF-8") as my_file:
            my_file.writelines(tmp_list)
    else:
        with open(destination_file, "w", encoding="UTF-8") as my_file:
            my_file.writelines(tmp_list)
    return len(tmp_list)


def write_log(
    search_count: int, saved_count: int, apartments: bool, sub_type: str
) -> None:
    """This module write log how successfully it has been when reading
    data. Parameters:
    :search_count: (int) the number of items in in immoweb search result. This
    is the true value how many items there are and is calculated by immoweb.
    :saved_count: (int) this is how many search results we actually found. This
    should be compared to the search_count. If these differ it's a fial
    :appartments: A boolean value, if true the ad type is 'Appartment', otherwise
    'House'.
    """
    if apartments:
        house_type = "APPARTEMENT"
    else:
        house_type = "HOUSE"
    filename = f"./data/log/{house_type}_{sub_type}.txt"
    log_txt = ""
    if search_count == saved_count:
        log_txt = (
            f"-------------------------------------------------------------------------"
            f"\nOK --- house_type -- sub_type -- {filename} \n"
            f"\n        search result / lines wrote to the file: {search_count} / {saved_count} \n"
            f"-------------------------------------------------------------------------"
        )
    else:
        log_txt = (
            "#####################################################\
            #######################################",
            f"\n#### FAIL!! --- house_type -- sub_type -- {filename} \
                                               ####",
            f"\n####         search result / lines wrote to the file: \
            {search_count} / {saved_count}    ####",
            "\n######################################################\
            ######################################",
        )
    log_file = os.path.join("data", "Scrapping_log.txt")
    with open(log_file, "a", encoding="UTF-8") as log_file:
        log_file.writelines(log_txt)


def read_and_save_immoweb_ads(
    sub_type: str, apartments: bool = False, test: bool = False
) -> None:
    """This is the method where to start the immoweb site search.
    :sub_type: string that is used to select correct checkbox
    :apartments : False by default (Houses are selected), if True, Apartments
    are selected.
    :test : if test is True, only one set of ads will be read (30 ads). Otherwise
    all the pages.
    """
    log_file = os.path.join("data", "Scrapping_log.txt")
    line = "=" * 20, "NEW RUN", "=" * 20, "\n"
    with open(log_file, "a", encoding="UTF-8") as log_file:
        log_file.writelines(line)
    if apartments:
        print("Apartments are selected")
        select_apartments()
    select_checkbox(sub_type)  # example: "FARMHOUSE"
    exclude_life_annuity_sales()
    time.sleep(1)
    press_search()
    time.sleep(2)
    search_count = read_count()
    saved_count = 0
    result = __collect_real_ads()  # First time we want a empty file
    saved_count += save_data(result, apartments, sub_type, False)
    next_page_exists = True
    if not test:
        while next_page_exists:
            next_page_exists = __open_next_page()
            if next_page_exists:
                result = __collect_real_ads()
                saved_count += save_data(result, apartments, sub_type)
    print("Reading worked until the very end")
    write_log(search_count, saved_count, apartments, sub_type)


# This list has all the parameters for
# going through the immoweb sites
# Element 1: bool, False = House, True = Apartment
# Element 2: str,  check box selection, apartment subtype
# Element 3: bool, if True, the data has already loaded and
# should not be loaded again (= skip this selection). Otherwise,
# read the data.
search_criteria = [
    [False, "BUNGALOW", True],
    [False, "CASTLE", True],
    [False, "COUNTRY_COTTAGE", True],
    [False, "APARTMENT_BLOCK", True],
    [False, "TOWN_HOUSE", False],
    [False, "CHALET", True],
    [False, "FARMHOUSE", True],
    [False, "EXCEPTIONAL_PROPERTY", True],
    [False, "MIXED_USE_BUILDING", True],
    [False, "MANSION", True],
    [False, "VILLA", True],
    [False, "MANOR_HOUSE", True],
    [False, "OTHER_PROPERTY", True],
    [False, "PAVILION", True],
    [True, "GROUND_FLOOR", True],
    [True, "TRIPLEX", True],
    [True, "PENTHOUSE", True],
    [True, "KOT", True],
    [True, "DUPLEX", True],
    [True, "FLAT_STUDIO", True],
    [True, "LOFT", True],
    [True, "SERVICE_FLAT", True],
]


def run_the_search() -> None:
    """This is the 'main' method that calls all the other methods."""
    just_testing = False
    for i in search_criteria:
        house_or_apart = i[0]
        sub_type_name = i[1]
        skip = i[2]
        if skip:
            print("skip:", sub_type_name)
            continue
        print(
            "READ THE INFORMATION FOR:\n     - >House: ",
            house_or_apart,
            "/ Sub type: ",
            sub_type_name,
        )
        open_web_page()
        accept_cookies()
        show_more_sub_type()
        read_and_save_immoweb_ads(sub_type_name, house_or_apart, just_testing)
        time.sleep(3)
    driver.close()
    driver.quit()


if __name__ == "__main__":
    run_the_search()
