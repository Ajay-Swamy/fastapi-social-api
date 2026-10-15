from sqlalchemy.orm import Session
from fastapi import FastAPI,Response,status,HTTPException,Depends,APIRouter
from .. import schemas,models
from ..database import get_db
from .. import oauth2
from typing import Optional,List
from sqlalchemy import func

router=APIRouter(
    prefix='/posts', # as all of our requests are containing /posts in the path we can use prefix to defaultly keep path prefix as /posts
    tags=['Posts']   # to create separate groups of users and posts in Swagger ui in fast api by "http://127.0.0.1:8000/docs"
)

#-------------------------Posts-------------------------------------------

# gets all posts 
@router.get("/",response_model=List[schemas.PostOut])
def get_posts(db: Session=Depends(get_db),user_id: int=Depends(oauth2.get_current_user)
              ,limit: int =10,skip:int =0,search: Optional[str]=""):
    # cursor.execute(""" SELECT * FROM posts """)
    # posts=cursor.fetchall()

    #posts=db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()

    posts=db.query(models.Post,func.count(models.Vote.post_id).label("votes")).join(
                         models.Vote,models.Vote.post_id==models.Post.id,isouter=True).group_by(models.Post.id).filter(
                            models.Post.title.contains(search)).limit(limit).offset(skip).all()
    #return [{"Post": post, "votes": votes} for post, votes in results]
    return posts
    


#creates new posts
@router.post("/",status_code=status.HTTP_201_CREATED,response_model=schemas.Post)
def createposts(post:schemas.PostCreate,db: Session=Depends(get_db),current_user: int=Depends(oauth2.get_current_user)):
    # cursor.execute(""" INSERT INTO posts (title,content,published) VALUES (%s,%s,%s) RETURNING * """,
    #                (post.title,post.content,post.published))
    # new_post=cursor.fetchone()
    # conn.commit()

    #new_post=models.Post(title=post.title,content=post.content,published=post.published)
    
    new_post=models.Post(owner_id=current_user.id,**post.model_dump()) #we are unpacking the dictionary it will automatically do like above comment but dynamically
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post



#gets posts with given ID
@router.get('/{id}',response_model=schemas.PostOut)
def get_posts(id:int,db: Session=Depends(get_db),current_user: int=Depends(oauth2.get_current_user) ):
    # cursor.execute("""  select * from posts where id= %s """,(str(id)))
    # post =cursor.fetchone()
    post=db.query(models.Post,func.count(models.Vote.post_id).label("votes")).join(
                             models.Vote,models.Vote.post_id==models.Post.id,isouter=True).group_by(
                                 models.Post.id).filter(models.Post.id==id).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,          # response.status_code=status.HTTP_404_NOT_FOUND
                            detail=f"post of id:{id} not found")            # return {"alert":f"post of id:{id} not found"}
        

    return post



#Deletes a post with given id
@router.delete("/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_posts(id: int,db: Session=Depends(get_db),current_user: int=Depends(oauth2.get_current_user)):

    # cursor.execute(""" delete from posts where id= %s returning * """,(str(id)))
    # deleted_post=cursor.fetchone()
    # conn.commit()

    post_query=db.query(models.Post).filter(models.Post.id== id)
    post=post_query.first()
    if post==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id {id} not found")
    
    #function to check whether the user is deleting his own posts
    if post.owner_id !=current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Not Authorised to perform the requested action")
    
    post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


#updates a post with id
@router.put("/{id}",response_model=schemas.Post)
def update_posts(id: int, updated_post: schemas.PostCreate,db: Session=Depends(get_db),current_user: int=Depends(oauth2.get_current_user)):

    # cursor.execute(""" update posts set title=%s, content=%s, published=%s where id=%s returning * """,
    #                (post.title,post.content,post.published,str(id)))

    # updated_post=cursor.fetchone()
    #conn.commit()

    post_query=db.query(models.Post).filter(models.Post.id== id)
    post=post_query.first()

    if post==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id {id} not found")

    #function to check whether the user is upxating his own posts
    if post.owner_id !=current_user.id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                                detail=f"Not Authorised to perform the requested action")
    post_query.update(updated_post.model_dump(),synchronize_session=False)
    db.commit()

    return post_query.first()
    
