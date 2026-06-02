from datetime import date
from src.validation import validate_pydantic, Funcionario, Endereco, Produto


class TestFuncionario:
    def test_valid(self):
        data = {
            "nome": "Joao Silva",
            "email": "joao@email.com",
            "cpf": "52998224725",
            "data_nascimento": "1990-05-10",
            "salario": 5000.0,
            "endereco": {
                "rua": "Rua A",
                "numero": "100",
                "bairro": "Centro",
                "cidade": "Cuiaba",
                "uf": "MT",
                "cep": "78000000",
            },
        }
        result = validate_pydantic(Funcionario, data)
        assert result["valido"] is True

    def test_invalid_cpf(self):
        data = {
            "nome": "Joao",
            "email": "joao@email.com",
            "cpf": "123",
            "data_nascimento": "1990-01-01",
            "salario": 5000.0,
            "endereco": {
                "rua": "Rua A",
                "numero": "1",
                "bairro": "Centro",
                "cidade": "Cuiaba",
                "uf": "MT",
                "cep": "78000000",
            },
        }
        result = validate_pydantic(Funcionario, data)
        assert result["valido"] is False

    def test_invalid_uf(self):
        data = {
            "nome": "Joao",
            "email": "joao@email.com",
            "cpf": "52998224725",
            "data_nascimento": "1990-01-01",
            "salario": 5000.0,
            "endereco": {
                "rua": "Rua A",
                "numero": "1",
                "bairro": "Centro",
                "cidade": "Cuiaba",
                "uf": "XX",
                "cep": "78000000",
            },
        }
        result = validate_pydantic(Funcionario, data)
        assert result["valido"] is False

    def test_negative_salary(self):
        data = {
            "nome": "Joao",
            "email": "joao@email.com",
            "cpf": "52998224725",
            "data_nascimento": "1990-01-01",
            "salario": -100,
            "endereco": {
                "rua": "Rua A",
                "numero": "1",
                "bairro": "Centro",
                "cidade": "Cuiaba",
                "uf": "MT",
                "cep": "78000000",
            },
        }
        result = validate_pydantic(Funcionario, data)
        assert result["valido"] is False


class TestProduto:
    def test_valid(self):
        data = {"nome": "Notebook", "preco": 3500.0, "quantidade": 10, "categoria": "Eletronicos"}
        result = validate_pydantic(Produto, data)
        assert result["valido"] is True

    def test_negative_quantity(self):
        data = {"nome": "Item", "preco": 10.0, "quantidade": -1, "categoria": "Teste"}
        result = validate_pydantic(Produto, data)
        assert result["valido"] is False
