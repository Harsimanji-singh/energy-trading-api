from fastapi import FastAPI, Depends, status, Response, HTTPException
from . import models, schemas
from .database import engine, get_db
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware

models.Base.metadata.create_all(bind=engine)
app = FastAPI()

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {"message": "Welcome to api"}


@app.get("/nft")
def get_datas(db: Session = Depends(get_db)):
    posts = db.query(models.EnergyNft).all()
    return posts


@app.get("/nft/{tokenId}")
def get_data(tokenId: int, db: Session = Depends(get_db)):
    post = db.query(models.EnergyNft).filter(
        models.EnergyNft.tokenId == tokenId).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"nft with tokenId{tokenId} not found")
    return post


@app.get("/nftlast")
def get_data(db: Session = Depends(get_db)):
    posts = db.query(models.EnergyNft).order_by(
        models.EnergyNft.tokenId.desc()).all()
    print(posts)
    if posts:
        return posts
    else:
        return {"tokenId": 0}


@app.post("/nft")
def create_nft(post: schemas.PostCreate, db: Session = Depends(get_db)):
    new_post = models.EnergyNft(
        tokenId=post.tokenId, address=post.address, tokenUri=post.tokenUri)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@app.post("/auction")
def create_auction(post: schemas.Auction, db: Session = Depends(get_db)):
    new_auction = models.EnergyAuction(tokenId=post.tokenId, seller=post.seller, startPrice=post.startPrice,
                                       duration=post.duration, startTimeStamp=post.startTimeStamp, endTimeStamp=post.endTimeStamp)
    db.add(new_auction)
    db.commit()
    db.refresh(new_auction)
    return new_auction


@app.get("/auction/{tokenId}")
def get_auction(tokenId: int, post: schemas.Auction, db: Session = Depends(get_db)):
    auction = db.query(models.EnergyAuction).filter(
        models.EnergyAuction.tokenId == tokenId).first()
    if not auction:
        return {}
    return auction


@app.get("/auctionlast")
def get_auctions(db: Session = Depends(get_db)):
    posts = db.query(models.EnergyAuction).order_by(
        models.EnergyAuction.tokenId.desc()).all()
    return posts


@app.delete("/auction/{tokenId}")
def delete_auction(tokenId: int, db: Session = Depends(get_db)):
    post_query = db.query(models.EnergyAuction).filter(
        models.EnergyAuction.tokenId == tokenId)
    post = post_query.first()
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id:{tokenId} does not exist")
    post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
