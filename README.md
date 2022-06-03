# Web Scraping Demo

## Objective:
Create a Flask App which can scrape NASA websites for mars data, load into mongo database, then display results on the page!

## Tools used:
- Jupyter Notebook
- MongoDB
- BeautifulSoup
- Splinter
- Python
- HTML / Bootstrap
- Flask

## Results:
![webpage_preview](https://github.com/Ryndine/web_scraping_demo/blob/main/resources/webpage_preview.jpg)

**News:**  
Webpage: [https://redplanetscience.com/](https://redplanetscience.com/)

Output the page to HTML with BS, then use a get_text() for the title and the paragraph text.

**Featured Image:**  
Webpage: [https://spaceimages-mars.com](https://spaceimages-mars.com)

Output the page to HTML with BS, then get the relative path text for the featured image and append it to the webpage url to generate a full link to the image.

**Facts:**  
Webpage: [https://galaxyfacts-mars.com](https://galaxyfacts-mars.com)

Use the read_html() function in pandas to create a dataframe, cleanup the dataframe, then use the to_html() function to prepare it for my webpage.

**Hemisphere Images & Titles:**  
Webpage: [https://marshemispheres.com/](https://marshemispheres.com/)

```
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
```

**Flask App:**  
```
@app.route("/scrape")
def scrape():
    mars = mongo.db.mars
    mars_data = scraping.scrape_all()
    mars.update_one({}, {"$set": mars_data}, upsert=True)
    return redirect('/', code=302)
```
I have my flask app setup to connect to mongo database, and run my script when the button on the webpage is clicked.
```
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
```
The Flask App runs this script, which will run all the above scripts I created and store them into a dictionary for mongodb.

From there my page displays the results of the scrape!
