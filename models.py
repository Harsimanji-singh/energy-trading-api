from sqlalchemy.orm import DeclarativeBase, Mapped, relationship, mapped_column
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text
import datetime
from sqlalchemy import ForeignKey


class Base(DeclarativeBase):
    type_annotation_map = {
        datetime.datetime: TIMESTAMP(timezone=True)

    }


class EnergyNft(Base):
    __tablename__ = "nft"
    # id: Mapped[int] = mapped_column()
    tokenId: Mapped[int] = mapped_column(primary_key=True)
    address: Mapped[str] = mapped_column(nullable=False)
    tokenUri: Mapped[str] = mapped_column(nullable=False)
    created_At: Mapped[datetime.datetime] = mapped_column(nullable=False, server_default=text('now()'
                                                                                              ))


class EnergyAuction(Base):
    __tablename__ = "auction"
    id: Mapped[int] = mapped_column(primary_key=True)
    tokenId: Mapped[int] = mapped_column(ForeignKey(
        "nft.tokenId", ondelete="CASCADE"), nullable=False)
    seller: Mapped[str] = mapped_column(nullable=False)
    startPrice: Mapped[int] = mapped_column(nullable=False)
    duration: Mapped[int] = mapped_column(nullable=False)
    startTimeStamp: Mapped[int] = mapped_column(nullable=False)
    endTimeStamp: Mapped[int] = mapped_column(nullable=False)
    created_At: Mapped[datetime.datetime] = mapped_column(nullable=False, server_default=text('now()'
                                                                                              ))
    auction = relationship("EnergyNft")
