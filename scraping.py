from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd
import datetime as dt
from webdriver_manager.chrome import ChromeDriverManager


def scrape_all():
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=True)

    news_title, news_paragraph = mars_news(browser)

    # Run all scraping functions and store results
    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": featured_image(browser),
        "facts": mars_facts(),
        "hemispheres": hemispheres(browser),
        "last_modified": dt.datetime.now()
    }

    browser.quit()
    return data


def mars_news(browser):
    # NASA mars news site
    url = 'https://redplanetscience.com/'
    browser.visit(url)

    browser.is_element_present_by_css('div.list_text', wait_time=1)

    # Html to a soup object
    html = browser.html
    news_soup = soup(html, 'html.parser')

    try:
        slide_elem = news_soup.select_one('div.list_text')
        # News title
        news_title = slide_elem.find('div', class_='content_title').get_text()
        # Paragraph
        news_paragraph = slide_elem.find('div', class_='article_teaser_body').get_text()

    except AttributeError:
        return None, None

    return news_title, news_paragraph


def featured_image(browser):
    url = 'https://spaceimages-mars.com'
    browser.visit(url)

    # Navigate to full image
    full_image_elem = browser.find_by_tag('button')[1]
    full_image_elem.click()

    # HTML to soup
    html = browser.html
    img_soup = soup(html, 'html.parser')

    try:
        # Get relative path
        img_url_relative = img_soup.find('img', class_='fancybox-image').get('src')

    except AttributeError:
        return None

    # Create full url
    img_url = f'https://spaceimages-mars.com/{img_url_relative}'

    return img_url


def mars_facts():
    try:
        # Pandas to convert HTML to Dataframe & cleanup
        comparison_df = pd.read_html('https://galaxyfacts-mars.com')[0]

    except BaseException:
        return None

    comparison_df.columns=['Description', 'Mars', 'Earth']
    comparison_df.set_index('Description', inplace=True)

    # Output for use on my webpage
    return comparison_df.to_html(classes="table table-striped")


def hemispheres(browser):
    url = 'https://marshemispheres.com/'
    browser.visit(url)

    hemisphere_image_urls = []

    # Retrieve titles and images
    links = browser.find_by_css('a.product-item img')

    for i in range(len(links)):
        hemisphere = {}   
        browser.find_by_css('a.product-item img')[i].click()
        
        # Find image
        find_sample = browser.links.find_by_text('Sample').first
        hemisphere['img_url'] = find_sample['href']
        
        # Find title
        hemisphere['title'] = browser.find_by_css('h2.title').text

        hemisphere_image_urls.append(hemisphere)
        browser.back()

    return hemisphere_image_urls

if __name__ == "__main__":
    print(scrape_all())