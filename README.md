# Eco-News Aggregator 🌍📰
A web application that aggregates environmental news articles from BBC News and National Geographic and presents them in a visually appealing format.

### 📌 Features
Fetches the latest environmental news from BBC News and National Geographic.
Displays news articles in a grid layout with source logos.
Backend powered by FastAPI and PostgreSQL.
Frontend built with React and styled using Tailwind CSS.
## 1️⃣ Clone the Repository
git clone https://github.com/yourusername/eco-news.git cd eco-news

## 2️⃣ Set Up the Backend
### 📌 Create and Activate Virtual Environment
cd backend python3 -m venv venv source venv/bin/activate # On Windows use: venv\Scripts\activate

### 📌 Install Dependencies
pip install -r requirements.txt

### 📌 Set Up PostgreSQL Database
```
CREATE DATABASE econews;

CREATE TABLE articles (
    id SERIAL PRIMARY KEY,
    title VARCHAR(512) NOT NULL,
    link VARCHAR(1024) UNIQUE NOT NULL,
    source_name VARCHAR(255) NOT NULL,
    source_logo VARCHAR(1024) NOT NULL
);
```
### 📌 Start Backend Server
uvicorn main:app --reload

3️⃣ Set Up the Frontend
### 📌 Install Dependencies
cd ../frontend npm install

### 📌 Start React App
npm start
