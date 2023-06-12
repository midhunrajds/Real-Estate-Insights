# Import the necessary libraries
import requests  # Library for making HTTP requests
from bs4 import BeautifulSoup  # Library for parsing HTML
import pandas as pd  # Library for data manipulation and analysis

# Step 1: Function for extracting
def extract(page):
    # Define headers for the HTTP request
    headers = {'User-Agent': 'My user agent'}

    # Make an HTTP request to fetch the web page
    url = f'https://www.bayut.com/for-sale/property/uae/page-{page}'

    r = requests.get(url, headers)  # Send a GET request to the URL
    soup = BeautifulSoup(r.content, 'html.parser')  # Create a BeautifulSoup object to parse the HTML content
    return soup

# Step 2: Function for transforming to dataframe.
def transform(soup):
    
    divs = soup.find_all('div', class_='d6e81fd0')  # Find all div elements with the specified class name
    
    # Extract relevant attributes from the HTML
    for item in divs:
        title = item.find('h2').text.strip()  # Extract the text of the h2 element
        location = item.find('div', class_='_7afabd84').text.strip()  # Extract the text of the div element with the specified class
        typ = item.find('div', class_='_9a4e3964').text.strip()  # Extract the text of the div element with the specified class
        bed_bath_area = []
        for items2 in item.find_all('span', class_='b6a29bc0'):
            try:
                bed_bath_area.append(items2.text)  # Extract the text of the span element
            except:
                bed_bath_area.append('')  # Append an empty string if the extraction fails
        price = item.find('span', class_='f343d9ce').text.strip()  # Extract the text of the span element with the specified class

        # Create a dictionary with the extracted attributes
        apt = {
            'title': title,
            'location': location,
            'type': typ,
            'bed': bed_bath_area[0],
            'bath': bed_bath_area[1],
            'area': bed_bath_area[2],
            'price': price
        }

        # Step 4: Append the dictionary to the aptlist
        aptlist.append(apt)
        # No return statement is needed as the `aptlist` is a global list variable

# Step 3: Create an empty list to store the dictionaries
aptlist = []

# Step 4: Iterate through the pages to scrape multiple pages
for i in range(2500):
    print(f'Getting page {i}')
    try:
        c = extract(i)
        transform(c)
    except:
        continue

# Step 5: Create a DataFrame from the aptlist
df = pd.DataFrame(aptlist)

# Step 6: Data cleaning and preprocessing

# Clean the 'area' attribute by removing commas and converting it to a numerical value
df['area'] = df['area'].str.replace(',', '').str.extract(r'(\d+)').astype(float) 

df['Neighbourhood'] = ''
df['District'] = ''
df['State'] = ''

# Extract location information from the 'location' column
for index, row in df.iterrows():
    strings = row['location'].split(',')  # Split the location string by comma
    if len(strings) >= 3:
        df.at[index, 'Neighbourhood'] = strings[-3].strip()  # Assign the last but two string to the 'Neighbourhood' column
        df.at[index, 'District'] = strings[-2].strip()  # Assign the last but one string to the 'District' column
        df.at[index, 'State'] = strings[-1].strip()  # Assign the last string to the 'State' column


df.to_csv('csv.csv')  # Save the DataFrame to a CSV file
