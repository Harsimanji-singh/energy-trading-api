from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class PostBase(BaseModel):
    tokenId: int
    address: str
    tokenUri: str


class PostCreate(PostBase):
    pass


class Auction(BaseModel):
    tokenId: int
    seller: str
    startPrice: int
    duration: int
    startTimeStamp: int
    endTimeStamp: int
