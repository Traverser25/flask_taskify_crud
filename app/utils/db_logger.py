import logging
from app.extensions import db
from app.models.log import Log


class DBHandler(logging.Handler):
    def emit(self, record):
        try:
            # Create a log entry from the record
            log_entry = self.format(record)
            
            # Ensure we have an application context when working with db

            log = Log(level=record.levelname, message=log_entry, source=record.name)
            db.session.add(log)
            db.session.commit()

        except Exception as e:
            # Fallback to file log if DB log fails
            print(f"Error logging to DB: {e}")
