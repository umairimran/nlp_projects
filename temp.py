from selenium import webdriver

# Set up the WebDriver (Make sure you have the correct driver installed)
driver = webdriver.Chrome()  # You can replace Chrome with Edge, Firefox, etc.

# Open a webpage
driver.get("https://www.google.com")

# Keep the browser open for a while
input("Press Enter to close the browser...")

# Close the browser
driver.quit()
