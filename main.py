from fastapi import FastAPI
from router import route_blog_get
from router import route_blog_post


app = FastAPI()
app.include_router(route_blog_get.router)
app.include_router(route_blog_post.router)


@app.get('/hello')
def index():
  return {'message': 'Hello world!'}


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