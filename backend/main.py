from fastapi import FastAPI, Depends, HTTPException, status, Path
from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship, Session
import datetime
from pydantic import BaseModel
from passlib.context import CryptContext
from jose import JWTError, jwt
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from typing import List, Optional

app = FastAPI()

# 数据库配置
DATABASE_URL = "mysql+pymysql://checkdoc_user:123456@127.0.0.1:3306/checkdoc"
engine = create_engine(DATABASE_URL, echo=True, future=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# 用户模型
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(64), unique=True, index=True, nullable=False)
    hashed_password = Column(String(128), nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    knowledge_bases = relationship("KnowledgeBase", back_populates="owner")

# 知识库模型
class KnowledgeBase(Base):
    __tablename__ = "knowledge_bases"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(128), nullable=False)
    description = Column(String(256))
    owner_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    owner = relationship("User", back_populates="knowledge_bases")

# 创建表
Base.metadata.create_all(bind=engine)

SECRET_KEY = "your_secret_key_here"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/login")

# Pydantic模型
class UserCreate(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class KnowledgeBaseCreate(BaseModel):
    name: str
    description: Optional[str] = None

class KnowledgeBaseOut(BaseModel):
    id: int
    name: str
    description: Optional[str]
    owner_id: int
    created_at: datetime.datetime
    class Config:
        orm_mode = True

# 数据库依赖

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_password_hash(password):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict):
    to_encode = data.copy()
    import datetime
    expire = datetime.datetime.utcnow() + datetime.timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=401,
        detail="无法验证凭据",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = db.query(User).filter(User.username == username).first()
    if user is None:
        raise credentials_exception
    return user

@app.get("/ping")
def ping():
    return {"message": "pong"}

# 注册接口
@app.post("/api/register", response_model=Token)
def register(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.username == user.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="用户名已存在")
    hashed_password = get_password_hash(user.password)
    new_user = User(username=user.username, hashed_password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    access_token = create_access_token(data={"sub": new_user.username})
    return {"access_token": access_token, "token_type": "bearer"}

# 登录接口
@app.post("/api/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="用户名或密码错误")
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}

# 创建知识库
@app.post("/api/knowledge_bases", response_model=KnowledgeBaseOut)
def create_knowledge_base(kb: KnowledgeBaseCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    new_kb = KnowledgeBase(name=kb.name, description=kb.description, owner_id=current_user.id)
    db.add(new_kb)
    db.commit()
    db.refresh(new_kb)
    return new_kb

# 获取知识库列表
@app.get("/api/knowledge_bases", response_model=List[KnowledgeBaseOut])
def list_knowledge_bases(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return db.query(KnowledgeBase).filter(KnowledgeBase.owner_id == current_user.id).all()

# 获取单个知识库详情
@app.get("/api/knowledge_bases/{kb_id}", response_model=KnowledgeBaseOut)
def get_knowledge_base(kb_id: int = Path(...), db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    kb = db.query(KnowledgeBase).filter(KnowledgeBase.id == kb_id, KnowledgeBase.owner_id == current_user.id).first()
    if not kb:
        raise HTTPException(status_code=404, detail="知识库不存在")
    return kb

# 更新知识库
@app.put("/api/knowledge_bases/{kb_id}", response_model=KnowledgeBaseOut)
def update_knowledge_base(kb_id: int, kb: KnowledgeBaseCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_kb = db.query(KnowledgeBase).filter(KnowledgeBase.id == kb_id, KnowledgeBase.owner_id == current_user.id).first()
    if not db_kb:
        raise HTTPException(status_code=404, detail="知识库不存在")
    db_kb.name = kb.name
    db_kb.description = kb.description
    db.commit()
    db.refresh(db_kb)
    return db_kb

# 删除知识库
@app.delete("/api/knowledge_bases/{kb_id}")
def delete_knowledge_base(kb_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_kb = db.query(KnowledgeBase).filter(KnowledgeBase.id == kb_id, KnowledgeBase.owner_id == current_user.id).first()
    if not db_kb:
        raise HTTPException(status_code=404, detail="知识库不存在")
    db.delete(db_kb)
    db.commit()
    return {"msg": "删除成功"} 