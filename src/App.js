import { useEffect, useState } from "react";
import axios from "axios";
import backgroundImage from "./background.jpg";

function App() {
    const [articles, setArticles] = useState([]);

    useEffect(() => {
        axios.get("http://127.0.0.1:8000/news")
            .then(response => setArticles(response.data.articles))
            .catch(error => console.error("Error fetching news:", error));
    }, []);

    return (
        <div 
            className="relative min-h-screen flex flex-col items-center p-4"
            style={{ 
                backgroundImage: `url(${backgroundImage})`, 
                backgroundSize: "cover", 
                backgroundPosition: "center" 
            }}
        >
            {/* Dark Overlay */}
            <div className="absolute inset-0 bg-black bg-opacity-50"></div>

            {/* Content */}
            <div className="relative z-10 text-center w-full">
                <h1 className="text-4xl font-bold text-green-400 mb-6">Eco-News Aggregator</h1>
                
                <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-6">
                    {articles.map((article, index) => (
                        <div key={index} className="bg-white shadow-md rounded-lg p-4 flex flex-col items-center ">
                            {/* Source Logo */}
                            <img 
                                src={`http://127.0.0.1:8000${article.source_logo}`} 
                                alt={article.source_name} 
                                className="h-12 w-auto mb-2"
                            />
                            
                            {/* Article Title */}
                            <a 
                                href={article.link} 
                                target="_blank" 
                                rel="noopener noreferrer" 
                                className="text-lg font-semibold text-gray-800 text-center hover:underline"
                            >
                                {article.title}
                            </a>
                        </div>
                    ))}
                </div>
            </div>
        </div>
    );
}

export default App;
