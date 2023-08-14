from typing import Optional, List, Dict
from fastapi import APIRouter, Query, Body, Path
from pydantic import BaseModel

router = APIRouter(
    prefix='/blog',
    tags=['blog']
)

#-----------------------------------------------------------------------------------------#
class BlogModel(BaseModel):
  title: str
  content: str
  nb_comments: int
  published: Optional[bool]
#-----------------------------------------------------------------------------------------#
# blank return.
@router.post('/new_blank')
def create_blog():
  pass
#-----------------------------------------------------------------------------------------#
# post with data retrun.
@router.post('/new')
def create_blog(blog: BlogModel):
  return {'data': blog}
#-----------------------------------------------------------------------------------------#
# post with parameters.
@router.post('/new_q/{id}')
def create_blog(blog: BlogModel, id: int, version: int = 1):
  return {
    'id': id,
    'data': blog,
    'version': version
}
#-----------------------------------------------------------------------------------------#
# post with query
@router.post('/new/{id}/comment')
def create_comment(blog: BlogModel, id: int,
        comment_id: int = Query(None,
            title='Id of the comment',
            description='Some description for comment_id',
            alias='commentId', # if needed a different name
            deprecated=True # if variable is deprecated
        )
    ):
    return {
        'blog': blog,
        'id': id,
        'comment_id': comment_id
    }
#-----------------------------------------------------------------------------------------#
# post with query and Body
@router.post('/new_body/{id}/comment')
def create_comment(blog: BlogModel, id: int,
        comment_id: int = Query(None,
            title='Id of the comment',
            description='Some description for comment_id',
            alias='commentId',
            deprecated=True
        ),
        # content: str = Body("Hello world") # default body
        # content: str = Body(...) # non-optional body
        #content: str = Body(Ellipsis) # other way for non-optional body
        content: str = Body(...,
           min_length=10, # min lenght of string
           max_length=50, # max lenght of string
           regex='^[a-z\s]*$' # regex to be applied on string.
        )
    ):
    return {
        'blog': blog,
        'id': id,
        'comment_id': comment_id,
        'content': content
    }
#-----------------------------------------------------------------------------------------#
# multiple vlaue parameters.
# url would be like : http://127.0.0.1:8000/blog/new_multi_param/2/comment?commentId=34&v=1.0&v=1.1&v=1.2
# above v is a query with type string
@router.post('/new_multi_param/{id}/comment')
def create_comment(blog: BlogModel, id: int,
        comment_id: int = Query(None,
            title='Id of the comment',
            description='Some description for comment_id',
            alias='commentId',
            deprecated=True
        ),
        content: str = Body(...,
            min_length=10,
            max_length=50,
            regex='^[a-z\s]*$'
        ),
        v: Optional[List[str]] = Query(['1.0', '1.1', '1.2']), # with default val
        #v: Optional[List[str]] = Query(), # no default value
    ):
    return {
        'blog': blog,
        'id': id,
        'comment_id': comment_id,
        'content': content,
        'version': v
    }
#-----------------------------------------------------------------------------------------#
# fastapi has 4 validators
# 1. greater than,
# 2. greater than or equal to,
# 3. less than,
# 4. less than or equal to.
# this helps in validating the parameters for path

@router.post('/new_valid/{id}/comment/{comment_id}')
def create_comment(blog: BlogModel, id: int,
        comment_title: int = Query(None,
            title='Title of the comment',
            description='Some description for comment_title',
            alias='commentTitle',
            deprecated=True
        ),
        content: str = Body(...,
            min_length=10,
            max_length=50,
            regex='^[a-z\s]*$'
        ),
        v: Optional[List[str]] = Query(['1.0', '1.1', '1.2']),
        # this will take value less than 5 and greate then 10
        comment_id: int = Path(..., gt=5, le=10)
    ):
    return {
        'blog': blog,
        'id': id,
        'comment_title': comment_title,
        'content': content,
        'version': v,
        'comment_id': comment_id
    }
#-----------------------------------------------------------------------------------------#

# compelx subtypes

# just assuming we have an image to display.
class Image(BaseModel):
    url: str
    alias: str

class BlogModelComplex(BaseModel):
    title: str
    content: str
    nb_comments: int
    published: Optional[bool]
    tags: List[str] = [] #list as param
    metadata: Dict[str, str] = {'key1': 'val1'} # dict as param
    image: Optional[Image] = None # class as param

@router.post('/new_complex/{id}/comment/{comment_id}')
def create_comment(blog: BlogModelComplex, id: int,
        comment_title: int = Query(None,
            title='Title of the comment',
            description='Some description for comment_title',
            alias='commentTitle',
            deprecated=True
        ),
        content: str = Body(...,
            min_length=10,
            max_length=50,
            regex='^[a-z\s]*$'
        ),
        v: Optional[List[str]] = Query(['1.0', '1.1', '1.2']),
        comment_id: int = Path(..., gt=5, le=10)
    ):
    return {
        'blog': blog,
        'id': id,
        'comment_title': comment_title,
        'content': content,
        'version': v,
        'comment_id': comment_id
    }
#-----------------------------------------------------------------------------------------#
# how depends functionality works
def required_functionality():
  return {'message': 'Learning FastAPI is important'}