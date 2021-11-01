#!/usr/bin/env python
# coding: utf-8

# In[1]:


# # Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd


# In[2]:


# Set up Splinter (path and browser)
executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)

#executable_path: unpack the dic we've stored the path in.
#headless=false: all of the browser's actions will be displayed in a Chrome window so we can see them.


# In[3]:


# Assign the url and instruct the browser to visit it
# Visit the mars nasa news site
url = 'https://redplanetscience.com'
browser.visit(url)
# Optional delay for loading the page
browser.is_element_present_by_css('div.list_text', wait_time=1)


# In[4]:


# set up the HTML parser
html = browser.html
news_soup = soup(html, 'html.parser')
slide_elem = news_soup.select_one('div.list_text')

#. is used to select classes (list_text). 'div.list_text' = <div /> tag w the class of list_text.


# In[5]:


#looking for a <div /> with a class of “content_title.” to identify the title.
slide_elem.find('div', class_='content_title')


# In[6]:


# Use the parent element to find the first `a` tag and save it as `news_title`
news_title = slide_elem.find('div', class_='content_title').get_text()
news_title


# In[7]:


# Use the parent element to find the paragraph text
news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
news_p


# ### Featured Images

# In[8]:


# Scrape image of another website
# Visit URL
url = 'https://spaceimages-mars.com'
browser.visit(url)


# In[9]:


# Find and click the full image button
# The browser finds an element by its tag. [1] = we want our browser to click the 2nd button
full_image_elem = browser.find_by_tag('button')[1]
# Splinter will click the image to view its full size
full_image_elem.click()

#after running this code, the automated browser auto "clicks" the button and change the view to an image


# In[10]:


# Parse the resulting html with soup
html = browser.html
img_soup = soup(html, 'html.parser')
img_soup


# In[14]:


# Find the relative image url (on the automated browser)
img_url_rel = img_soup.find('img', class_='headerimage').get('src')
img_url_rel


# In[15]:


# Use the base URL to create an absolute URL
img_url = f'https://spaceimages-mars.com/{img_url_rel}'
img_url


# In[16]:


# scrape the entire table in https://galaxyfacts-mars.com/
# Use read_html() search for & returns a list of tables found in the HTML
df = pd.read_html('https://galaxyfacts-mars.com')[0] #index 0 = pull only the first table it encounters

# assign columns to the new DataFrame for additional clarity
df.columns=['description', 'Mars', 'Earth']

#turning the Description column into the DataFrame's index
df.set_index('description', inplace=True) #inplace=True: the updated index will remain in place, no reassign the DataFrame to a new variable
df


# In[17]:


# convert DataFrame back into HTML-ready code
df.to_html()


# D1: Scrape High-Resolution Mars’ Hemisphere Images and Titles

# In[18]:


# 1. Use browser to visit the URL 
url = 'https://marshemispheres.com/'

browser.visit(url)


# In[20]:


# 2. Create a list to hold the images and titles.
hemisphere_image_urls = []

# 3. Write code to retrieve the image urls and titles for each hemisphere.
for i in range(3, 7):
    # Store img url and title to an empty dictionary
    hemisphere = {}
    
    # Find & click the hemisphere image link
    img_thumb = browser.find_by_tag('img')[i]
    img_thumb.click()
    
    # Parse the resulting html with soup
    html = browser.html
    hemisphere_soup = soup(html, 'html.parser')
    
    #Find the relative url for the image
    img_rel_url = hemisphere_soup.find('div', class_="downloads").ul.li.a.get('href')
    
    # Use the base URL to create an absolute URL
    img_url = f'https://marshemispheres.com/{img_rel_url}'
    
    # Get the title
    title = hemisphere_soup.find('div', class_="cover").h2.text
    
    # Save the hemisphere url and the title to the dictionary.
    hemisphere['img_url']= img_url
    hemisphere['title'] = title
    
    # Append the hemisphere dictionary to the list.
    hemisphere_image_urls.append(hemisphere)
       
    # Navigate back to the beginning.
    browser.back()


# In[21]:


# 4. Print the list that holds the dictionary of each image url and title.
hemisphere_image_urls


# In[22]:


#end the automated browsing session
browser.quit()


# In[ ]:




