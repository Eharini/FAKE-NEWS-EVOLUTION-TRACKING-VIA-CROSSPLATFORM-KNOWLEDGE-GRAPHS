from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ClaimRequest(BaseModel):
    claim: str

base_graph = {
    "nodes": [
        {"id": "claim1", "label": "Vaccine causes health issues", "type": "claim"},
        {"id": "post1", "label": "Tweet A", "platform": "twitter"},
        {"id": "post2", "label": "Reddit Post B", "platform": "reddit"},
        {"id": "post3", "label": "YouTube Video C", "platform": "youtube"},
        {"id": "fact1", "label": "Fact Check Article", "platform": "claim"}
    ],
    "links": [
        {"source": "claim1", "target": "post1", "weight": 1},
        {"source": "claim1", "target": "post2", "weight": 1},
        {"source": "claim1", "target": "post3", "weight": 1},
        {"source": "post3", "target": "fact1", "weight": 1}
    ]
}

@app.get("/graph")
def get_graph():
    return base_graph

@app.post("/evolution")
def analyze_claim(req: ClaimRequest):
    new_graph = {
        "nodes": list(base_graph["nodes"]),
        "links": list(base_graph["links"])
    }
    new_id = f"claim_{len(new_graph['nodes']) + 1}"
    new_claim = {"id": new_id, "label": f"Derived: {req.claim}", "type": "claim"}
    new_graph["nodes"].append(new_claim)
    new_links = [
        {"source": "claim1", "target": new_id, "weight": 1},
        {"source": new_id, "target": "post1", "weight": 1},
        {"source": new_id, "target": "post2", "weight": 1}
    ]
    new_graph["links"].extend(new_links)
    return {"message": "Claim evolution tracked successfully.", "graph": new_graph}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
