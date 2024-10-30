from fastapi import FastAPI
from baml_client import b


app = FastAPI()

@app.post("/")
async def root():
    print("Received request")
    res = b.stream.ExtractResume("""
      Vaibhav Gupta
      vbv@boundaryml.com

      Experience:
      - Founder at BoundaryML
      - CV Engineer at Google
      - CV Engineer at Microsoft

      Skills:
      - Rust
      - C++
    """)
    for chunk in res:
        print(chunk)
    return res.get_final_response()
