# Testovací scénář pro web CHMI

## 1. Základní testy
- **1.1 Načtení úvodní stránky**
  - Očekávaný výsledek: Stránka se úspěšně načte, zobrazí se hlavní obsah
  - Kritické body: Rychlost načtení, viditelnost hlavního menu

- **1.2 Přijetí cookies**
  - Očekávaný výsledek: Cookie lišta se zobrazí a po kliknutí na tlačítko "Souhlasit" zmizí
  - Kritické body: Správné fungování tlačítka, uložení volby

## 2. Testy navigace
- **2.1 Hlavní menu**
  - Ověření všech položek menu
  - Test rozbalovacích podnabídek
  - Ověření funkčnosti odkazů

- **2.2 Předpověď počasí**
  - Navigace na stránku s předpovědí
  - Ověření zobrazení mapy
  - Kontrola výběru lokality

## 3. Testy funkcionalit
- **3.1 Vyhledávání**
  - Vyhledání konkrétního pojmu
  - Ověření relevance výsledků
  - Test prázdného vyhledávání

- **3.2 Přepínání jazykových mutací**
  - Ověření funkčnosti přepínání mezi CZ/EN
  - Kontrola překladů klíčových prvků

## 4. Testy responzivity
- **4.1 Různá rozlišení**
  - Mobil (360x640)
  - Tablet (768x1024)
  - Desktop (1920x1080)

## 5. Výkonnostní testy
- Doba načítání stránek
- Rychlost reakce na akce uživatele
- Zatížení stránky

## 6. Postup spuštění testů
1. Nainstalujte závislosti: `pip install -r requirements.txt`
2. Spusťte testy: `pytest test_scenar.py -v`
3. Pro generování reportu: `pytest --html=report.html`

## 7. Očekávané chování
- Všechny testy by měly projít bez chyb
- Průběh testů je logován do konzole
- Při selhání se vytvoří screenshot chyby