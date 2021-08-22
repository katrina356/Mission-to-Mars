
# Import Splinter, BeautifulSoup, and Pandas
from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd
import datetime as dt
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.driver import ChromeDriver


# create function to scrape all. Set up Splinter. This creates an instance of a splinter browser, using chrome
def scrape_all():
    # Initiate headless driver for deployment
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=True)

    # function will return two variables
    news_title, news_paragraph = mars_news(browser)

    # Run all scraping functions and store results in a dictionary
    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": featured_image(browser),
        "facts": mars_facts(),
        "last_modified": dt.datetime.now(),
        "mars": mars_data()
    }

    # Stop webdriver and return data
    browser.quit()
    return data


def mars_news(browser):

    # Visit the mars nasa news site
    url = 'https://redplanetscience.com'
    browser.visit(url)

    # Optional delay for loading the page. 
    browser.is_element_present_by_css('div.list_text', wait_time=1)


    # set up HTML Parser
    html = browser.html
    news_soup = soup(html, 'html.parser')

    try:
        
        # begin the scraping '.find' search specific information
        slide_elem = news_soup.select_one('div.list_text')
        #slide_elem.find('div', class_='content_title')  KH; this was removed, not certain if it should have been


        # Use the parent element to find the first `a` tag and save it as `news_title`
        news_title = slide_elem.find('div', class_='content_title').get_text()

        # Use the parent element to find the paragraph text
        news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
        
    except AttributeError:
        return None, None
    
    
    return news_title, news_p



def featured_image(browser):
    # Visit URL
    url = 'https://spaceimages-mars.com'
    browser.visit(url)


    # Find and click the full image button
    full_image_elem = browser.find_by_tag('button')[1]
    full_image_elem.click()


    # Parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')

    # Add try/except for error handling
    try:
        # Find the relative image url .get('src') pulls the link to the image
        img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
        
    except AttributeError:
        return None


    # Use the base URL to create an absolute URL
    img_url = f'https://spaceimages-mars.com/{img_url_rel}'
    
    #browser.quit()
    return img_url


def mars_facts():
    # Add try/except for error handling
    try:
        # create new dataframe from the HTML table
        df = pd.read_html('https://galaxyfacts-mars.com')[0]

    except BaseException:
        return None
    df.columns=['description', 'Mars', 'Earth']
    # set_index function changes description to an index. inplace means index will remain in place
    df.set_index('description', inplace=True)

    # insert panda function to convert dataframe back into HTML
    return df.to_html()
    
def mars_data(browser):
    
    url = 'https://marshemispheres.com/'

    browser.visit(url)
    
    hemisphere_image_urls = []
    
    for i in range(4):
        print(i)
    browser.find_by_tag('h3')[i].click()
    
    
    #parse with soup
    html = browser.html
    hem_soup = soup(html, 'html.parser')
    
    #Find the image
    img_link = hem_soup.find('div', class_= "downloads")
    
    img_div = (img_link.find('a').get('href'))
    
    hemisphere_title = hem_soup.select_one('h2.title').text
    
    print(hemisphere_title)
    
    #add to a dictionary the img and the title
    hemisphere_dict = {
        "img": f'{url}{img_div}',
        "title": hemisphere_title
      }
    
    hemisphere_image_urls.append(hemisphere_dict)
    browser.back()
    
    return mars_data

#if __name__ == "__main__":
    # If running as script, print scraped data
    #print(scrape_all())
    





