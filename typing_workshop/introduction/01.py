# def foo(number: int) -> str:
#     return str(number)

# foo(10)
# foo("100")
# print(foo.__annotations__)





















# # you can put a lot of stuff there
# from typing import Annotated
# def foo(number: Annotated[int, "some message", "whatever", {"data": "in addition"}]) -> str:
#     return str(number)
# print(foo.__annotations__)

















# which can be used on many places

from fastapi import FastAPI, Query
from typing import Annotated

app = FastAPI()

@app.get("/items/")
async def read_items(q: Annotated[str, Query(max_length=50, min_length=3, regex="^[a-zA-Z0-9]*$")]):
    return {"query": q}


# or for DI


from typing import Annotated

from fastapi import Depends, FastAPI

app = FastAPI()


async def common_parameters(q: str | None = None, skip: int = 0, limit: int = 100):
    return {"q": q, "skip": skip, "limit": limit}


@app.get("/items/")
async def read_items(commons: Annotated[dict, Depends(common_parameters)]):
    return commons
