# Stahovač výsledků voleb

Tento program slouží ke stažení a zpracování výsledků voleb z webu volby.cz. Umožňuje snadné získání dat o volbách pro konkrétní okres a jejich uložení do CSV souboru.

## Požadavky

Pro spuštění programu potřebujete nainstalovat Python 3.7 nebo novější a následující knihovny:
- requests >= 2.31.0
- beautifulsoup4 >= 4.12.2

## Instalace

1. Stáhněte si tento repozitář nebo zkopírujte soubory do složky vašeho projektu.

2. Nainstalujte potřebné knihovny pomocí příkazu:

```bash
pip install -r requirements.txt
```

## Jak používat

1. Otevřete příkazový řádek (Command Prompt nebo PowerShell) a přejděte do složky s programem.
2. Spusťte program následujícím příkazem:

```bash
python main.py
```

Po spuštění program automaticky stáhne data a uloží je do souboru `vysledky_rakovnik.csv` v aktuální složce.

### Popis funkce

Program automaticky:
1. Naváže spojení s webem volby.cz
2. Stáhne výsledky voleb pro okres Rakovník
3. Uloží data do souboru `vysledky_rakovnik.csv`

### Přizpůsobení

Pokud chcete stáhnout výsledky pro jiný okres, upravte proměnné `URL` a `VYSTUP` v souboru `main.py`:

```python
# Příklad pro jiný okres
# xkraj=2 (Středočeský kraj), xnumnuts=2113 (okres Rakovník)
URL = "https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=2&xnumnuts=2113"
VYSTUP = "vysledky_jiny_okres.csv"  # Název výstupního souboru
```

## Formát výstupu

Výstupní soubor ve formátu CSV obsahuje následující sloupce:

- Kod obce - Kód obce (číslo obce v rámci okresu)
- Nazev obce - Název obce
- Volici v seznamu - Počet voličů v seznamu
- Vydane obalky - Počet vydaných obálek
- Platne hlasy - Počet platných hlasů
- Následují sloupce s názvy politických stran a počty hlasů pro každou stranu

## Řešení problémů

- **Chyby při stahování**: Zkontrolujte připojení k internetu a zda je URL platné.
- **Chyby s kódováním**: Ujistěte se, že používáte kódování UTF-8 pro práci se soubory.
- **Chybějící knihovny**: Pokud se zobrazí chyba o neznámých modulech, nainstalujte je pomocí `pip install`.

## Upozornění

Tento program byl vytvořen výhradně pro studijní účely. Je určen k výukovým účelům a neměl by být používán pro komerční nebo produkční nasazení.
