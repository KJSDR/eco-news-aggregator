import requests
from bs4 import BeautifulSoup
from database import SessionLocal, Article


NEWS_SOURCES = [
    {
        "name": "BBC News",
        "url": "https://www.bbc.com/news/science_and_environment",
        "logo": "/static/bbclogo.jpg",
        "required_url_part": "/news/science_and_environment"
    },
    {
        "name": "National Geographic",
        "url": "https://www.nationalgeographic.com/environment",
        "logo": "/static/natgeo.webp",
        "required_url_part": "/environment"
    }
]

def fetch_articles():
    session = SessionLocal()
    articles = []

    for source in NEWS_SOURCES:
        response = requests.get(source["url"])
        print(f"Fetching from {source['url']} - Status Code: {response.status_code}")

        if response.status_code != 200:
            continue

        soup = BeautifulSoup(response.text, "html.parser")

        
        if "bbc.com" in source["url"]:
            article_elements = soup.find_all("a", class_="ssrcss-a4w391-PromoLink exn3ah92")

        
        elif "nationalgeographic.com" in source["url"]:
            article_elements = soup.find_all("a")

        for item in article_elements:
            title = item.get_text(strip=True)
            link = item.get("href", "")

            
            if link.startswith("/news"):
                link = f"https://www.bbc.com{link}"

            
            if source["required_url_part"] not in link:
                continue  

            
            if not title or not link.startswith("http"):
                continue

            
            existing_article = session.query(Article).filter(Article.link == link).first()
            if not existing_article:
                new_article = Article(
                    title=title,
                    link=link,
                    source_name=source["name"],
                    source_logo=source["logo"]
                )
                session.add(new_article)
                session.commit()

            articles.append({
                "title": title,
                "link": link,
                "source_name": source["name"],
                "source_logo": source["logo"]
            })

    session.close()
    return articles
