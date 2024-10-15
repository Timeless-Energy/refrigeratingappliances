from selenium import webdriver
from selenium_stealth import stealth
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


pathway = r"C:\\Programs\\refrigeratingappliances\\chromedriver_128\\chromedriver.exe"
service = Service(executable_path=pathway)
# service = Service(ChromeDriverManager().install())

def start_chrome():
    options = webdriver.ChromeOptions()   

    options.add_argument("start-maximized")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    ''' https://www.crx4chrome.com/ '''
    # options.add_extension("AdBlocker/adblock.crx")

    driver = webdriver.Chrome(service=service, options=options) 

    stealth(driver,
            languages=["en-US", "en"],
            vendor="Google Inc.",
            platform="Win32",
            webgl_vendor="Intel Inc.",
            renderer="Intel Iris OpenGL Engine",
            fix_hairline=True,
            )
    ''' driver test '''
    # driver.get("https://bot.sannysoft.com/")



    driver.get(url="https://eprel.ec.europa.eu/screen/product/refrigeratingappliances2019/")

    return driver







