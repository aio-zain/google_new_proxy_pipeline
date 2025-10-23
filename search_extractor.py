# search_extractor.py
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

def fun_extract_ai_results(driver, timeout=5):
    try:
        # WebDriverWait(driver, timeout).until(
        #     EC.presence_of_element_located((By.CSS_SELECTOR, "div.LT6XE"))
        # )
        time.sleep(1)
        el = driver.find_element(By.CSS_SELECTOR, "div.LT6XE")
        print("OOO0o---- AI Data Found")
        return el.text.strip()
    except Exception:
        print("AI Data Not Found ------oOOOOO")
        return "AI Overview not available"


def fun_extract_results(driver, timeout=6):
    try:
        WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#rso > div"))
        )
        search_results = driver.find_elements(By.CSS_SELECTOR, "#rso > div")
        print("OOO0o---- Results data Found")

        if len(search_results) < 2:
            print("RSO div had less than 2 results")
            search_results = driver.find_elements(By.CLASS_NAME, "A6K0A")
            print("total new search results: ", len(search_results))
        return search_results
    except Exception:
        print("Results data Not Found ------oOOOOO")
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
            print("Title :", title_text)
        except Exception:
            title_text = block_text.split("\n")[0].strip()
            print("Title in except:", title_text)
        try:
            link_el = element.find_element(By.CSS_SELECTOR, "a[href]")
            link = link_el.get_attribute("href")
            print("Link :", link)
        except Exception:
            print("Link not found")
            link = None

        lines = [l.strip() for l in block_text.split("\n") if l.strip()]
        snippet = max(lines, key=len) if lines else block_text
        if snippet:
            print("Snippet found")
        else:
            print("Snippet not found")
        if len(snippet) > 400:
            snippet = snippet[:400] + "..."
        print("=================================================================================")
        print({
            "search_title": title_text,
            "search_snippet": snippet,
            "search_link": link
        })
        print("=================================================================================")
        return {
            "search_title": title_text,
            "search_snippet": snippet,
            "search_link": link
        }
    except Exception:
        print("in exception in parse_result_block --- returning None")
        return None


def extract_search_data(driver, query_title, query_address):
    try:
        ai = fun_extract_ai_results(driver)
        blocks = fun_extract_results(driver)
        print("total search blocks: ", len(blocks))
        results = []
        for b in blocks:
            parsed = parse_result_block(b)
            if parsed:
                results.append(parsed)

        print("OKkkkkkkkkkkk -- in extract_search_data")
        return {
            "title": query_title,
            "address": query_address,
            "ai_result": ai,
            "search_results": results
        }
    except Exception as e:
        print("in except of extract_search_data:----- sent empty data")
        return {
            "title": query_title,
            "address": query_address,
            "ai_result": f"Error: {e}",
            "search_results": []
        }
