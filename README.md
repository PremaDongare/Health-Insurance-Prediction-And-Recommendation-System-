# Health Insurance System

A modern web application for health insurance premium prediction and AI-powered chatbot assistance, built with React.js frontend and Python FastAPI backend.

## Features

- **Insurance Premium Calculator**: Predict health insurance costs using TensorFlow machine learning model
- **AI Chatbot**: Get answers about insurance terms, policies, and laws using RAG (Retrieval-Augmented Generation)
- **Professional UI**: Modern, responsive design with Tailwind CSS
- **Real-time Predictions**: Fast API responses with detailed recommendations

## Technology Stack

### Frontend
- React.js 18
- Tailwind CSS
- Axios for API calls
- Lucide React for icons

### Backend
- FastAPI
- TensorFlow for ML predictions
- LangChain for RAG implementation
- Google Gemini API for chatbot responses
- Groq API for insurance recommendations
- BeautifulSoup for web scraping

## Usage

1. **Insurance Calculator**: Fill in your details (age, gender, BMI, etc.) and get an estimated insurance premium with personalized recommendations.

2. **AI Chatbot**: Ask questions about health insurance terms, policies, or laws in India. The chatbot uses RAG to provide accurate, context-aware answers.

## Features in Detail

### Machine Learning Model
- Trained on medical insurance dataset
- Uses TensorFlow/Keras for predictions
- Preprocessed with LabelEncoder and StandardScaler

### RAG Implementation
- Web scrapes insurance glossary from SBI General
- Uses FAISS vector store for similarity search
- HuggingFace embeddings for text processing
- Google Gemini for generating responses

### Insurance Recommendations
- Filters insurance plans based on predicted budget
- Uses Groq API for intelligent plan recommendations
- Provides detailed feature comparisons


## License

This project is licensed under the MIT License.
**If you want to see the video implementation of Project you can just downlode the PPT and watch the video .**
