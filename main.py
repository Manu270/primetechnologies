from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time

# Set up headless Chrome browser
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--window-size=1920,1080")
chrome_options.add_argument("--no-sandbox")

# Start WebDriver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
driver.get("https://rera.odisha.gov.in/projects/project-list")

wait = WebDriverWait(driver, 20)

# Wait for the 'View Details' buttons to appear
wait.until(EC.presence_of_element_located((By.XPATH, "//a[contains(text(), 'View Details')]")))

data = []

for i in range(6):
    try:
        # Refresh the list of buttons every iteration
        view_buttons = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//a[contains(text(), 'View Details')]")))
        
        if i >= len(view_buttons):
            print(f"❌ Only {len(view_buttons)} 'View Details' buttons found.")
            break

        button = view_buttons[i]

        # Scroll and click
        driver.execute_script("arguments[0].scrollIntoView(true);", button)
        driver.execute_script("arguments[0].click();", button)

        # Wait for details to load
        wait.until(EC.presence_of_element_located((By.XPATH, "//span[@id='project_name']")))

        # Extract Project details
        rera_no = driver.find_element(By.XPATH, "//span[@id='rera_reg_no']").text.strip()
        project_name = driver.find_element(By.XPATH, "//span[@id='project_name']").text.strip()

        # Navigate to Promoter tab
        promoter_tab = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), 'Promoter Details')]")))
        promoter_tab.click()
        time.sleep(2)  # Small delay for tab content to load

        promoter_name = driver.find_element(By.XPATH, "//span[@id='company_name']").text.strip()
        promoter_address = driver.find_element(By.XPATH, "//span[@id='reg_office_address']").text.strip()
        gst_no = driver.find_element(By.XPATH, "//span[@id='gst_no']").text.strip()

        data.append({
            "RERA Regd. No": rera_no,
            "Project Name": project_name,
            "Promoter Name": promoter_name,
            "Address of Promoter": promoter_address,
            "GST No.": gst_no
        })

        # Go back to the main list
        driver.back()
        wait.until(EC.presence_of_element_located((By.XPATH, "//a[contains(text(), 'View Details')]")))

    except Exception as e:
        print(f"❌ Error on project {i+1}: {e}")
        try:
            driver.back()
            wait.until(EC.presence_of_element_located((By.XPATH, "//a[contains(text(), 'View Details')]")))
        except:
            pass

# Display the results
df = pd.DataFrame(data)
print("\n📋 Final Output:")
print(df)

# Close the browser
driver.quit()


# """
# Instructions:
# ---------------
# 1. Install required packages using:
#    pip install selenium pandas webdriver-manager

# 2. Run the script:
#    python3 main.py
# """

# from selenium import webdriver
# from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.common.by import By
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from webdriver_manager.chrome import ChromeDriverManager
# import pandas as pd
# import time

# # Set up headless Chrome browser
# chrome_options = Options()
# chrome_options.add_argument("--headless")
# chrome_options.add_argument("--disable-gpu")
# chrome_options.add_argument("--window-size=1920,1080")
# chrome_options.add_argument("--no-sandbox")

# # Start WebDriver
# driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
# driver.get("https://rera.odisha.gov.in/projects/project-list")

# wait = WebDriverWait(driver, 20)

# # Wait for at least one 'View Details' link to load
# wait.until(EC.presence_of_element_located((By.XPATH, "//a[contains(text(), 'View Details')]")))

# # Get first 6 'View Details' buttons
# view_buttons = driver.find_elements(By.XPATH, "//a[contains(text(), 'View Details')]")[:6]

# data = []

# for i, button in enumerate(view_buttons):
#     try:
#         # Scroll into view and click
#         driver.execute_script("arguments[0].scrollIntoView(true);", button)
#         driver.execute_script("arguments[0].click();", button)

#         # Wait for Project Name to load
#         wait.until(EC.presence_of_element_located((By.XPATH, "//span[@id='project_name']")))

#         # Extract RERA Regd. No and Project Name
#         rera_no = driver.find_element(By.XPATH, "//span[@id='rera_reg_no']").text.strip()
#         project_name = driver.find_element(By.XPATH, "//span[@id='project_name']").text.strip()

#         # Go to Promoter Details tab
#         promoter_tab = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), 'Promoter Details')]")))
#         promoter_tab.click()

#         # Allow tab to load
#         time.sleep(2)

#         # Extract Promoter details
#         promoter_name = driver.find_element(By.XPATH, "//span[@id='company_name']").text.strip()
#         promoter_address = driver.find_element(By.XPATH, "//span[@id='reg_office_address']").text.strip()
#         gst_no = driver.find_element(By.XPATH, "//span[@id='gst_no']").text.strip()

#         # Append extracted data
#         data.append({
#             "RERA Regd. No": rera_no,
#             "Project Name": project_name,
#             "Promoter Name": promoter_name,
#             "Address of Promoter": promoter_address,
#             "GST No.": gst_no
#         })

#         # Go back to the project list
#         driver.back()
#         wait.until(EC.presence_of_element_located((By.XPATH, "//a[contains(text(), 'View Details')]")))

#         # Refresh button list after navigating back
#         view_buttons = driver.find_elements(By.XPATH, "//a[contains(text(), 'View Details')]")
#     except Exception as e:
#         print(f" Error on project {i+1}: {e}")
#         driver.back()
#         view_buttons = driver.find_elements(By.XPATH, "//a[contains(text(), 'View Details')]")

# # Print final results
# df = pd.DataFrame(data)
# print("\n📋 Final Output:")
# print(df)

# # Quit browser
# driver.quit()






