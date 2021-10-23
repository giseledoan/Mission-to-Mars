# # Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd

# Set up Splinter (path and browser)
executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)
#executable_path: unpack the dic we've stored the path in.
#headless=false: all of the browser's actions will be displayed in a Chrome window so we can see them.

# Assign the url and instruct the browser to visit it
# Visit the mars nasa news site
url = 'https://redplanetscience.com'
browser.visit(url)
# Optional delay for loading the page
browser.is_element_present_by_css('div.list_text', wait_time=1)

# set up the HTML parser
html = browser.html
news_soup = soup(html, 'html.parser')
slide_elem = news_soup.select_one('div.list_text')
#. is used to select classes (list_text). 'div.list_text' = <div /> tag w the class of list_text.

#looking for a <div /> with a class of “content_title.” to identify the title.
slide_elem.find('div', class_='content_title')


# Use the parent element to find the first `a` tag and save it as `news_title`
news_title = slide_elem.find('div', class_='content_title').get_text()
news_title

# Use the parent element to find the paragraph text
news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
news_p


# ### Featured Images

# Scrape image of another website
# Visit URL
url = 'https://spaceimages-mars.com'
browser.visit(url)


# Find and click the full image button
# The browser finds an element by its tag. [1] = we want our browser to click the 2nd button
full_image_elem = browser.find_by_tag('button')[1]
# Splinter will click the image to view its full size
full_image_elem.click()

#after running this code, the automated browser auto "clicks" the button and change the view to an image

# Parse the resulting html with soup
html = browser.html
img_soup = soup(html, 'html.parser')


# Find the relative image url (on the automated browser)
img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
img_url_rel


# Use the base URL to create an absolute URL
img_url = f'https://spaceimages-mars.com/{img_url_rel}'
img_url

# scrape the entire table in https://galaxyfacts-mars.com/
# Use read_html() search for & returns a list of tables found in the HTML
df = pd.read_html('https://galaxyfacts-mars.com')[0] #index 0 = pull only the first table it encounters

# assign columns to the new DataFrame for additional clarity
df.columns=['description', 'Mars', 'Earth']

#turning the Description column into the DataFrame's index
df.set_index('description', inplace=True) #inplace=True: the updated index will remain in place, no reassign the DataFrame to a new variable
df


# convert DataFrame back into HTML-ready code
df.to_html()

#end the automated browsing session
browser.quit()




