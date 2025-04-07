import requests
from ollama import ChatResponse
from ollama import chat
from bs4 import BeautifulSoup
url = 'https://www.mercadolivre.com.br/monitor-195-led-3green-75hz-hd-gamer-2ms-hdmi-e-vga-vesa-cor-preto-110v220v/p/MLB28983718?pdp_filters=item_id:MLB5323656810#is_advertising=true&searchVariation=MLB28983718&backend_model=search-backend&position=2&search_layout=grid&type=pad&tracking_id=a6fb286e-0a70-434e-8f83-7cd523324694&is_advertising=true&ad_domain=VQCATCORE_LST&ad_position=2&ad_click_id=OGFkN2YwZTctMmRlMy00YTcwLWJlN2UtZjFlYmZkMWE0YzJj'
url2 = 'https://www.kabum.com.br/produto/472913/monitor-profissional-lg-27-uhd-4k-ips-hdmi-e-dp-hdr400-freesync-dci-p3-95-branco-27up650-w'
url3 = 'https://www.pichau.com.br/pc-gamer-pichau-afrodite-intel-i5-11400-intel-arc-a750-8gb-16gb-ddr4-ssd-1tb-46021?gad_source=1&gclid=CjwKCAjwwLO_BhB2EiwAx2e-35Z_aX72uM6JuqzKbPKhQeOzy-ZlfWeLzyRGbYWTfucyLkYug07Q8xoCQAMQAvD_BwE'
url4 = 'https://www.kabum.com.br/produto/471957/teclado-mecanico-gamer-kbm-gaming-tg700-preto-65-e-abnt2-rgb-switch-gateron-red-kgtg700ptvr'
headers = {"User-Agent":"Mozilla/5.0"}

x = requests.get(url4, headers=headers)

soup = BeautifulSoup(x.text, "html.parser")

html = soup.find_all('span')

response: ChatResponse = chat(model='gemma3:12b', messages=[
    {
        'role': 'user',
        'content': f'com base nesse bloco de html {html} indentifique o nome do produto e preço, ao indentificar, você apenas retornará ({{nome do produto}},{{preco do produto}}) apenas, não diga nada além desses dois valores, e caso não encontre, retorne Undefine',
    }
])
print(response['message']['content'])