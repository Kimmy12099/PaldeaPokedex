import os
import requests
from PIL import Image
from io import BytesIO
from bs4 import BeautifulSoup

# URL of the page containing the unobtainable Pokémon list
url = 'https://pokemondb.net/scarlet-violet/unobtainable'

# Directory to save the images
image_dir = 'Unobtainable_Pokemon_Images'
os.makedirs(image_dir, exist_ok=True)

# Fetch the HTML content of the page
response = requests.get(url)
if response.status_code != 200:
    print("Failed to retrieve the webpage.")
    exit()

soup = BeautifulSoup(response.content, 'html.parser')

# Find all Pokémon listed on the page
pokemon_elements = soup.find_all('a', class_='ent-name')

# Function to download, process, and save the image as PNG with transparent background
def download_image(pokemon_name, gender=''):
    # Pokémon Database uses a consistent image URL pattern for Pokémon images
    base_url = 'https://img.pokemondb.net/artwork/large/'
    # Handle gender variations if needed
    image_url = f'{base_url}{pokemon_name.lower().replace(" ", "-")}{gender}.jpg'
    image_path = os.path.join(image_dir, f'{pokemon_name}{gender}.png')

    print(f'Trying URL: {image_url}')  # Debugging line to check URLs

    response = requests.get(image_url)
    if response.status_code == 200:
        # Open the image with Pillow
        image = Image.open(BytesIO(response.content))
        # Convert the image to PNG with a transparent background
        image = image.convert("RGBA")  # Convert to RGBA (including alpha channel)
        data = image.getdata()

        # Create a new image data list to store modified pixel data
        new_data = []
        for item in data:
            # Change all white pixels to transparent
            if item[:3] == (255, 255, 255):
                new_data.append((255, 255, 255, 0))  # RGBA with 0 alpha (transparent)
            else:
                new_data.append(item)

        # Update image data with new data
        image.putdata(new_data)
        # Save the image with a transparent background
        image.save(image_path, 'PNG')
        print(f'Downloaded and processed to PNG with transparent background: {pokemon_name}{gender}')
    else:
        print(f'Failed to download: {pokemon_name}{gender} from {image_url}')

# Iterate through the Pokémon list and download images
for pokemon in pokemon_elements:
    pokemon_name = pokemon.text.strip()
    # Download image for the Pokémon without gender sign
    download_image(pokemon_name)
    # Download image with male sign (if available)
    download_image(pokemon_name, '-male')
    # Download image with female sign (if available)
    download_image(pokemon_name, '-female')
