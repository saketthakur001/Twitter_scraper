from selenium import webdriver
from selenium.webdriver.edge.service import Service

# initialize edge options
edge_options = webdriver.EdgeOptions()

# add user data directory argument
edge_options.add_argument("--user-data-dir=/tmp/edgeprofile")

# initialize edge driver
driver = webdriver.Edge(service=Service(executable_path="/home/saket/path/msedgedriver"), options=edge_options)


# from msedge.selenium_tools import Edge, EdgeOptions  # Import Edge from msedge.selenium_tools
# import time

# # Initialize EdgeOptions
# options = EdgeOptions()
# options.use_chromium = True  # Use Chromium-based Edge
# options.add_argument("--user-data-dir=/tmp/edgeprofile")

# # Initialize the Edge driver
# driver = Edge(options=options, executable_path='/path/to/msedgedriver')  # Use Edge from msedge.selenium_tools

# # Navigate to Twitter
# driver.get('https://twitter.com/home')

# # Sleep for demonstration
# time.sleep(1000)
