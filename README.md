# Bing Rewards Search Automator

This Python script automates Bing searches to help users earn Microsoft Rewards points. It uses Selenium to control a Microsoft Edge browser instance, performing searches with keywords loaded from a file.

## Features

- Automates desktop and mobile Bing searches.
- Uses a `keywords.txt` file for search terms.
- Includes human-like delays to mimic natural browsing behavior.
- Provides clear instructions and disclaimers.

## Prerequisites

- **Microsoft Edge Browser**: Ensure Microsoft Edge is installed on your system.
- **Microsoft Account**: You must be logged into your Microsoft account in Edge before running the script.
- **Edge WebDriver**: Selenium requires the Edge WebDriver to control the browser. It should be automatically managed by `selenium-manager` if you have a recent version of Selenium.

## Setup

1.  **Install Python**: If you don't have Python installed, download it from [python.org](https://www.python.org/downloads/).

2.  **Install Dependencies**: Navigate to the script's directory in your terminal and install the required Python packages:

    ```bash
    pip install -r requirements.txt
    ```

3.  **Prepare `keywords.txt`**: Create a file named `keywords.txt` in the same directory as the script. Add one search keyword per line. The script will randomly select keywords from this file for searches.

    Example `keywords.txt`:

    ```
    weather forecast
    latest news
    python programming
    world history facts
    ```

## Usage

1.  **Close all Edge windows**: Before running the script, ensure all Microsoft Edge browser windows are closed.

2.  **Run the script**: You can run the script directly from your terminal:

    ```bash
    python auto_bing_search.py
    ```

    Alternatively, you can use the provided `run.bat` file (for Windows):

    ```bash
    run.bat
    ```

3.  **Follow the prompts**: The script will ask you to choose between Desktop searches, Mobile searches, or both. Enter your choice (1, 2, or 3) and press Enter.

    ```
    --- CHOOSE AN OPTION ---
     1. Desktop Searches Only
     2. Mobile Searches Only
     3. Both Desktop & Mobile Searches
    Enter your choice (1, 2, or 3):
    ```

4.  **Monitor the process**: The script will open Edge browser windows (which may appear and close quickly) and perform searches. Do not interact with the browser windows while the script is running.

## Important Notes

- **Disclaimer**: Automating searches may be against the Microsoft Rewards Terms of Service. Use this script at your own risk.
- **Troubleshooting**: If the script fails to start the Edge driver, ensure Edge is completely closed and that you have a stable internet connection.
- **Customization**: You can adjust the number of searches and delay times by modifying the `NUM_DESKTOP_SEARCHES`, `NUM_MOBILE_SEARCHES`, `MIN_DELAY_SECONDS`, `MAX_DELAY_SECONDS`, `MIN_TYPING_DELAY_SECONDS`, and `MAX_TYPING_DELAY_SECONDS` variables in the `auto_bing_search.py` file.
