import streamlit as st
import requests
from bs4 import BeautifulSoup
import json
import pandas as pd

@st.cache
def convert_df(df):
    return df.to_csv().encode('utf-8')

# Add a title to the app
st.title('Image Schema Generator')

# Use an expander to explain the app
with st.expander("See explanation"):
    st.write("""
        This app generates image schema that follows schema.org guidelines. 
        The schema can be used to provide search engines with information about images on a webpage. 
        For more information, please visit the following link: https://schema.org/ImageObject. 
        To generate a schema, paste URLs of the webpages you wish to scrape for images in the text area below.
    """)

# Replace the file uploader with a text area where users can input URLs
url_input = st.text_area("Enter the URLs (one per line)")

# Add a button to generate the image schemas
if st.button('Generate Image Schema'):
    # Split the user's input by newlines to generate a list of URLs
    urls = url_input.split("\n")

    if len(urls) > 0 and urls[0] != '':
        # Initialize a list to store the results
        results = []

        # Iterate over the URLs
        for URL in urls:
            # Send an HTTP GET request to the URL and retrieve the HTML content
            response = requests.get(URL)
            html = response.text

            # Parse the HTML content using Beautiful Soup
            soup = BeautifulSoup(html, 'html.parser')

            # Extract the image objects from the HTML
            images = soup.find_all('img')

            # Initialize a list to store the image schema objects
            image_schemas = []

            # Iterate over the images
            for image in images:
                # Build the image schema using JSON-LD and schema.org guidelines
                image_schema = {
                    "@type":"ImageObject",
                    "name": image.get('alt'),  # Extract the alt text as the name
                    "description": image.get('alt'),  # Extract the alt text as the description
                    "contentUrl": image.get('src'),  # Use the get method to safely retrieve the src
                }
                # Only add the height and width fields if they are present
                height = image.get('height')
                if height is not None:
                    image_schema['height'] = height
                width = image.get('width')
                if width is not None:
                    image_schema['width'] = width
                # Add the image schema object to the list if the src attribute is present
                if image_schema['contentUrl'] is not None:
                    image_schemas.append(image_schema)

            # Build the main schema object
            schema = {
                "@context": "https://schema.org",
                "@type": "ImageObject",
                "url": URL,
                "image": image_schemas,
            }

            # Convert the schema object to a JSON-LD string
            json_ld = json.dumps(schema)

            # Add the URL and schema markup to the results list
            results.append((URL, json_ld))

        # Create a new DataFrame from the results list
        df_results = pd.DataFrame(results, columns=['url', 'img_schema'])

        # Set the filename for the downloaded CSV file
        filename = 'image_schemas_' + str(pd.to_datetime('today').date()) + '.csv'

        # Save the DataFrame as a CSV file and download it
        csv = convert_df(df_results)
        st.session_state.data = csv  # save the data in the session state

# Add the download button outside the 'Generate Image Schema' button
# It only appears if there is data to download
if 'data' in st.session_state:
    st.download_button(
        label="Download data as CSV",
        data=st.session_state.data,
        file_name='image_schemas_' + str(pd.to_datetime('today').date()) + '.csv',
        mime='text/csv',
    )
