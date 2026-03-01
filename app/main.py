"""API: structural gate boundary. No retries, no coercion."""

from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from app.llm_simulator import generate_output
from app.logging_config import configure_logging, get_logger
from app.validator import ValidationSuccess, validate

configure_logging()
logger = get_logger()

app = FastAPI(title="Structural Gate")


class InvokeRequest(BaseModel):
    mode: str


@app.post("/invoke")
def invoke(request: InvokeRequest):
    """
    Client -> Simulator -> Parse JSON -> Structural validation -> Accept or Reject.
    No silent correction, no retries, no auto-fix.
    """
    mode = request.mode
    try:
        raw = generate_output(mode)
    except ValueError as e:
        logger.info("validation_result=invalid", mode=mode, reason=str(e))
        return JSONResponse(
            status_code=400,
            content={"status": "rejected", "reason": str(e)},
        )
    result = validate(raw)

    if isinstance(result, ValidationSuccess):
        logger.info("validation_result=valid", mode=mode)
        return result.instance.model_dump()

    failure = result
    reason = failure.reason
    logger.info("validation_result=invalid", mode=mode, reason=reason)
    return JSONResponse(
        status_code=400,
        content={"status": "rejected", "reason": reason},
    )
