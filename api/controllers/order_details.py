from sqlalchemy.orm import Session
from fastapi import HTTPException, status, Response, Depends
from ..models import models, schemas


def create(db: Session, detail):
    # Create a new instance of the Order model with the provided data
    db_detail = models.OrderDetail(
        detail_name=detail.detail_name,
        description=detail.description
    )
    # Add the newly created Order object to the database session
    db.add(db_detail)
    # Commit the changes to the database
    db.commit()
    # Refresh the Order object to ensure it reflects the current state in the database
    db.refresh(db_detail)
    # Return the newly created Order object
    return db_detail


def read_all(db: Session):
    return db.query(models.OrderDetail).all()


def read_one(db: Session, detail_id):
    return db.query(models.OrderDetail).filter(models.OrderDetail.id == detail_id).first()


def update(db: Session, detail_id, detail):
    # Query the database for the specific order detail to update
    db_detail = db.query(models.OrderDetail).filter(models.OrderDetail.id == detail_id)
    # Extract the update data from the provided 'order' object
    update_data = detail.model_dump(exclude_unset=True)
    # Update the database record with the new data, without synchronizing the session
    db_detail.update(update_data, synchronize_session=False)
    # Commit the changes to the database
    db.commit()
    # Return the updated order record
    return db_detail.first()


def delete(db: Session, detail_id):
    # Query the database for the specific order to delete
    db_detail = db.query(models.OrderDetail).filter(models.OrderDetail.id == detail_id)
    # Delete the database record without synchronizing the session
    db_detail.delete(synchronize_session=False)
    # Commit the changes to the database
    db.commit()
    # Return a response with a status code indicating success (204 No Content)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
