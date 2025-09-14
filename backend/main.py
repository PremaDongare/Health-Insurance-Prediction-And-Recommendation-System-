from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import insurance_model_utils
from chatbot_rag import get_answer_from_gemini
import uvicorn

app = FastAPI(title="Health Insurance API", version="1.0.0")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React app URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models for request/response
class InsurancePredictionRequest(BaseModel):
    age: int
    sex: str
    bmi: float
    children: int
    smoker: str
    region: str

class InsurancePredictionResponse(BaseModel):
    estimated_price: float

class RecommendationsRequest(BaseModel):
    price: float

class RecommendationsResponse(BaseModel):
    recommendations: str

class ChatbotRequest(BaseModel):
    query: str

class ChatbotResponse(BaseModel):
    answer: str

@app.get("/")
async def root():
    return {"message": "Health Insurance API is running"}

@app.post("/predict-insurance", response_model=InsurancePredictionResponse)
async def predict_insurance(request: InsurancePredictionRequest):
    try:
        # Validate input
        if request.age < 0 or request.age > 100:
            raise HTTPException(status_code=400, detail="Age must be between 0 and 100")
        if request.bmi < 10 or request.bmi > 50:
            raise HTTPException(status_code=400, detail="BMI must be between 10 and 50")
        if request.children < 0 or request.children > 10:
            raise HTTPException(status_code=400, detail="Children must be between 0 and 10")
        if request.sex not in ["male", "female"]:
            raise HTTPException(status_code=400, detail="Sex must be 'male' or 'female'")
        if request.smoker not in ["yes", "no"]:
            raise HTTPException(status_code=400, detail="Smoker must be 'yes' or 'no'")
        if request.region not in ["southeast", "southwest", "northeast", "northwest"]:
            raise HTTPException(status_code=400, detail="Invalid region")
        
        # Get prediction
        price = insurance_model_utils.predict_insurance(
            request.age, request.sex, request.bmi, 
            request.children, request.smoker, request.region
        )
        
        return InsurancePredictionResponse(
            estimated_price=price
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")

@app.post("/get-recommendations", response_model=RecommendationsResponse)
async def get_recommendations(request: RecommendationsRequest):
    try:
        # Get AI recommendations
        recommendations = insurance_model_utils.get_groq_recommendations(request.price)
        
        return RecommendationsResponse(
            recommendations=recommendations
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get recommendations: {str(e)}")

@app.post("/chatbot", response_model=ChatbotResponse)
async def chatbot_query(request: ChatbotRequest):
    try:
        if not request.query.strip():
            raise HTTPException(status_code=400, detail="Query cannot be empty")
        
        answer = get_answer_from_gemini(request.query)
        return ChatbotResponse(answer=answer)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Chatbot query failed: {str(e)}")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
