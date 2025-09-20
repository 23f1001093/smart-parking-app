from celery import Celery
from models import db, Reservation, User
import csv

celery = Celery("tasks", broker="redis://localhost:6379/0")

@celery.task
def export_user_reservations(user_id, email):
    reservations = Reservation.query.filter_by(user_id=user_id).all()
    if not reservations:
        return
    filename = f"user_{user_id}_reservations.csv"
    with open(filename, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=list(reservations[0].serialize().keys()))
        writer.writeheader()
        for r in reservations:
            writer.writerow(r.serialize())
    # Email/send notification logic goes here
    return filename

