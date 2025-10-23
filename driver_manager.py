
import random
import time
import seleniumwire.undetected_chromedriver as webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

def fun_check_captcha(driver):

    try:
        temp_source = driver.find_element(By.TAG_NAME, "body").text
        print("temp source found")
        print("driver current url: ", driver.current_url)
        if "Our systems have detected unusual traffic" in temp_source:
            print("permission to get URL Error (captcha)")
            try:
                driver.quit()
            except Exception:
                pass
            return False
        elif "Your client does not have permission to get URL" in temp_source:
            print("detected unusual traffic Error (permission)")
            try:
                driver.quit()
            except Exception:
                pass
            return False
        elif "/sorry/index" in driver.current_url:
            print("captcha detected in url")
            return False
        else:
            return True
    except Exception as e:
        print("⚠️ fun_check_captcha: cannot read page body:", e)
        try:
            driver.quit()
        except Exception:
            pass
        return False


def build_proxy_endpoint():
    us_states = [
        "California", "New York", "Texas", "Massachusetts",
        "Washington", "Illinois", "Colorado", "Virginia",
        "Florida", "New Jersey", "Maryland", "Georgia",
        "North Carolina", "Oregon", "Minnesota"
    ]
    random_state = random.choice(us_states).lower().replace(" ", "")
    # endpoint = f"6df3a0d207f7f8a12eaf__cr.us;state.{random_state}:36d8cb204fe949ca@gw.dataimpulse.com:{random.randint(10000,15000)}"
    # endpoint = f"04ca83490882b593a156__cr.us;state.{random_state}:fcfd4edff021770e@gw.dataimpulse.com:{random.randint(10000,15000)}"
    # endpoint = "04ca83490882b593a156__cr.us:fcfd4edff021770e@gw.dataimpulse.com:823"
    endpoint = f"04ca83490882b593a156__cr.ca:fcfd4edff021770e@gw.dataimpulse.com:823"
    return endpoint


def init_driver(url):

    driver = None
    try:
        endpoint = build_proxy_endpoint()

        options = Options()
        options.add_argument("--no-first-run")
        options.add_argument("--disable-background-networking")
        options.add_argument("--disable-component-update")
        options.add_argument("--disable-popup-blocking")
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_argument("--disable-features=OptimizationGuideModelDownloading,OptimizationHintsFetching")

        selenium_wire_options = {
            'proxy': {
                'http': f'http://{endpoint}',
                'https': f'http://{endpoint}',
                'no_proxy': 'localhost,127.0.0.1'
            },
        }

        driver = webdriver.Chrome(
            options=options,
            seleniumwire_options=selenium_wire_options,
            version_main=141
        )
        driver.maximize_window()
        time.sleep(random.uniform(1.5, 2.5))
        # quick smoke test
        try:
            driver.get(url)
        except Exception as e:
            print("⚠️ init_driver: couldn't load google:", e)

        return driver

    except Exception as e:
        print("❌ init_driver error:", e)
        try:
            if driver:
                driver.quit()
        except Exception:
            pass
        return None


def get_new_driver_with_retries(one_time_queries):
    retries = 6
    print("Getting new driver...")
    for attempt in range(1, retries + 1):
        url = one_time_queries[0]
        print("Getting:---- ", url)
        driver = init_driver(url)
        if driver:
            if fun_check_captcha(driver):
                print("No captcha found")
                return driver
            else:
                print("Captcha found at get_new_driver_with_retries")
                driver.quit()
        print(f"Retrying driver init ({attempt}/{retries})...")
        time.sleep(random.randint(1, 2))
    raise RuntimeError("Unable to initialize driver after retries")
