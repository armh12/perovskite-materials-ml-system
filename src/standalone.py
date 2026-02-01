from dotenv import load_dotenv
import uvicorn

from perovskite_prediction_api.app import app


load_dotenv()

def main():
    uvicorn.run(app, host="0.0.0.0", port=8080)


if __name__ == "__main__":
    main()