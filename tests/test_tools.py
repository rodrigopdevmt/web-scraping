from src.tools import (
    gerar_senha,
    validar_cpf,
    cifra_cesar,
    converter_base,
    analisar_frequencia,
)


class TestGerarSenha:
    def test_default_length(self) -> None:
        senha = gerar_senha()
        assert len(senha) == 16

    def test_custom_length(self) -> None:
        senha = gerar_senha(length=8)
        assert len(senha) == 8

    def test_only_lowercase(self) -> None:
        senha = gerar_senha(uppercase=False, digits=False, symbols=False)
        assert senha.islower()

    def test_only_digits(self) -> None:
        senha = gerar_senha(uppercase=False, lowercase=False, symbols=False)
        assert senha.isdigit()


class TestValidarCPF:
    def test_valid_cpf(self) -> None:
        assert validar_cpf("529.982.247-25") is True

    def test_valid_cpf_digits(self) -> None:
        assert validar_cpf("52998224725") is True

    def test_invalid_cpf(self) -> None:
        assert validar_cpf("111.111.111-11") is False

    def test_invalid_length(self) -> None:
        assert validar_cpf("123") is False

    def test_invalid_digits(self) -> None:
        assert validar_cpf("12345678901") is False


class TestCifraCesar:
    def test_encrypt(self) -> None:
        assert cifra_cesar("abc", 3) == "def"

    def test_decrypt(self) -> None:
        assert cifra_cesar("def", 3, decrypt=True) == "abc"

    def test_wrap_around(self) -> None:
        assert cifra_cesar("xyz", 3) == "abc"

    def test_preserves_case(self) -> None:
        assert cifra_cesar("AbC", 1) == "BcD"

    def test_preserves_spaces(self) -> None:
        assert cifra_cesar("a b", 1) == "b c"

    def test_preserves_non_alpha(self) -> None:
        assert cifra_cesar("a!b", 1) == "b!c"


class TestConverterBase:
    def test_dec_to_bin(self) -> None:
        assert converter_base("10", 10, 2) == "1010"

    def test_bin_to_dec(self) -> None:
        assert converter_base("1010", 2, 10) == "10"

    def test_dec_to_hex(self) -> None:
        assert converter_base("255", 10, 16) == "FF"

    def test_hex_to_dec(self) -> None:
        assert converter_base("FF", 16, 10) == "255"

    def test_zero(self) -> None:
        assert converter_base("0", 10, 2) == "0"

    def test_dec_to_oct(self) -> None:
        assert converter_base("8", 10, 8) == "10"


class TestAnalisarFrequencia:
    def test_basic_analysis(self) -> None:
        result = analisar_frequencia("ola mundo ola")
        assert result["total_palavras"] == 3
        assert result["palavras_unicas"] == 2

    def test_empty_text(self) -> None:
        result = analisar_frequencia("")
        assert result["total_palavras"] == 0

    def test_sentence_count(self) -> None:
        result = analisar_frequencia("Ola. Mundo. Teste.")
        assert result["total_frases"] == 3

    def test_top_words(self) -> None:
        result = analisar_frequencia("a a a b b c")
        top = result["palavras_topo"]
        assert top[0][0] == "a"
        assert top[0][1] == 3
