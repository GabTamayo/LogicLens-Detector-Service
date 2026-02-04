from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Any
import api

app = FastAPI()

# CORS for Laravel communication
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


class Submission(BaseModel):
    id: str
    code_content: str


class ComparisonResult(BaseModel):
    submission_a_id: str
    submission_b_id: str
    seq_score: float
    struct_score: float
    avg_score: float
    line_matches: List[Dict[str, Any]]


class DetectionRequest(BaseModel):
    submissions: List[Submission]
    language: str = "java"


class DetectionResponse(BaseModel):
    results: List[ComparisonResult]


@app.get("/")
def root():
    return {"message": "Plagiarism Detection API", "status": "running"}


@app.post("/detect", response_model=DetectionResponse)
def detect_plagiarism(request: DetectionRequest):
    try:
        # Select the proper detector
        lang = request.language.lower()
        if lang == "java":
            detector = api.JavaSimilarityDetector()
        elif lang == "python":
            detector = api.PythonSimilarityDetector()
        else:
            raise HTTPException(status_code=400, detail=f"Unsupported language: {request.language}")

        results = []

        for i in range(len(request.submissions)):
            for j in range(i + 1, len(request.submissions)):
                sub_a = request.submissions[i]
                sub_b = request.submissions[j]

                comparison = detector.compare(sub_a.code_content, sub_b.code_content)

                if comparison['avg_score'] > 0.85:  # adjust threshold if needed
                    results.append(ComparisonResult(
                        submission_a_id=sub_a.id,
                        submission_b_id=sub_b.id,
                        seq_score=round(comparison['seq_score'], 4),
                        struct_score=round(comparison['struct_score'], 4),
                        avg_score=round(comparison['avg_score'], 4),
                        line_matches=comparison['line_matches']
                    ))

        # Sort by avg_score descending
        results.sort(key=lambda x: x.avg_score, reverse=True)

        return DetectionResponse(results=results)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8001)
