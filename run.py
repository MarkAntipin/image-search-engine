import uvicorn

from app.app import create_app

app = create_app()

if __name__ == '__main__':
    uvicorn.run(app=app)
