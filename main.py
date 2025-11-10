import csv, os, sys, requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from requests.exceptions import RequestException
from typing import Dict, List, Optional, Any


def nacti_obce(zakladni_url: str = "https://www.volby.cz/pls/ps2017nss/ps32?"
                              "xjazyk=CZ&xkraj=2&xnumnuts=2112") -> List[Dict[str, str]]:
    """Nacte seznam obci z webove stranky s vysledky voleb."""
    try:
        parsed_url = urlparse(zakladni_url)
        if not all([parsed_url.scheme, parsed_url.netloc]): raise ValueError("Neplatný formát URL")
        soup = BeautifulSoup(requests.get(zakladni_url, timeout=10).text, 'html.parser')
        obce = []
        for tabulka in soup.find_all('table', {'class': 'table'}):
            for radek in tabulka.find_all('tr')[2:]:
                bunky = radek.find_all(['td', 'th'])
                if len(bunky) >= 3:
                    odkaz = bunky[0].find('a')
                    if odkaz and 'xobec' in odkaz.get('href', ''):
                        obce.append({
                            'Kod obce': bunky[0].get_text(strip=True),
                            'Nazev obce': bunky[1].get_text(strip=True),
                            'odkaz': urljoin(zakladni_url, odkaz['href'])
                        })
        return obce
    except RequestException as e:
        raise RequestException(f"Chyba při stahování: {str(e)}") from e


def _extr_kod(url: str) -> str:
    return url.split('xobec=')[1].split('&')[0] if 'xobec=' in url else 'N/A'


def _najdi_obec(kod: str, obce: List[Dict[str, str]]) -> str:
    return next((o['Nazev obce'] for o in obce if o['Kod obce'] == kod), 'Neznámá obec')


def _zpracuj_zakl_udaje(tab: BeautifulSoup) -> Dict[str, str]:
    vysledek = {
        'Volici v seznamu': '0',
        'Vydane obalky': '0',
        'Platne hlasy': '0'
    }
    try:
        bunky = next(
            (r.find_all('td') for r in tab.find_all('tr') 
             if len(r.find_all('td')) >= 8),
            None
        )
        if bunky:
            vysledek.update({
                'Volici v seznamu': bunky[3].get_text(strip=True).replace('\xa0', ''),
                'Vydane obalky': bunky[4].get_text(strip=True).replace('\xa0', ''),
                'Platne hlasy': bunky[7].get_text(strip=True).replace('\xa0', '')
            })
    except (IndexError, AttributeError):
        pass
    return vysledek


def _zpracuj_strany(tab: BeautifulSoup) -> Dict[str, str]:
    vysledky = {}
    for radek in tab.find_all('tr'):
        if len(bunky := radek.find_all('td')) >= 3:
            try:
                if (nazev := bunky[1].get_text(strip=True)) and (hlasy := bunky[2].get_text(strip=True).replace('\xa0', '')).isdigit():
                    vysledky[nazev] = hlasy
            except (IndexError, AttributeError):
                continue
    return vysledky


def ziskej_data_obce(
    url: str, 
    obce: List[Dict[str, str]]
) -> Optional[Dict[str, Any]]:
    try:
        soup = BeautifulSoup(requests.get(url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=10).text, 'html.parser')
        kod = _extr_kod(url)
        vysledek = {
            'Kod obce': kod,
            'Nazev obce': _najdi_obec(kod, obce),
            'Volici v seznamu': '0',
            'Vydane obalky': '0',
            'Platne hlasy': '0'
        }
        if tabulky := soup.find_all('table'):
            vysledek.update(_zpracuj_zakl_udaje(tabulky[0]))
            for tab in tabulky[1:]:
                vysledek.update(_zpracuj_strany(tab))
        return vysledek
    except Exception as e:
        print(f"Chyba: {e}")
        return None


def _vytvor_hlavicku(data: List[Dict[str, str]]) -> List[str]:
    zakladni = ['Kod obce', 'Nazev obce', 'Volici v seznamu', 'Vydane obalky', 'Platne hlasy']
    return zakladni + sorted({k for radek in data for k in radek} - set(zakladni))


def uloz_do_csv(data: List[Dict[str, str]], nazev: str) -> bool:
    if not data: return False
    try:
        nazev = f"{nazev}.csv" if not nazev.lower().endswith('.csv') else nazev
        with open(nazev, 'w', newline='', encoding='utf-8-sig') as f:
            writer = csv.DictWriter(f, fieldnames=_vytvor_hlavicku(data), delimiter=';', quoting=csv.QUOTE_NONNUMERIC)
            writer.writeheader()
            for radek in data:
                writer.writerow(
                    {k: radek.get(k, '0') for k in writer.fieldnames}
                )
        print(f"Ulozeno {len(data)} zaznamu do {nazev}")
        return True
    except Exception as e:
        print(f"Chyba: {e}")
        return False


def stahni_a_uloz(url: str, vystup: str) -> None:
    if not url: return
    print(f"Stahuji z: {url}")
    print(f"Ukladam do: {vystup}")
    
    original = sys.stdout
    sys.stdout = open(os.devnull, 'w', encoding='utf-8')
    
    try:
        obce = nacti_obce(url)
        if not obce:
            print("Nenalezena zadna obec")
            return
            
        vysledky = []
        for obec in obce:
            if not isinstance(obec, dict) or 'odkaz' not in obec: continue
            try:
                if data := ziskej_data_obce(obec['odkaz'], obce):
                    vysledky.append(data)
            except Exception as e:
                print(f"Chyba u {obec.get('Nazev obce', 'neznama')}: {e}")
        
        sys.stdout = original
        if vysledky:
            if uloz_do_csv(vysledky, vystup):
                print(f"Hotovo: {len(vysledky)} zaznamu")
            else:
                print("Chyba pri ukladani")
        else:
            print("Zadna data k ulozeni")
    except Exception as e:
        sys.stdout = original
        print(f"Chyba: {e}")
    finally:
        sys.stdout = original

if __name__ == "__main__":
    URL = "https://www.volby.cz/pls/ps2017nss/ps32?" \
          "xjazyk=CZ&xkraj=2&xnumnuts=2112"
    VYSTUP = "vysledky_rakovnik.csv"
    stahni_a_uloz(URL, VYSTUP)
    print("Program byl uspesne ukoncen.")

