import requests
from bs4 import BeautifulSoup
import re
from colorama import Fore
import colorama
import requests

colorama.init()

def Hypeboost_Scrapper(SKU):
    try:
        url=f"https://hypeboost.com/es/search/shop?keyword={SKU}"

        html_text= requests.get(url).text
        soup= BeautifulSoup(html_text,'html.parser')
        link_scrapper = soup.find('a')

        URL=link_scrapper['href']
        html= requests.get(URL).text
        soup= BeautifulSoup(html,'html.parser')
        tallas =soup.find('div', {'class': 'sizes'})

        #shoe name
        nombre=soup.find('h1')
        titulo=nombre.text

        #size
        talla=tallas.find_all('div', {'class': 'label'})

        #price
        precio=tallas.find_all('div', {'class': 'price'})

        vec_tallas=['Talla']
        vec_precios=['Precio']
        vec_payouts=['Payout']

        
        for i in talla:
            vec_tallas.append(i.text)

        for e in precio:
            str_precio=re.sub(r'[^\d€]+', '', (e.text))
            precio_zapa=str_precio.replace("€", "")
            if("€" not in str_precio):
                vec_precios.append("0")
                vec_payouts.append("0")
            else:
                vec_precios.append(precio_zapa)
                payout= (float(precio_zapa)*0.915)-15
                payout_redondeado = round(payout, 2)
                vec_payouts.append(str(payout_redondeado))

        embed_text=""
        for i in range(len(vec_precios)):
            embed_text=embed_text+(vec_tallas[i]+" | "+vec_precios[i]+" | "+vec_payouts[i]+'\n')

        mensaje_hb=(f"HYPEBOOST: {titulo}\n{embed_text}")
        
        return mensaje_hb
    except Exception as e:
        print(Fore.RED+f"Error al obtener la zapatilla, Error: ", e)


print(Fore.WHITE+   "      __  ____  ______  __________  ____  ____  ___________   _____ __________  ___    ____  ____  __________ \n"+
                    "     / / / /\ \/ / __ \/ ____/ __ )/ __ \/ __ \/ ___/_  __/  / ___// ____/ __ \/   |  / __ \/ __ \/ ____/ __ \ \n"+
                    "    / /_/ /  \  / /_/ / __/ / __  / / / / / / /\__ \ / /     \__ \/ /   / /_/ / /| | / /_/ / /_/ / __/ / /_/ / \n"+
                    "   / __  /   / / ____/ /___/ /_/ / /_/ / /_/ /___/ // /     ___/ / /___/ _, _/ ___ |/ ____/ ____/ /___/ _, _/  \n"+
                    "  /_/ /_/   /_/_/   /_____/_____/\____/\____//____//_/     /____/\____/_/ |_/_/  |_/_/   /_/   /_____/_/ |_| by Mochaaless ")


while True:
    sku=input(Fore.WHITE+"\nIntroduzca sku: ")
    print(Fore.WHITE+"\n"+Hypeboost_Scrapper(sku))
    print(Fore.WHITE+"--------------------------------------")
