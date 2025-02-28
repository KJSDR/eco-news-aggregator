import { useEffect, useState } from "react";
import axios from "axios";

function App() {
    const [articles, setArticles] = useState([]);

    useEffect(() => {
        axios.get("http://127.0.0.1:8000/news")
            .then(response => setArticles(response.data.articles))
            .catch(error => console.error("Error fetching news:", error));
    }, []);

    return (
        <div className="min-h-screen bg-green-700 p-6 flex flex-col items-left">
            <h1 className="text-3xl font-bold text-white mb-4 w-full text-center">Eco-News Aggregator</h1>
            <ul className="space-y-3 w-full max-w-md">
                {articles.map((article, index) => (
                    <li key={index} className="bg-white p-4 rounded shadow hover:bg-green-100 transition-colors flex justify-between items-center">
                        <a href={article.link} target="_blank" rel="noopener noreferrer" className="text-green-800 hover:text-green-600">
                            {article.title}
                        </a>
                    </li>
                ))}
            </ul>
        </div>
    );
}

export default App;
