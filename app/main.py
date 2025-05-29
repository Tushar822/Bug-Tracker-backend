# # from fastapi import FastAPI
# # from app.api.v1.auth import endpoints as auth_endpoints
# # from app.api.v1.user import endpoints as user_endpoints


# # from fastapi import FastAPI
# # from fastapi.middleware.cors import CORSMiddleware
# # from contextlib import asynccontextmanager
# # from app.api.v1.endpoints.projects import router as api_router
# # from app.api.v1.endpoints.auth import router as api_router
# # from app.api.v1.endpoints.issues import router as api_router

# # from app.core.config import settings
# # from app.db.database import create_db_and_tables

# # @asynccontextmanager
# # def lifespan(app: FastAPI):
# #     # Create tables on startup
# #     create_db_and_tables()
# #     yield

# # app = FastAPI(
# #     title="Project Management System",
# #     description="A role-based project management system built with SQLModel",
# #     version="1.0.0",
# #     lifespan=lifespan
# # )

# # # CORS middleware
# # app.add_middleware(
# #     CORSMiddleware,
# #     allow_origins=["*"],  # In production, specify allowed origins
# #     allow_credentials=True,
# #     allow_methods=["*"],
# #     allow_headers=["*"],
# # )

# # app.include_router(api_router, prefix="/api/v1")

# # @app.get("/")
# # def read_root():
# #     return {
# #         "message": "Project Management System API", 
# #         "version": "1.0.0",
# #         "docs": "/docs"
# #     }

# # if __name__ == "__main__":
# #     import uvicorn
# #     uvicorn.run(app, host="0.0.0.0", port=8000)


# import os
# from fastapi import FastAPI
# from fastapi.middleware.cors import CORSMiddleware

# from app.api.v1.endpoints.projects import router as projects_router
# from app.api.v1.endpoints.auth import router as auth_router
# from app.api.v1.endpoints.issues import router as issues_router

# from app.core.config import settings
# from app.db.database import create_db_and_tables

# app = FastAPI(
#     title="Project Management System",
#     description="A role-based project management system built with SQLModel",
#     version="1.0.0"
# )
# port = int(os.environ.get("PORT", 8000))
# # Create tables on startup (sync)
# @app.on_event("startup")
# def on_startup():
#     create_db_and_tables()

# # CORS middleware
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],  # In production, specify allowed origins
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# # Include routers
# app.include_router(projects_router, prefix="/api/v1/projects")
# app.include_router(auth_router, prefix="/api/v1/auth")
# app.include_router(issues_router, prefix="/api/v1/issues")

# @app.get("/")
# def read_root():
#     return {
#         "message": "Project Management System API", 
#         "version": "1.0.0",
#         "docs": "/docs"
#     }

# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="0.0.0.0", port=8000)


import os
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.endpoints.projects import router as projects_router
from app.api.v1.endpoints.auth import router as auth_router
from app.api.v1.endpoints.issues import router as issues_router

from app.core.config import settings
from app.db.database import create_db_and_tables

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Create tables on startup
    create_db_and_tables()
    yield
    # Cleanup on shutdown (if needed)

app = FastAPI(
    title="Project Management System",
    description="A role-based project management system built with SQLModel",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://bug-tracker-frontend-ochre.vercel.app","http://localhost:3000"],  # In production, specify allowed origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(projects_router, prefix="/api/v1/projects", tags=["projects"])
app.include_router(auth_router, prefix="/api/v1/auth", tags=["authentication"])
app.include_router(issues_router, prefix="/api/v1/issues", tags=["issues"])

@app.get("/", tags=["root"])
@app.head("/", tags=["root"])
def read_root():
    return {
        "message": "Project Management System API", 
        "version": "1.0.0",
        "docs": "/docs",
        "health": "OK"
    }

@app.get("/health", tags=["health"])
def health_check():
    return {"status": "healthy"}

print("ENV SETTINGS:", settings.dict())

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)

