#!/usr/bin/env python
import warnings
import uvicorn 
import json
from typing import List, Dict, Any, Optional
from fastapi import FastAPI, HTTPException, BackgroundTasks, APIRouter, Depends
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from uuid import uuid4
from enum import StrEnum
from crew import ProblemFinder
from dotenv import load_dotenv
import os
import auth

load_dotenv()

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

# This main file is intended to be a way for you to run your
# crew locally, so refrain from adding unnecessary logic into this file.
# Replace with inputs you want to test with, it will automatically
# interpolate any tasks and agents information

class Status(StrEnum):
    RUNNING = "running"
    FINISHED = "finished"
    FAILED = "failed"
class ProblemFinderInput(BaseModel):
    documents: List[str]
    chat: List[Dict[str, Any]]
    check_list: str

class CrewItem(BaseModel):
    status: Status
    input: ProblemFinderInput
    output: List[str] = []
    error: Optional[str] = None

class ResponseData(BaseModel):
    status: Status
    output: Optional[List[str]] = None
    error: Optional[str] = None    

store: Dict[str, CrewItem] = {}

router = APIRouter(dependencies=[Depends(auth.validate_api_key)])

def run_kickoff(input_data: ProblemFinderInput, job_id: str):
    try:
        problemFinder = ProblemFinder()
        output = problemFinder.crew().kickoff(input_data.dict())
        
        store[job_id].status = Status.FINISHED
        store[job_id].output = json.loads(output.raw)
    except Exception as e:
        store[job_id].status = Status.FAILED
        store[job_id].error = str(e)

@router.post("/kickoff")
async def kickoff(input_data: ProblemFinderInput, background_tasks: BackgroundTasks):
    try:
        job_id = str(uuid4())
        background_tasks.add_task(run_kickoff, input_data, job_id)
        store[job_id] = CrewItem(status=Status.RUNNING, input=input_data)
        
        return {
            "job_id": job_id
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.get("/status/{job_id}")
async def get_status(job_id: str):
    try:
        if job_id not in store:
            raise HTTPException(status_code=404, detail=f"Job {job_id} not found")
        
        job = store[job_id]
        
        response = ResponseData(status=job.status)
        if job.status == Status.FAILED:
            response.error = job.error
            del store[job_id]  # Remove failed jobs
        elif job.status == Status.FINISHED:
            response.output = job.output
            del store[job_id]  # Remove completed jobs

        return jsonable_encoder(response, exclude_none=True)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
app = FastAPI(title="ProblemFinder API")
app.include_router(router=router, prefix="")

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=int(os.getenv("PORT", "10000")), reload=True)