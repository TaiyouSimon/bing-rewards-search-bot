import time
import random
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.edge.service import Service as EdgeService
from webdriver_manager.microsoft import EdgeChromiumDriverManager
import subprocess
import sys

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
print(f"║        BING REWARDS SEARCH AUTOMATOR V3.1        ║")
print(f"╚══════════════════════════════════════════════════════╝{Colors.ENDC}")

print(f"\n{Colors.BOLD}{Colors.RED}CRITICAL INSTRUCTIONS (READ FIRST):{Colors.ENDC}")
print(f"{Colors.RED}1. Make sure you are already logged into your Microsoft account in Edge.")
print(f"2. You MUST close all Microsoft Edge windows before running this script.{Colors.ENDC}")

print(f"\n{Colors.YELLOW}Disclaimer: Automating searches may be against the Microsoft")
print(f"Rewards Terms of Service. Use this script at your own risk.{Colors.ENDC}\n")
print(f"{Colors.BLUE}============================================================{Colors.ENDC}")

def kill_edge_processes():
    """Kill all Edge and EdgeDriver processes."""
    try:
        # Kill Edge processes
        subprocess.run(['taskkill', '/f', '/im', 'msedge.exe'], 
                      capture_output=True, check=False)
        # Kill EdgeDriver processes
        subprocess.run(['taskkill', '/f', '/im', 'msedgedriver.exe'], 
                      capture_output=True, check=False)
        time.sleep(2)
        print(f"{Colors.GREEN}[✔] Cleaned up existing Edge processes{Colors.ENDC}")
    except Exception as e:
        print(f"{Colors.YELLOW}[!] Note: Could not kill processes (this is usually fine): {e}{Colors.ENDC}")

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
    """Sets up the Selenium Edge driver with improved error handling."""
    # Clean up any existing processes first
    kill_edge_processes()
    
    options = EdgeOptions()
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option('excludeSwitches', ['enable-automation'])
    options.add_experimental_option('useAutomationExtension', False)
    options.add_argument("--disable-web-security")
    options.add_argument("--allow-running-insecure-content")
    options.add_argument("--disable-extensions")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

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

    # Try multiple approaches to get the driver working
    attempts = 0
    max_attempts = 3
    
    while attempts < max_attempts:
        try:
            attempts += 1
            print(f"{Colors.YELLOW}[+] Attempt {attempts}/{max_attempts}: Getting EdgeDriver...{Colors.ENDC}")
            
            # Method 1: Use webdriver_manager with cache clearing and forced download
            if attempts == 1:
                try:
                    # Clear the webdriver manager cache more thoroughly
                    import shutil
                    cache_locations = [
                        os.path.expanduser("~/.wdm"),
                        os.path.expanduser("~/AppData/Local/.wdm"), 
                        os.path.expanduser("~/AppData/Roaming/.wdm"),
                        os.path.join(os.getcwd(), ".wdm")
                    ]
                    for cache_dir in cache_locations:
                        if os.path.exists(cache_dir):
                            shutil.rmtree(cache_dir)
                            print(f"{Colors.CYAN}[+] Cleared webdriver cache: {cache_dir}{Colors.ENDC}")
                except:
                    pass
                
                # Force fresh download 
                service = EdgeService(EdgeChromiumDriverManager().install())
                driver = webdriver.Edge(service=service, options=options)
                
            # Method 2: Try without specifying service
            elif attempts == 2:
                print(f"{Colors.CYAN}[+] Trying without explicit service...{Colors.ENDC}")
                driver = webdriver.Edge(options=options)
                
            # Method 3: Try with explicit port
            else:
                print(f"{Colors.CYAN}[+] Trying with explicit port configuration...{Colors.ENDC}")
                service = EdgeService(port=0)  # Let it choose a free port
                driver = webdriver.Edge(service=service, options=options)
            
            # Test the connection
            driver.get("about:blank")
            print(f"{Colors.GREEN}[✔] Successfully started Edge driver on attempt {attempts}{Colors.ENDC}")
            return driver
            
        except Exception as e:
            print(f"{Colors.RED}[✖] Attempt {attempts} failed: {e}{Colors.ENDC}")
            if attempts < max_attempts:
                print(f"{Colors.YELLOW}[+] Waiting 5 seconds before next attempt...{Colors.ENDC}")
                time.sleep(5)
                kill_edge_processes()  # Clean up before next attempt
            else:
                print(f"{Colors.RED}[✖] All attempts failed. Troubleshooting steps:")
                print(f"    1. Make sure Microsoft Edge is installed and updated")
                print(f"    2. Close all Edge windows completely")
                print(f"    3. Run as administrator")
                print(f"    4. Check your antivirus isn't blocking the driver")
                print(f"    5. Try restarting your computer{Colors.ENDC}")
                sys.exit(1)

def perform_searches(driver, keywords, num_searches, device_type):
    """Performs the given number of searches using the provided driver."""
    print(f"{Colors.BLUE}[▶] Starting {device_type} searches...{Colors.ENDC}")
    
    try:
        driver.get("https://www.bing.com")
        time.sleep(5)  # Increased wait time
    except Exception as e:
        print(f"{Colors.RED}[✖] Could not load Bing.com: {e}{Colors.ENDC}")
        return

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
            try:
                driver.refresh()
                time.sleep(5)
            except:
                print(f"{Colors.RED}[!] Could not recover. Skipping this search.{Colors.ENDC}")

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

    try:
        if choice in ['1', '3']:
            desktop_driver = setup_driver(is_mobile=False)
            perform_searches(desktop_driver, all_keywords, NUM_DESKTOP_SEARCHES, "Desktop")
            print(f"{Colors.GREEN}[✔] Desktop searches completed.{Colors.ENDC}")
            desktop_driver.quit()
            time.sleep(3)  # Brief pause between desktop and mobile

        if choice in ['2', '3']:
            mobile_driver = setup_driver(is_mobile=True)
            perform_searches(mobile_driver, all_keywords, NUM_MOBILE_SEARCHES, "Mobile")
            print(f"{Colors.GREEN}[✔] Mobile searches completed.{Colors.ENDC}")
            mobile_driver.quit()

        print(f"\n{Colors.GREEN}{Colors.BOLD}╔════════════════════════════════════════════╗")
        print(f"║     All tasks finished successfully!     ║")
        print(f"╚════════════════════════════════════════════╝{Colors.ENDC}")
        
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}[!] Script interrupted by user{Colors.ENDC}")
    except Exception as e:
        print(f"\n{Colors.RED}[✖] Unexpected error: {e}{Colors.ENDC}")
    finally:
        # Clean up any remaining processes
        kill_edge_processes()