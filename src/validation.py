from datetime import date, datetime
from typing import Any, Optional

from pydantic import BaseModel, field_validator, EmailStr


class Endereco(BaseModel):
    rua: str
    numero: str
    bairro: str
    cidade: str
    uf: str
    cep: str

    @field_validator("uf")
    @classmethod
    def uf_must_be_valid(cls, v: str) -> str:
        ufs = {
            "AC", "AL", "AP", "AM", "BA", "CE", "DF", "ES", "GO",
            "MA", "MT", "MS", "MG", "PA", "PB", "PR", "PE", "PI",
            "RJ", "RN", "RS", "RO", "RR", "SC", "SP", "SE", "TO",
        }
        if v.upper() not in ufs:
            raise ValueError(f"UF invalida: {v}")
        return v.upper()


class Funcionario(BaseModel):
    nome: str
    email: EmailStr
    cpf: str
    data_nascimento: date
    salario: float
    endereco: Endereco
    departamento: str = "TI"
    ativo: bool = True
    data_admissao: Optional[datetime] = None

    @field_validator("cpf")
    @classmethod
    def validate_cpf(cls, v: str) -> str:
        digits = "".join(c for c in v if c.isdigit())
        if len(digits) != 11:
            raise ValueError("CPF deve ter 11 digitos")
        if digits == digits[0] * 11:
            raise ValueError("CPF com todos digitos iguais")
        return v

    @field_validator("salario")
    @classmethod
    def validate_salario(cls, v: float) -> float:
        if v <= 0:
            raise ValueError("Salario deve ser positivo")
        return v


class Produto(BaseModel):
    nome: str
    preco: float
    quantidade: int
    categoria: str
    tags: list[str] = []

    @field_validator("quantidade")
    @classmethod
    def validate_quantidade(cls, v: int) -> int:
        if v < 0:
            raise ValueError("Quantidade nao pode ser negativa")
        return v


def validate_pydantic(model: type[BaseModel], data: dict[str, Any]) -> dict[str, Any]:
    try:
        instance = model(**data)
        return {"valido": True, "dados": instance.model_dump()}
    except Exception as e:
        return {"valido": False, "erros": str(e)}


def validate_dataframe_schema(df: Any, schema_type: str = "funcionarios") -> dict[str, Any]:
    """Valida DataFrame com Pandera. Retorna dict com resultado."""
    try:
        import pandas as pd
        import pandera as pa
    except ImportError:
        return {"valido": False, "erro": "pandas/pandera nao instalados"}

    if not isinstance(df, pd.DataFrame):
        return {"valido": False, "erro": "Entrada nao e um DataFrame"}

    schemas = {
        "funcionarios": pa.DataFrameSchema(
            columns={
                "nome": pa.Column(str, nullable=False),
                "idade": pa.Column(int, pa.Check.in_range(18, 120)),
                "salario": pa.Column(float, pa.Check.greater_than(0)),
                "departamento": pa.Column(str),
                "ativo": pa.Column(bool),
            }
        ),
        "produtos": pa.DataFrameSchema(
            columns={
                "nome": pa.Column(str),
                "preco": pa.Column(float, pa.Check.greater_than(0)),
                "quantidade": pa.Column(int, pa.Check.greater_than_or_equal_to(0)),
                "categoria": pa.Column(str),
            }
        ),
    }

    schema = schemas.get(schema_type)
    if not schema:
        return {"valido": False, "erro": f"Schema '{schema_type}' nao encontrado"}

    try:
        schema.validate(df, lazy=True)
        return {"valido": True, "linhas": len(df)}
    except pa.errors.SchemaErrors as e:
        return {"valido": False, "erros": str(e)[:500]}
