from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
import api

app = FastAPI()

#CORS for Laravel communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://project_detector.test",
        "http://localhost",
        "http://127.0.0.1",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ComparisonRequest(BaseModel):
    submissions: List[dict]
    language: str = "java"

class ComparisonResult(BaseModel):
    submission_a_id: str
    submission_b_id: str
    similarity_score: float

class DetectionResponse(BaseModel):
    results: List[ComparisonResult]

@app.get("/")
def root():
    return {"message": "Plagiarism Detection API", "status": "running"}

@app.post("/detect", response_model=DetectionResponse)
def detect_plagiarism(request: ComparisonRequest):
    try:
        if request.language.lower() == "java":
            detector = api.JavaSimilarityDetector()
        elif request.language.lower() == "python":
            detector = api.PythonSimilarityDetector()
        else:
            raise HTTPException(status_code=400, detail="Unsupported language")

        results = []
        submissions = request.submissions

        for i in range(len(submissions)):
            for j in range(i + 1, len(submissions)):
                code_a = submissions[i]['file_content']
                code_b = submissions[j]['file_content']

                score = detector.compare(code_a, code_b)

                if score > 0.5:
                    results.append(ComparisonResult(
                        submission_a_id=submissions[i]['id'],
                        submission_b_id=submissions[j]['id'],
                        similarity_score=round(score, 4)
                    ))

        results.sort(key=lambda x: x.similarity_score, reverse=True)

        return DetectionResponse(results=results)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8001)