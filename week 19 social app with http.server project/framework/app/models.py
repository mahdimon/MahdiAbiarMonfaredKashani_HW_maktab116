from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Date, create_engine
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime, timedelta
from sqlalchemy.orm import sessionmaker, joinedload, relationship
from sqlalchemy.exc import IntegrityError
from bcrypt import gensalt, hashpw, checkpw
import uuid

Base = declarative_base()
engine = create_engine("sqlite:///social-media.db", echo=True)
db_Session = sessionmaker(bind=engine)


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    password = Column(String(20), nullable=False)
    email = Column(String(50), nullable=False, unique=True)
    last_login = Column(DateTime)

    posts = relationship("Post", back_populates="user",
                         cascade="all, delete-orphan")
    session = relationship("Session",uselist=False, back_populates="user")

    @classmethod
    def add_user(cls, name, email, password1, password2):
        if password1 != password2 or len(password1) < 6:
            return {"error": "passwords doesnt match"}

        hashed_password = hashpw(password1.encode(), gensalt())

        user = cls(
            name=name,
            password=hashed_password,
            email=email
        )

        with db_Session() as session:
            session.add(user)
            try:
                session.commit()
            except IntegrityError as e:
                session.rollback()
                error_info = str(e.orig)
                if 'email' in error_info.lower():
                    return {"error": "email already exists"}


class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    create_at = Column(DateTime, default=datetime.now())
    body = Column(String, nullable=False)
    parent_id = Column(Integer, ForeignKey("posts.id"), nullable=True)

    user = relationship("User", back_populates="posts")
    parent = relationship("Post", remote_side=[id], back_populates="comments")
    comments = relationship(
        "Post", back_populates="parent", cascade="all, delete-orphan")

    @classmethod
    def get_posts(cls):
        with db_Session() as session:
            posts = session.query(cls).options(joinedload(
                cls.user)).filter(cls.parent_id == None).order_by(cls.create_at.desc()).all()
            return [(post.body, post.user.name, post.id) for post in posts]

    @classmethod
    def get_post_by_id(cls, id):
        with db_Session() as session:
            post = session.query(cls).filter(cls.id == id).one_or_none()

            if post:
                author_name = post.user.name
                comments_data = [
                    (comment.body, comment.user.name)
                    for comment in sorted(post.comments, key=lambda c: c.create_at, reverse=True)
                ]

                return {
                    "post_body": post.body,
                    "author_name": author_name,
                    "comments": comments_data,
                }

        return None

    @classmethod
    def add_post(cls, user_id, body, parent_id=None):
        with db_Session() as session:
            new_post = cls(
                user_id=user_id,
                body=body,
                parent_id=parent_id
            )
            session.add(new_post)
            try:
                session.commit()
            except IntegrityError:
                session.rollback()


class Session(Base):
    __tablename__ = 'sessions'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    session_token = Column(String, unique=True, nullable=False)
    expiers_at = Column(DateTime)

    user = relationship("User", back_populates="session")

    @classmethod
    def get_user(cls, session_token):
        with db_Session() as session:
            current_session = session.query(Session).filter(
                Session.session_token == session_token,
                Session.expiers_at > datetime.now()).first()
            if current_session is None:
                return None
            return current_session.user


def db_login(email, password):
    with db_Session() as session:
        user = session.query(User).filter_by(email=email).first()
        if user is None:
            return {"error": "User not found"}, 404

        if not checkpw(password.encode(), user.password):
            return {"error": "Invalid password"}, 401

        session_token = str(uuid.uuid4())
        current_time = datetime.now()
        if user.session:           
            user.session.expiers_at = current_time+timedelta(minutes=2)
            user.session.session_token = session_token
            
        else:
            new_session = Session(
                user_id=user.id,
                session_token=session_token,
                expiers_at = current_time+timedelta(minutes=2))
            session.add(new_session)
        
        user.last_login = current_time
       

        try:
            session.commit()
        except IntegrityError:
            session.rollback()
            return {"error": "error in serverside"}, 500

        return {"session_token": session_token, "expires_at": user.session.expiers_at}, None


if __name__ == "__main__":
    Base.metadata.create_all(engine)
