# Import the required packages
import pandas as pd
import googlemaps # Importing the googlemaps library for geocoding functionality
from datetime import datetime  

gmaps = googlemaps.Client(key='xxxxxxxxxxxxxxxxxxxxxxxxxxx')  # Initialize the Google Maps client
df = pd.read_csv('~//bsv.csv')  # Read the CSV file containing the locations

df['Latitude'] = ''  # Create empty columns for latitude
df['Longitude'] = ''  # Create empty columns for longitude

for index, row in df.iterrows():
    address = row['location']  # column name containing addresses
    
    # Geocode the address using Google Maps API
    geocode_result = gmaps.geocode(address)
    
    if geocode_result:
        # Extract latitude and longitude
        latitude = geocode_result[0]['geometry']['location']['lat']
        longitude = geocode_result[0]['geometry']['location']['lng']
        
        # Update the DataFrame with the coordinates
        df.at[index, 'Latitude'] = latitude
        df.at[index, 'Longitude'] = longitude

# Print the updated DataFrame
print(df)

df.to_csv('results.csv')  # Save the DataFrame to a CSV file
