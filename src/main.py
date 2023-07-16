import __main__
import torch
import uvicorn
import numpy as np
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from mlp import MLP
from config import Logger, Environment
from transaction import Transaction, TransactionClassificationMapper
from torch.autograd import Variable


setattr(__main__, "MLP", MLP)

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
    Initialize FastAPI and PyTorch model
    """
    logger.debug('Loading AI Classifier model')
    model = torch.load(Environment.CLASSIFIER_MODEL_PATH,
                       map_location=torch.device('cpu'))
    model.eval()
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

    # Turning data into a Variable for pytorch
    entry = Variable(torch.from_numpy(data)).float()

    # Classifying the entry
    classification = model(entry)

    # Finally extracting the predicted class
    classification = classification.argmax().item()

    # Parse result to enum value
    classification_enum = TransactionClassificationMapper.to_model(
        classification)

    logger.debug(f'{transaction} classified as {classification_enum}')

    return {"classification": classification_enum}


if __name__ == '__main__':
    # server api
    uvicorn.run("main:app", host="0.0.0.0", port=4000, reload=True)
