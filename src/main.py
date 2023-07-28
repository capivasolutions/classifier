import __main__
import uvicorn
import numpy as np
from joblib import load
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from config import Logger, Environment
from transaction import Transaction, TransactionClassificationMapper

app = FastAPI(
    title="Classifier service",
    description="Classify transactions as FRAUDULENT or GENUINE",
    version="1.0.0",
    contact=None,
    license_info=None,
    terms_of_service=None,
)
app.add_middleware(CORSMiddleware, allow_origins=["*"])

logger = Logger.get_instance()


@app.on_event("startup")
async def startup_event():
    """
    Initialize FastAPI and Sckit-learn model
    """
    logger.debug('Loading AI Classifier model')
    model = load(Environment.CLASSIFIER_MODEL_PATH)
    
    app.package = {"model": model}
    logger.debug('AI Classifier model loaded')


@app.post("/")
async def create_transaction(transaction: Transaction):
    logger.debug(f'Classifying transaction {transaction}')

    # Get the AI model from the context
    model = app.package['model']

    # Select only the relevant attributes
    data = np.asarray([[
        transaction.v3,
        transaction.v4,
        transaction.v5,
        transaction.v7,
        transaction.v9,
        transaction.v10,
        transaction.v11,
        transaction.v12,
        transaction.v14,
        transaction.v16,
        transaction.v17,
        transaction.v19,
        transaction.amount
    ]])

    # Classifying the entry
    classification = model.predict(data)

    # Finally extracting the predicted class
    classification = classification[0]

    # Parse result to enum value
    classification_enum = TransactionClassificationMapper.to_model(
        classification)

    logger.debug(f'{transaction} classified as {classification_enum}')

    return {"classification": classification_enum}


if __name__ == '__main__':
    uvicorn.run("main:app", host=Environment.CLASSIFIER_HOST, port=Environment.CLASSIFIER_PORT, reload=True)
