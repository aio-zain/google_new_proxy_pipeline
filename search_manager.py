# search_manager.py
import random
import time
from query_generator import generate_queries, linkedin_owner_query
from search_extractor import extract_search_data
import driver_manager as dm

def perform_all_searches(driver, title, address, delay_between=2):

    urls, raw_queries, tab_names = generate_queries(title, address)
    record = {}
    for idx, url in enumerate(urls):
        try:
            try:
                if url == driver.current_url:
                    print("OK | Found the same franchise restaurant")
                    pass
                else:
                    print("NOT OK | NOT Found the same Link")
                    driver.get(url)
                check = dm.fun_check_captcha(driver)
                if not check:
                    print("----------- C A P T C H A   F O U N D ---------")
                    try:
                        driver.quit()
                    except:
                        pass
                    try:
                        driver = dm.get_new_driver_with_retries(urls)
                    except Exception as e:
                        print("Some problem in creating new driver in perform_all_searches", e)
                else:
                    pass
                print("time delay")
                time.sleep(random.uniform(0.5, 1.5))
                print("extracting")
                res = extract_search_data(driver, title, address)
                print("Done")
                record[tab_names[idx]] = res
            except:
                try:
                    driver.quit()
                except:
                    pass
                try:
                    dm.get_new_driver_with_retries(urls)
                except Exception as e:
                    print("Some problem in creating new driver in perform_all_searches", e)
                driver.get(url)
                print("time delay")
                time.sleep(random.uniform(0.5, 1.5))
                print("extracting")
                res = extract_search_data(driver, title, address)
                record[tab_names[idx]] = res
        except Exception as e:
            print("some outer exception in perform all searches", e)
            try:
                driver.quit()
            except Exception as e:
                print("driver quit successfully in outer exception in perform_all_searches", e)
            record = {}

    return record


def perform_owner_linkedin_search(driver, owner_name, title, delay_between=2):
    """
    Perform LinkedIn-style query for a single owner_name.
    """
    if not owner_name:
        return None
    q_url = linkedin_owner_query(owner_name, title)
    try:
        driver.get(q_url)
        time.sleep(random.uniform(0.5, 1.5))
        return extract_search_data(driver, title, f"linkedin_search_for_{owner_name}")
    except Exception as e:
        print("⚠️ Error during owner linkedin search:", e)
        return {
            "title": title,
            "address": "",
            "ai_result": f"error: {e}",
            "search_results": []
        }
