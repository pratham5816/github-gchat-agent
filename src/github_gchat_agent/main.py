import uvicorn
from github_gchat_agent.config import settings

def main():
    print(f"Starting GitHub GChat Agent Server on {settings.HOST}:{settings.PORT} ...")
    uvicorn.run(
        "github_gchat_agent.server:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
    )

if __name__ == "__main__":
    main()
