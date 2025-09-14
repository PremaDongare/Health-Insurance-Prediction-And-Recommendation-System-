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

## Project Structure

```
├── frontend/                 # React.js frontend
│   ├── public/
│   ├── src/
│   │   ├── components/      # React components
│   │   ├── App.js          # Main app component
│   │   ├── index.js        # Entry point
│   │   └── index.css       # Tailwind CSS
│   ├── package.json
│   └── tailwind.config.js
├── backend/                 # Python FastAPI backend
│   ├── main.py             # FastAPI application
│   ├── insurance_model_utils.py  # ML model utilities
│   ├── chatbot_rag.py      # RAG chatbot implementation
│   ├── Company data.csv    # Insurance plans data
│   ├── TrainingModel/      # ML model files
│   └── requirements.txt
└── README.md
```

## Setup Instructions

### Prerequisites
- Node.js (v16 or higher)
- Python (v3.8 or higher)
- pip

### Backend Setup

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   ```

3. Activate the virtual environment:
   - Windows: `venv\Scripts\activate`
   - macOS/Linux: `source venv/bin/activate`

4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

5. Create a `.env` file in the backend directory with your API keys:
   ```
   Google_Gemani_API=your_google_gemini_api_key
   GROQ_API_KEY=your_groq_api_key
   ```

6. Run the backend server:
   ```bash
   python main.py
   ```

The backend will be available at `http://localhost:8000`

### Frontend Setup

1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Start the development server:
   ```bash
   npm start
   ```

The frontend will be available at `http://localhost:3000`

## API Endpoints

### Insurance Prediction
- **POST** `/predict-insurance`
- **Body**: JSON with age, sex, bmi, children, smoker, region
- **Response**: Estimated price and AI recommendations

### Chatbot
- **POST** `/chatbot`
- **Body**: JSON with query string
- **Response**: AI-generated answer

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

## Environment Variables

Create a `.env` file in the backend directory:

```
Google_Gemani_API=your_google_gemini_api_key_here
GROQ_API_KEY=your_groq_api_key_here
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is licensed under the MIT License.
