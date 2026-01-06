from playwright.sync_api import Page, expect, TimeoutError as PlaywrightTimeoutError
import logging
import pytest

URL_UVODNI_STRANKY = "https://www.chmi.cz/"
CASOVY_LIMIT_MS = 2000
LOG_LEVEL = logging.INFO

logging.basicConfig(level=LOG_LEVEL)
logger = logging.getLogger(__name__)

@pytest.fixture(scope="function")
def page(browser):
    context = browser.new_context(locale="cs-CZ")
    stranka = context.new_page()
    stranka.set_default_timeout(20000)
    stranka.set_default_navigation_timeout(30000)

    def log_pozadavek(pozadavek):
        logger.info(f"Pozadavek: {pozadavek.method} {pozadavek.url}")

    def log_odpoved(odpoved):
        if odpoved.status >= 400:
            logger.warning(f"Chyba {odpoved.status} pro {odpoved.url}")
        else:
            logger.info(f"Odpoved: {odpoved.status} {odpoved.url}")

    stranka.on("request", log_pozadavek)
    stranka.on("response", log_odpoved)

    yield stranka
    stranka.close()
    context.close()

def prijmout_cookies(stranka):
    try:
        selektory = [
            "button:has-text('Souhlasim')",
            "button:has-text('Prijmout')",
            "button:has-text('Souhlas')",
            "button:has-text('Accept')",
            "button#didomi-notice-agree-button",
            ".cookie-consent button"
        ]

        for selektor in selektory:
            try:
                if stranka.locator(selektor).first.is_visible(timeout=CASOVY_LIMIT_MS):
                    with stranka.expect_navigation(wait_until="domcontentloaded"):
                        stranka.click(selektor)
                    return True
            except (PlaywrightTimeoutError, Exception) as chyba:
                logger.debug(f"Selektor {selektor} nebyl nalezen: {str(chyba)}")
                continue
        return False
    except Exception as chyba:
        logger.error(f"Neocekavana chyba v prijmout_cookies: {str(chyba)}")
        return False

def test_nacitani_uvodni_stranky(page: Page):
    odpoved = page.goto(URL_UVODNI_STRANKY, wait_until="networkidle")
    assert odpoved.status == 200, "Nepodarilo se nacist uvodni stranku"

    prijmout_cookies(page)
    assert page.title(), "Titulek stranky je prazdny"
    expect(page.locator("body")).to_be_visible()
    logger.info("Uvodni stranka byla uspesne nactena")

def test_navigace_na_predpoved(page: Page):
    page.goto(URL_UVODNI_STRANKY)
    prijmout_cookies(page)

    selektory = [
        "a:has-text('Predpoved pocasi')",
        "a:has-text('Predpovedi')",
        "a:has-text('predpoved')",
        "a[href*='predpoved']"
    ]

    for selektor in selektory:
        try:
            if page.locator(selektor).first.is_visible(timeout=CASOVY_LIMIT_MS):
                with page.expect_navigation(wait_until="networkidle"):
                    page.click(selektor)
                logger.info(f"Kliknuto na: {selektor}")
                break
        except (PlaywrightTimeoutError, Exception) as chyba:
            logger.debug(f"Navigace selhala pro {selektor}: {str(chyba)}")
            continue

    obsah = page.content().lower()
    assert any(termin in obsah for termin in ["predpoved", "teplota", "vitr"]), \
        "Nenalezeny ocekavane klicove vyrazy na strance"

def test_radarova_stranka(page: Page):
    page.goto(URL_UVODNI_STRANKY)
    prijmout_cookies(page)

    selektory = [
        "a:has-text('Radar')",
        "a:has-text('RADAR')",
        "a[href*='radar']",
        "a[href*='RADAR']"
    ]

    for selektor in selektory:
        try:
            if page.locator(selektor).first.is_visible(timeout=CASOVY_LIMIT_MS):
                with page.expect_navigation(wait_until="networkidle"):
                    page.click(selektor)
                logger.info(f"Kliknuto na radar: {selektor}")
                break
        except (PlaywrightTimeoutError, Exception) as chyba:
            logger.debug(f"Navigace na radar selhala: {str(chyba)}")
            continue

    obsah = page.content().lower()
    assert (any(termin in obsah for termin in ["radar", "srazky"]) or
            page.locator("iframe, canvas, [id*='radar'], [class*='radar']").count() > 0), \
        "Nenalezeny ocekavane radarove prvky"
    logger.info("Radarova stranka byla uspesne overena")