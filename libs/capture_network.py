import json
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from chromedriver_py import binary_path
# Initialize Chrome WebDriver with performance logging enabled
svc = webdriver.ChromeService(executable_path=binary_path)
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--remote-debugging-port=9222')  # Enable DevTools Protocol
chrome_options.add_argument("--incognito")
chrome_options.add_argument('--enable-logging')
chrome_options.add_argument("--ignore-certificate-errors")
chrome_options.add_argument("--disable-web-security")
chrome_options.add_argument("--allow-running-insecure-content")
driver = webdriver.Chrome(service=svc, options=chrome_options)


# Navigate to the target website
driver.get("https://www.linkvideo.download/")
WebDriverWait(driver, 30).until(
        lambda d: d.execute_script('return document.readyState') == 'complete'
)
test = driver.execute_async_script(
        """
        var performance = window.performance || window.mozPerformance || window.msPerformance || window.webkitPerformance || { };
        var callback = arguments[arguments.length - 1];
        if (performance) {
          if (typeof(performance.getEntries)==='function'){
            performance = performance.getEntriesByType('resource').map(entry => entry.name);
          };
          callback(performance);
        } else { callback(null);}"""
    )
#response = driver.execute_async_script("""var performance = window.performance || window.mozPerformance || window.msPerformance || window.webkitPerformance || { }; return performance;""")
print(test)
# Close the WebDriver
driver.quit()