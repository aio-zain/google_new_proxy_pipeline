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
            print("Working on tab:", tab_names[idx])
            try:
                try:
                    driver.get(url)
                    print("got the link 1")
                except Exception as e:
                    print("unable to get link 1")
                    try:
                        driver.quit()
                        print("Quiting driver 1")
                    except:
                        print("unable to quit driver 1")
                        pass
                    print("starting new drive 1r")
                    driver = dm.get_new_driver_with_retries(urls)
                    driver.get(url)
                    print("new driver 1")
                check = dm.fun_check_captcha(driver)
                if not check:
                    print("----------- C A P T C H A   F O U N D ---------")
                    try:
                        driver.quit()
                        print("Closing driver after captcha found 1")
                    except:
                        pass
                    try:
                        print("trying new driver after captcha found 1")
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
                    print("Quiting driver 2")
                    driver.quit()
                    print("driver 2 closed")
                except:
                    pass
                try:
                    print("trying new driver after captcha found 2")
                    driver = dm.get_new_driver_with_retries(urls)
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
                print("driver quit successfully in outer exception in perform_all_searches")
                print("trying new driver in outer exception in perform_all_searches")
                driver = dm.get_new_driver_with_retries(urls)
            except Exception as e:
                print("some problem in quiting driver in outer except", e)
            record = {}

    return record, driver


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
