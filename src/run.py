import os
from datetime import datetime, timedelta
import planetary_computer
import pystac_client
from PIL import Image
import requests
from io import BytesIO

# Carregar variáveis de ambiente
from dotenv import load_dotenv
load_dotenv()

# URL da API STAC
STAC_API_URL = os.getenv('STAC_API_URL')

# Criar um cliente STAC
client = pystac_client.Client.open(STAC_API_URL, modifier=planetary_computer.sign_inplace)

# Obter o número de dias para retroceder a partir da data atual
days_back = int(os.getenv('DAYS_BACK'))

# Definir a data mais recente para pesquisa
end_date = datetime.utcnow()
start_date = end_date - timedelta(days=days_back)

# Parâmetros da pesquisa
collections = os.getenv('COLLECTIONS').split(',')
datetime_range = f"{start_date.isoformat()}Z/{end_date.isoformat()}Z"
bbox = [float(n) for n in os.getenv('SEARCH_BBOX').split(',')]
cloud_cover_max = int(os.getenv('CLOUD_COVER_MAX'))
search_limit = int(os.getenv('SEARCH_LIMIT'))

# Realizar a busca por imagens
search = client.search(
    collections=collections,
    datetime=datetime_range,
    bbox=bbox,
    query={"eo:cloud_cover": {"lt": cloud_cover_max}},
    limit=search_limit,
    sortby=[{"field": "properties.datetime", "direction": "desc"}]
)

# Baixar, converter e salvar os itens
items = list(search.get_items())
if items:
    for item in items:
        signed_item = planetary_computer.sign(item)
        response = requests.get(signed_item.assets['visual'].href)
        image = Image.open(BytesIO(response.content))
        # Converter para JPEG
        jpeg_quality = int(os.getenv('JPEG_QUALITY'))
        jpeg_path = os.path.join('img', f"{item.id}.jpeg")
        image.convert('RGB').save(jpeg_path, "JPEG", quality=jpeg_quality)
        print(f"Imagem salva em: {jpeg_path} | Data da imagem: {item.properties['datetime']}")
else:
    print("Nenhum item encontrado.")
