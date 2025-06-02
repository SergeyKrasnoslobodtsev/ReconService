from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from enum import Enum


class ReconciliationActRequestModel(BaseModel):
    document: str

class ProcessIdResponse(BaseModel):
    process_id: str

class ProcessStatusEnum(Enum):
    WAIT = 0
    DONE = 1
    NOT_FOUND = -1
    ERROR = -2

class RowIdModel(BaseModel):
    id_table: int
    id_row: int

class ActEntryModel(BaseModel):
    row_id: RowIdModel
    record: str
    value: float
    date: Optional[str] = None

class PeriodModel(BaseModel):
    from_date: str = Field(alias="from")
    to_date: str = Field(alias="to")

    model_config = {
        "populate_by_name": True, # Замена allow_population_by_field_name
        "from_attributes": True    # Замена orm_mode
    }


class ReconciliationActResponseModel(BaseModel):
    process_id: str
    status: int
    message: str
    seller: str
    buyer: str
    period: PeriodModel
    debit: List[ActEntryModel]
    credit: List[ActEntryModel]

    model_config = {
        "from_attributes": True    # Замена orm_mode
    }



# Модель для запроса /process_status
class ProcessStatusRequest(BaseModel):
    process_id: str

class StatusResponseModel(BaseModel): # Общая модель для статусов WAIT, ERROR, NOT_FOUND
    status: int
    message: str

# Модель для внутреннего представления данных процесса
class InternalProcessDataModel(BaseModel):
    process_id: str
    status_enum: ProcessStatusEnum = ProcessStatusEnum.WAIT
    seller: Optional[str] = None
    buyer: Optional[str] = None
    buyer_org_data: Optional[Dict[str, Any]] = None # Добавлено поле для хранения информации о покупателе
    period: Optional[PeriodModel] = None
    debit_seller: List[ActEntryModel] = [] 
    credit_seller: List[ActEntryModel] = [] 
    debit_buyer: List[ActEntryModel] = []
    credit_buyer: List[ActEntryModel] = []
    error_message_detail: Optional[str] = None
    # Это структура документа Document из классы base_extractor.py уже хранит в себе данные PDF в виде байтов,
    # поэтому здесь можно использовать тип Any
    document_structure: Optional[Any] = None

    model_config = {
        "arbitrary_types_allowed": True
        # "from_attributes": True # Если нужно создавать из атрибутов объекта
    }
