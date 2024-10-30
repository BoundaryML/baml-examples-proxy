
from typing import Any, Dict, Iterable, Optional, List, Union

from pydantic import BaseModel

from starlette.responses import StreamingResponse
from fastapi import FastAPI
from anthropic import AsyncAnthropic, MessageStreamEvent
from anthropic.resources.messages import MessageParam, ModelParam, MetadataParam, TextBlockParam, ToolChoiceParam, ToolParam

app = FastAPI(title="Anthropic-compatible API")


# data models
class Message(BaseModel):
    role: str
    content: str


class ChatCompletionRequest(BaseModel):
    max_tokens: int
    messages: Iterable[MessageParam]
    model: ModelParam
    metadata: Optional[MetadataParam] = None
    stop_sequences: Optional[List[str]] = None
    stream: Optional[bool] = False
    system: Optional[Union[str, Iterable[TextBlockParam]]] = None
    temperature: Optional[float] = None
    tool_choice: Optional[ToolChoiceParam] = None
    tools: Optional[Iterable[ToolParam]] = None
    top_k: Optional[int] = None
    top_p: Optional[float] = None


client = AsyncAnthropic(api_key="...")

@app.post("/v1/messages")
async def chat_completions(request: ChatCompletionRequest):
    if request.stream:
        stream = await client.messages.create(**request.model_dump(exclude_none=True))
        async def _gen():
            event: MessageStreamEvent
            async for event in stream:
                yield f"data: {event.model_dump_json()}\n\n"
            yield "data: [DONE]"
        return StreamingResponse(_gen(), media_type="text/event-stream")
    else:
        return await client.messages.create(**request.model_dump(exclude_none=True))


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8081)