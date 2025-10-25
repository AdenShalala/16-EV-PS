import secrets
import database
from datetime import datetime
import hmac
import hashlib
from schema import Session

def generate_token() -> str:
    return secrets.token_urlsafe(24)

def hash_secret(secret: str) -> str:
    hash_object = hashlib.sha256()
    hash_object.update(secret.encode('utf-8'))
    return hash_object.hexdigest()

def validate_session(token: str) -> Session:
    split: list[str] = token.split('.')

    # ensure the token is only two parts
    if (len(split) != 2):
        return None
    
    # get session from database
    session: Session = get_session(split[0])
    if session == None:
        return None
    
    hashed_secret = hash_secret(split[1])

    valid: bool = hmac.compare_digest(session.secret_hash, hashed_secret)
    if not valid:
        return None
    
    if (datetime.now() - session.created_at).seconds >= 3600:
        session.last_verified_at = datetime.now()
        database.update_session_verified_at(session)

    return session

def get_session(session_id: str) -> Session:
    session = database.get_session(session_id)

    if session == None:
        return None
    
    if (datetime.now() - session.last_verified_at).days >= 7:
        database.delete_session(session.session_id)
        return None

    return session

def create_session(user_id: str, type: str) -> tuple[Session, str]:
    time = datetime.now()
    id = generate_token()
    secret = generate_token()
    hashed_secret = hash_secret(secret)
    token = id + "." + secret

    session = Session(id, user_id, type, hashed_secret, time, time)

    database.write_session(session)

    return session, token

def delete_session(session: Session) -> None:
    database.delete_session(session.session_id)