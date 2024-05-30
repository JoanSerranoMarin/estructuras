import urllib.request
from bs4 import BeautifulSoup
import re
import urllib.parse
import requests
import urllib.request
compuestos = ["pyruvate", "alanine", "glycine", "serotonin", "dopamine"]
link_imagenes = []
url= 'https://pubchem.ncbi.nlm.nih.gov/compound/'
urls_base = []
for i in compuestos:
    urls = urls_base.append(('{}{}'.format(url, i)))



link_imagenes = []
link_smiles = []

for i in urls_base:
    webUrl = urllib.request.urlopen(i)
    html_content = webUrl.read()
    html_content = html_content.decode('utf-8')
    soup = BeautifulSoup(html_content, 'html.parser')
    og_image_tag = soup.find('meta', {'property': 'og:image'})
    og_image_tag = soup.find('meta', {'property': 'og:image'})
    rdf_link_tag = soup.find('link', {'type': 'application/rdf+xml'})
    og_image_content = og_image_tag.get('content')
    print(og_image_content)
    link_imagenes.append(og_image_content)
    rdf_link = rdf_link_tag.get('href')
    print(rdf_link)
    link_smiles.append(rdf_link)


print(link_imagenes)
print(link_smiles)

cids = []

for i in link_smiles:
    match = re.search(r'[^/]+$', i.strip())  # Strip any leading or trailing spaces
    last_part = match.group(0)
    cids.append(last_part)
print(cids)




### A partir de aquí queremos importar los canonical smiles
url_final = []
for i in cids:
    url1= 'https://pubchem.ncbi.nlm.nih.gov/rest/rdf/descriptor/'
    url2= '_Canonical_SMILES'
    url_final.append(('{}{}{}'.format(url1, i, url2)))

print(url_final)

# Function to extract chemical structure from a given URL
def extract_chemical_structure(url):
    try:
        # Fetch the HTML content
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad status codes
        
        # Parse HTML content with BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Find the span element with the chemical structure
        chemical_structure_span = soup.find('span', class_='value')
        if chemical_structure_span:
            return chemical_structure_span.text
        else:
            return "No chemical structure found."
    
    except requests.exceptions.RequestException as e:
        return f"Error fetching {url}: {e}"

# Iterate over the list of URLs and extract information
smiles = []
for url in url_final:
    chemical_structure = extract_chemical_structure(url)
    print(f"Chemical Structure: {chemical_structure}")
    smiles.append(chemical_structure)

print(smiles)
print(link_imagenes)
print(link_smiles)

cids_numeros = [entry[3:] for entry in cids]
print(cids)
print(cids_numeros)

## A partir de aquí quiero descargar las imágenes
def download_image(url, save_as):
    urllib.request.urlretrieve(url, save_as)

for i,j in zip(link_imagenes, cids_numeros):
    image_url_1 = 'https://pubchem.ncbi.nlm.nih.gov/image/imgsrv.fcgi?cid='
    image_url_2 = '&t=l'
    image_url_final = ('{}{}{}'.format(image_url_1, j, image_url_2))
    print(image_url_final)
    save_as = ('{}{}'.format(j, ".png"))
    download_image(image_url_final, save_as)







from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Image, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors



image_paths = []

for i in cids_numeros:
    parte_1_directorio = "C:/Users/joan.serrano.marin/"
    parte_2_directorio = ".png"
    image_directorio = ('{}{}{}'.format(parte_1_directorio, i, parte_2_directorio))
    image_paths.append(image_directorio)


letters = compuestos


# Create a PDF document
pdf_path = "letters_and_images_2.pdf"
doc = SimpleDocTemplate(pdf_path, pagesize=letter)

# Prepare the table data
data = []
for letter, image_path in zip(letters, image_paths):
    # Create a paragraph for the letter
    styles = getSampleStyleSheet()
    letter_paragraph = Paragraph(letter, styles['Normal'])
    
    # Create an image object
    img = Image(image_path)
    img.drawHeight = 150  # Set the height of the image
    img.drawWidth = 150   # Set the width of the image
    
    # Append the row to the data list
    data.append([letter_paragraph, img])

# Create the table
table = Table(data)

# Add a simple table style
table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), colors.white),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    ('FONTSIZE', (0, 0), (-1, 0), 14),
    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
    ('BACKGROUND', (0, 1), (-1, -1), colors.white),
    ('GRID', (0, 0), (-1, -1), 1, colors.grey),
]))

# Build the PDF
doc.build([table])

print(f"PDF created successfully and saved as {pdf_path}")