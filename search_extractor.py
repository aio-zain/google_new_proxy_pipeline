# search_extractor.py
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

def fun_extract_ai_results(driver, timeout=5):
    try:
        WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div.LT6XE"))
        )
        el = driver.find_element(By.CSS_SELECTOR, "div.LT6XE")
        return el.text.strip()
    except Exception:
        return "AI Overview not available"


def fun_extract_results(driver, timeout=6):
    try:
        WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#rso > div"))
        )
        return driver.find_elements(By.CSS_SELECTOR, "#rso > div")
    except TimeoutException:
        return []
    except Exception:
        return []


def parse_result_block(element):
    try:
        block_text = element.text.strip()
        if not block_text:
            return None
        if "People also ask" in block_text:
            return None
        try:
            title_el = element.find_element(By.CSS_SELECTOR, "h3")
            title_text = title_el.text.strip()
        except Exception:
            title_text = block_text.split("\n")[0].strip()
        try:
            link_el = element.find_element(By.CSS_SELECTOR, "a[href]")
            link = link_el.get_attribute("href")
        except Exception:
            link = None
        lines = [l.strip() for l in block_text.split("\n") if l.strip()]
        snippet = max(lines, key=len) if lines else block_text
        if len(snippet) > 400:
            snippet = snippet[:400] + "..."
        return {
            "search_title": title_text,
            "search_snippet": snippet,
            "search_link": link
        }
    except Exception:
        return None


def extract_search_data(driver, query_title, query_address):
    try:
        ai = fun_extract_ai_results(driver)
        blocks = fun_extract_results(driver)
        results = []
        for b in blocks:
            parsed = parse_result_block(b)
            if parsed:
                results.append(parsed)
        return {
            "title": query_title,
            "address": query_address,
            "ai_result": ai,
            "search_results": results
        }
    except Exception as e:
        return {
            "title": query_title,
            "address": query_address,
            "ai_result": f"Error: {e}",
            "search_results": []
        }
