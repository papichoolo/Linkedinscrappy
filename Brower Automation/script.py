from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import csv
import time
import os
import getpass
# Function to initialize a Chrome browser with Selenium
def init_browser():
    options = webdriver.ChromeOptions()
    # Add any additional options as needed
    browser = webdriver.Chrome(options=options)
    return browser

# Function to login to LinkedIn
def login_to_linkedin(browser, username, password):
    browser.get("https://www.linkedin.com/login")
    time.sleep(2)  # Allow time for the page to load
    
    # Find the username and password fields and login button
    username_field = browser.find_element(By.ID, "username")
    password_field = browser.find_element(By.ID, "password")
    login_button = browser.find_element(By.CSS_SELECTOR, ".login__form_action_container button")

    # Input username and password
    username_field.send_keys(username)
    password_field.send_keys(password)

    # Click the login button
    login_button.click()

    time.sleep(10)  # Allow time for the page to load

# Function to search for users on LinkedIn
def search_linkedin_users(browser, search_query):
    search_box = browser.find_element(By.CSS_SELECTOR, "input.search-global-typeahead__input")
    search_box.send_keys(search_query)
    search_box.send_keys(Keys.RETURN)
    time.sleep(5)
    people_button= browser.find_element(By.CLASS_NAME,'artdeco-pill--choice')
    people_button.click()
    time.sleep(2)
    

# Function to extract user data from search results
def extract_user_data(browser):
    # Wait for the search results to load
    time.sleep(5)

    # Get the page source and parse it with BeautifulSoup
    page_source = browser.page_source
    soup = BeautifulSoup(page_source, 'html.parser')

    # Extract user data from the search results
    user_data_list = []
    title_list=[]
    search_results = soup.find_all("li", class_="reusable-search__result-container")

    user_data_list = []  # Initialize an empty list to store user data

    for result in search_results[:10]:  # Only consider the first 10 search results
        # Find the span element within the current result
        name_element = result.find('span', {'aria-hidden': 'true'})
        name = name_element.get_text(strip=True) if name_element else "N/A"

        primary_title_element = result.find("div", class_="entity-result__primary-subtitle t-14 t-black t-normal")
        primary_title = primary_title_element.get_text(strip=True) if primary_title_element else "N/A"

        secondary_title_element = result.find("div", class_="entity-result__secondary-subtitle t-14 t-normal")
        secondary_title=secondary_title_element.get_text(strip=True) if secondary_title_element else "N/A"
        # You can extract other information such as job title, company, etc., based on your needs

        user_data = {
            "Name": name,
            "Title": primary_title,
            "Location": secondary_title
            # Add other fields as needed
        }
        user_data_list.append(user_data)

    return user_data_list
    


    

# Function to save user data to a CSV file
def save_to_csv(user_data_list, csv_filename):
    with open(csv_filename, mode='w', newline='', encoding='utf-8') as csv_file:
        fieldnames = ["Name","Title","Location"]  # Add other field names as needed
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()

        for user_data in user_data_list:
            writer.writerow(user_data)

if __name__ == "__main__":
    # Set your LinkedIn credentials
    linkedin_username = str(input("Enter Email:"))
    linkedin_password = getpass.getpass("Enter Password:")

    # Set the search query
    search_query = str(input("Enter Name to search: "))  # Replace with the desired user's name

    # Set the filename for the CSV file
    csv_filename = "linkedin_data.csv"

    # Initialize the browser and perform actions
    browser = init_browser()
    login_to_linkedin(browser, linkedin_username, linkedin_password)
    search_linkedin_users(browser, search_query)
    user_data_list = extract_user_data(browser)
    save_to_csv(user_data_list, csv_filename)

    # Close the browser
    browser.quit()
