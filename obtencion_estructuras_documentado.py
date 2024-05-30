# Importar los módulos necesarios
import urllib.request
from bs4 import BeautifulSoup
import re
import urllib.parse
import requests
import urllib.request

# Lista de compuestos químicos
compuestos = ["pyruvate", "alanine", "glycine", "serotonin", "dopamine"]

# Lista para almacenar las URL de las imágenes de los compuestos
link_imagenes = []

# URL base para la búsqueda de compuestos en PubChem
url= 'https://pubchem.ncbi.nlm.nih.gov/compound/'

# Lista para almacenar las URL completas de cada compuesto
urls_base = []

# Generar las URL completas para cada compuesto y agregarlas a la lista
for i in compuestos:
    urls_base.append(('{}{}'.format(url, i)))

# Lista para almacenar los enlaces RDF de los compuestos
link_smiles = []

# Obtener los enlaces RDF y las URL de las imágenes para cada compuesto
for i in urls_base:
    # Abrir la URL y obtener el contenido HTML
    webUrl = urllib.request.urlopen(i)
    html_content = webUrl.read()
    html_content = html_content.decode('utf-8')
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Encontrar la etiqueta meta con la propiedad 'og:image' para obtener la URL de la imagen
    og_image_tag = soup.find('meta', {'property': 'og:image'})
    og_image_content = og_image_tag.get('content')
    link_imagenes.append(og_image_content)  # Agregar la URL de la imagen a la lista
    
    # Encontrar la etiqueta link con el tipo 'application/rdf+xml' para obtener el enlace RDF
    rdf_link_tag = soup.find('link', {'type': 'application/rdf+xml'})
    rdf_link = rdf_link_tag.get('href')
    link_smiles.append(rdf_link)  # Agregar el enlace RDF a la lista

# Imprimir las listas de URL de imágenes y enlaces RDF
print(link_imagenes)
print(link_smiles)

# Lista para almacenar los ID de los compuestos
cids = []

# Extraer los ID de los compuestos de los enlaces RDF y agregarlos a la lista
for i in link_smiles:
    match = re.search(r'[^/]+$', i.strip())  # Buscar el ID del compuesto en el enlace RDF
    last_part = match.group(0)
    cids.append(last_part)

# Imprimir los ID de los compuestos
print(cids)

# Crear las URL finales para obtener los Canonical SMILES de cada compuesto
url_final = []
for i in cids:
    url1= 'https://pubchem.ncbi.nlm.nih.gov/rest/rdf/descriptor/'
    url2= '_Canonical_SMILES'
    url_final.append(('{}{}{}'.format(url1, i, url2)))

# Imprimir las URL finales
print(url_final)

# Función para extraer la estructura química de una URL dada
def extract_chemical_structure(url):
    try:
        # Enviar una solicitud HTTP y obtener el contenido HTML
        response = requests.get(url)
        response.raise_for_status()  # Generar un error para códigos de estado HTTP incorrectos
        
        # Analizar el contenido HTML con BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Encontrar el elemento span con la estructura química
        chemical_structure_span = soup.find('span', class_='value')
        if chemical_structure_span:
            return chemical_structure_span.text
        else:
            return "No se encontró estructura química."
    
    except requests.exceptions.RequestException as e:
        return f"Error al obtener {url}: {e}"

# Lista para almacenar los Canonical SMILES de los compuestos
smiles = []

# Iterar sobre las URL finales y extraer la información
for url in url_final:
    chemical_structure = extract_chemical_structure(url)
    print(f"Estructura química: {chemical_structure}")
    smiles.append(chemical_structure)

# Imprimir los Canonical SMILES
print(smiles)
# Imprimir las listas de URL de imágenes y enlaces RDF
print(link_imagenes)
print(link_smiles)

# Lista para almacenar los ID de los compuestos sin el prefijo 'cid'
cids_numeros = [entry[3:] for entry in cids]

# Imprimir las listas de ID de compuestos con y sin el prefijo 'cid'
print(cids)
print(cids_numeros)



from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Image, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors




# Función para descargar una imagen desde una URL y guardarla localmente
def download_image(url, save_as):
    urllib.request.urlretrieve(url, save_as)

# Descargar las imágenes asociadas a los compuestos
for i, j in zip(link_imagenes, cids_numeros):
    image_url_1 = 'https://pubchem.ncbi.nlm.nih.gov/image/imgsrv.fcgi?cid='
    image_url_2 = '&t=l'
    image_url_final = ('{}{}{}'.format(image_url_1, j, image_url_2))
    print(image_url_final)
    save_as = ('{}{}'.format(j, ".png"))
    download_image(image_url_final, save_as)

# Lista para almacenar las rutas de las imágenes descargadas
image_paths = []

# Construir las rutas de las imágenes descargadas
for i in cids_numeros:
    parte_1_directorio = "C:/Users/joan.serrano.marin/"
    parte_2_directorio = ".png"
    image_directorio = ('{}{}{}'.format(parte_1_directorio, i, parte_2_directorio))
    image_paths.append(image_directorio)

# Lista de letras asociadas a los compuestos
letters = compuestos

# Crear un documento PDF
pdf_path = "letters_and_images_3.pdf"
doc = SimpleDocTemplate(pdf_path, pagesize=letter)

# Preparar los datos de la tabla para el PDF
data = []
for letter, image_path, smile in zip(letters, image_paths, smiles):
    # Crear un párrafo para la letra
    styles = getSampleStyleSheet()
    letter_paragraph = Paragraph(letter, styles['Normal'])
    
    # Crear un objeto de imagen
    img = Image(image_path)
    img.drawHeight = 150  # Establecer la altura de la imagen
    img.drawWidth = 150   # Establecer el ancho de la imagen
    
    # Agregar la fila a los datos de la tabla
    data.append([letter_paragraph, img, smile])

# Crear la tabla
table = Table(data)

# Agregar un estilo simple a la tabla
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

# Construir el PDF
doc.build([table])

# Imprimir la confirmación de creación del PDF
print(f"PDF creado exitosamente y guardado como {pdf_path}")
