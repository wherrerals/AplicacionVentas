import requests

DEFAULT_IMAGE_URL = "https://ledstudiocl.vtexassets.com/assets/vtex.file-manager-graphql/images/14ecba9f-2814-4029-9e0e-e5e6b9e2869c___b2a5497dbc81c0adc5576c48b2eeb27b.jpg"

def url_exists(url):

    if not url: 
        return False
    try:
        response = requests.head(url, allow_redirects=True, timeout=5)
        return response.status_code == 200
    except requests.RequestException:
        return False
    
def get_valid_image_url(url):

    return url if url_exists(url) else DEFAULT_IMAGE_URL