from fastapi import FastAPI, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from database import SessionLocal, Article
from sqlalchemy.orm import Session
from scraping import fetch_articles


app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

# Allow frontend from port 3000
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def read_root():
    return {"message": "Eco-News Aggregator API"}

@app.get("/news")
def get_news(db: Session = Depends(get_db)):
    fetch_articles()
    articles = db.query(Article).all()
    return {
        "articles": [
            {
                "title": a.title,
                "link": a.link,
                "source_name": a.source_name,
                "source_logo": a.source_logo,
            }
            for a in articles
        ]
    }
