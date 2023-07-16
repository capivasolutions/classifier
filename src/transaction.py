from uuid import UUID
from enum import Enum
from typing import Union
from pydantic import BaseModel
from datetime import datetime


class TransactionClassification(str, Enum):
    FRAUDULENT = 'FRAUDULENT'
    GENUINE = 'GENUINE'


class TransactionClassificationMapper:
    @staticmethod
    def to_model(classification: int) -> TransactionClassification:
        if classification == 0:
            return TransactionClassification.GENUINE
        else:
            return TransactionClassification.FRAUDULENT


class Transaction(BaseModel):
    time: float
    v1: float
    v2: float
    v3: float
    v4: float
    v5: float
    v6: float
    v7: float
    v8: float
    v9: float
    v10: float
    v11: float
    v12: float
    v13: float
    v14: float
    v15: float
    v16: float
    v17: float
    v18: float
    v19: float
    v20: float
    v21: float
    v22: float
    v23: float
    v24: float
    v25: float
    v26: float
    v27: float
    v28: float
    amount: float

    def __str__(self):
        return f'Transaction [ time: {self.time}, amount: {self.amount} ]'
