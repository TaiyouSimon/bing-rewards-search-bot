import time
import random
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.edge.options import Options as EdgeOptions

os.system('')

class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    ENDC = '\033[0m'

KEYWORDS_FILE = 'keywords.txt'
NUM_DESKTOP_SEARCHES = random.randint(32, 36)
NUM_MOBILE_SEARCHES = random.randint(22, 26)
MIN_DELAY_SECONDS = 6
MAX_DELAY_SECONDS = 12
MIN_TYPING_DELAY_SECONDS = 0.08
MAX_TYPING_DELAY_SECONDS = 0.25

print(f"{Colors.HEADER}{Colors.BOLD}╔══════════════════════════════════════════════════════╗")
print(f"║        BING REWARDS SEARCH AUTOMATOR V3.0        ║")
print(f"╚══════════════════════════════════════════════════════╝{Colors.ENDC}")

print(f"\n{Colors.BOLD}{Colors.RED}CRITICAL INSTRUCTIONS (READ FIRST):{Colors.ENDC}")
print(f"{Colors.RED}1. Make sure you are already logged into your Microsoft account in Edge.")
print(f"2. You MUST close all Microsoft Edge windows before running this script.{Colors.ENDC}")

print(f"\n{Colors.YELLOW}Disclaimer: Automating searches may be against the Microsoft")
print(f"Rewards Terms of Service. Use this script at your own risk.{Colors.ENDC}\n")
print(f"{Colors.BLUE}============================================================{Colors.ENDC}")



def load_keywords(filename):
    """Loads search keywords from a text file."""
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            keywords = [line.strip() for line in f if line.strip()]
        print(f"{Colors.GREEN}[✔] Successfully loaded {len(keywords)} keywords from '{filename}'{Colors.ENDC}")
        return keywords
    except FileNotFoundError:
        print(f"{Colors.RED}[✖] ERROR: The file '{filename}' was not found.")
        print(f"[✖] Please create it and add one search keyword per line.{Colors.ENDC}")
        exit()

def human_like_delay(min_sec, max_sec):
    """Waits for a random duration within a given range."""
    delay = random.uniform(min_sec, max_sec)
    time.sleep(delay)

def setup_driver(is_mobile=False):
    """Sets up the Selenium Edge driver."""
    options = EdgeOptions()
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option('excludeSwitches', ['enable-automation'])
    options.add_experimental_option('useAutomationExtension', False)

    if is_mobile:
        print(f"\n{Colors.CYAN}[+] Configuring for MOBILE browser emulation...{Colors.ENDC}")
        mobile_emulation = {
            "deviceMetrics": {"width": 375, "height": 812, "pixelRatio": 3.0},
            "userAgent": "Mozilla/5.0 (Linux; Android 11; Pixel 5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.91 Mobile Safari/537.36"
        }
        options.add_experimental_option("mobileEmulation", mobile_emulation)
    else:
        print(f"\n{Colors.CYAN}[+] Configuring for DESKTOP browser...{Colors.ENDC}")
        options.add_argument("--start-maximized")

    try:
        driver = webdriver.Edge(options=options)
        return driver
    except Exception as e:
        print(f"{Colors.RED}[✖] ERROR: Failed to start Edge driver. Is Edge fully closed?")
        print(f"    Details: {e}{Colors.ENDC}")
        exit()


def perform_searches(driver, keywords, num_searches, device_type):
    """Performs the given number of searches using the provided driver."""
    print(f"{Colors.BLUE}[▶] Starting {device_type} searches...{Colors.ENDC}")
    driver.get("https://www.bing.com")
    time.sleep(3) 

    for i in range(num_searches):
        search_term = random.choice(keywords)
        print(f"  {Colors.CYAN}↳{Colors.ENDC} Search {Colors.YELLOW}{i + 1}/{num_searches}{Colors.ENDC}: '{search_term}'")
        try:
            search_box = driver.find_element(By.NAME, 'q')
            search_box.clear()
            
            for char in search_term:
                search_box.send_keys(char)
                human_like_delay(MIN_TYPING_DELAY_SECONDS, MAX_TYPING_DELAY_SECONDS)
            
            search_box.send_keys(Keys.RETURN)
            human_like_delay(MIN_DELAY_SECONDS, MAX_DELAY_SECONDS)

        except Exception as e:
            print(f"{Colors.RED}[!] An error occurred during search {i + 1}: {e}")
            print(f"    Attempting to recover...{Colors.ENDC}")
            driver.refresh()
            time.sleep(5)


if __name__ == "__main__":
    all_keywords = load_keywords(KEYWORDS_FILE)

    print(f"\n{Colors.HEADER}--- CHOOSE AN OPTION ---{Colors.ENDC}")
    print(" 1. Desktop Searches Only")
    print(" 2. Mobile Searches Only")
    print(" 3. Both Desktop & Mobile Searches")
    choice = ""
    while choice not in ["1", "2", "3"]:
        choice = input(f"{Colors.YELLOW}Enter your choice (1, 2, or 3): {Colors.ENDC}").strip()
        if choice not in ["1", "2", "3"]:
            print(f"{Colors.RED}[!] Invalid choice. Please try again.{Colors.ENDC}")
    
    if choice in ['1', '3']:
        desktop_driver = setup_driver(is_mobile=False)
        perform_searches(desktop_driver, all_keywords, NUM_DESKTOP_SEARCHES, "Desktop")
        print(f"{Colors.GREEN}[✔] Desktop searches completed.{Colors.ENDC}")
        desktop_driver.quit()

    if choice in ['2', '3']:
        mobile_driver = setup_driver(is_mobile=True)
        perform_searches(mobile_driver, all_keywords, NUM_MOBILE_SEARCHES, "Mobile")
        print(f"{Colors.GREEN}[✔] Mobile searches completed.{Colors.ENDC}")
        mobile_driver.quit()

    print(f"\n{Colors.GREEN}{Colors.BOLD}╔════════════════════════════════════════════╗")
    print(f"║     All tasks finished successfully!     ║")
    print(f"╚════════════════════════════════════════════╝{Colors.ENDC}")