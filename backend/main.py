from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from models.legal_model import LegalModel
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4321"],  # frontend origin
    allow_methods=["POST"],
    allow_headers=["Content-Type"],
)
legal_model = LegalModel()

@app.post("/api/legal-assist/")
async def legal_assistance(request: Request):
    data = await request.json()
    question = data.get("question")
    if question:
        response = legal_model.get_advice(question)
        return JSONResponse(content={"answer": response})
    return JSONResponse(content={"error": "Invalid input"}, status_code=400)

# to-do
# - add api endpoints in Legalchat.astro http://localhost:8000/api/legal-assist/