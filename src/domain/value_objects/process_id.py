from pydantic import BaseModel, Field, field_validator
import uuid


class ProcessId(BaseModel):
    """Идентификатор процесса"""
    value: str = Field(..., min_length=1, description="Уникальный идентификатор процесса")
    
    model_config = {
        "frozen": True 
    }
    
    @field_validator('value')
    def validate_uuid_format(cls, v):
        """Проверяет, что значение является валидным UUID"""
        try:
            uuid.UUID(v)
        except ValueError:
            raise ValueError('ProcessId должен быть валидным UUID')
        return v
    
    @classmethod
    def generate(cls) -> 'ProcessId':
        """Генерирует новый уникальный идентификатор"""
        return cls(value=str(uuid.uuid4()))
    
    def __str__(self) -> str:
        return self.value
    
    def __hash__(self) -> int:
        return hash(self.value)