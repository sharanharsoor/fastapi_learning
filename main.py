from typing import Optional
from fastapi import FastAPI, Request
from router import route_blog_get
from router import route_blog_post
from router import user
from router import article
from router import file
from auth import authentication
from db.database import engine
from db import models
from exceptions import StoryException
from fastapi.responses import JSONResponse
from router import product
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from templates import templates
import time
from client import html # import from client.py
from starlette.responses import HTMLResponse
from fastapi.websockets import WebSocket

app = FastAPI()
app.include_router(authentication.router)
app.include_router(templates.router)
app.include_router(file.router)
app.include_router(user.router)
app.include_router(article.router)
app.include_router(route_blog_get.router)
app.include_router(route_blog_post.router)
app.include_router(product.router)

@app.get('/hello')
def index():
  return {'message': 'Hello world!'}

@app.exception_handler(StoryException)
def story_exception_handler(request: Request, exc: StoryException):
  return JSONResponse(
    status_code=418,
    content={'detail': exc.name}
  )

# below code is for example to handle any HTTPException, but this shouldn't
# be used.
# @app.exception_handler(HTTPException)
# def custom_handler(request: Request, exc: StoryException):
#   return PlainTextResponse(str(exc), status_code=400)

models.Base.metadata.create_all(engine)

# CORS
origins = [
  'http://localhost:3000'
]

app.add_middleware(
  CORSMiddleware,
  allow_origins = origins,
  allow_credentials = True,
  allow_methods = ["*"],
  allow_headers = ['*']
)

# A middleware is a function that is processed with every request (before being
# processed by any specific path operation) as well as with every
# response before returning it.
# This function takes each request that comes to your application.
@app.middleware("http")
async def add_middleware(request: Request, call_next):
  start_time = time.time()
  response = await call_next(request)
  duration = time.time() - start_time
  response.headers['duration_api'] = str(duration)
  return response

@app.get("/")
async def get():
  return HTMLResponse(html)

clients = []

@app.websocket("/chat")
async def websocket_endpoint(websocket: WebSocket):
  await websocket.accept()
  clients.append(websocket)
  while True:
    data = await websocket.receive_text()
    #print(data)
    for client in clients:
      await client.send_text(data)
      #print(client)

app.mount('/files', StaticFiles(directory="files"), name='files')
app.mount('/templates/static',
      StaticFiles(directory="templates/static"),
      name="static"
)

'''
@app.post("/write_to_file/")
def write_to_file(text_data: TextData):
    try:
        with open("./output.txt", "w") as file:
            file.write(text_data.content)
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to write to file")
    return {"message": "Data written to file successfully"}

@app.get("/read_from_file/")
def read_from_file():
    try:
        with open("./output.txt", "r") as file:
            content = file.read()
            return {"content": content}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to read from file")

#@app.get("/blog/all")
#def all_blog():
#    return {"message": "all blogs provide"}

@app.get('/blog/all',tags=['blog'])
def get_blogs(page = 1, page_size: Optional[int] = None):
  return {'message': f'All {page_size} blogs on page {page}'}

@app.get('/blog/{id}/comments/{comment_id}', tags=['blog', 'comment'])
def get_comment(id: int, comment_id: int, valid: bool = True, username: Optional[str] = None):
  return {'message': f'blog_id {id}, comment_id {comment_id}, valid {valid}, username {username}'}

class BlogType(str, Enum):
    short = 'short'
    story = 'story'
    howto = 'howto'

@app.get('/blog/type/{type}',tags=['blog'])
def get_blog_type(type: BlogType):
  return {'message': f'Blog type {type}'}

@app.get("/blog/{id}", tags=['blog'])
def get_blog(id: int):
    return {"message": f"blog with id {id}"}

@app.get('/blog_resp/{id}', status_code=status.HTTP_200_OK,
tags=['blog'],
summary="Retrive some blogs",
description="this API helps in retriving blogs based on id's",
response_description ="gives blog id's"
)
def get_blog(id: int, response: Response):
  if id > 5:
    response.status_code = status.HTTP_404_NOT_FOUND
    return {'error': f'Blog {id} not found'}
  else :
    response.status_code = status.HTTP_200_OK
    return {'message': f'Blog with id {id}'}
'''