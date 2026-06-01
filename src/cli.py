import sys
from src.decipher import decipher_secret_message, DEFAULT_URL
from src.staircase import create_staircase
from src.tools import (
    gerar_senha,
    validar_cpf,
    cifra_cesar,
    converter_base,
    analisar_frequencia,
)


def main() -> None:
    print("=" * 40)
    print("   SISTEMA DE PROCESSAMENTO v2")
    print("=" * 40)
    print("1. Decifrar Mensagem (Google Docs)")
    print("2. Criar Escada (Staircase)")
    print("3. Gerar Senha Segura")
    print("4. Validar CPF")
    print("5. Cifra de Cesar")
    print("6. Conversor de Bases Numericas")
    print("7. Analisar Frequencia de Texto")
    print("0. Sair")

    choice = input("\nEscolha uma opcao: ")

    if choice == "1":
        url = input("URL do Google Docs (Enter = padrao): ").strip()
        if not url:
            url = DEFAULT_URL
        print("\nProcessando...\n")
        result = decipher_secret_message(url)
        if result:
            print(result)
        else:
            print("Nenhuma mensagem encontrada ou erro ao processar.")

    elif choice == "2":
        entrada = input("Numeros separados por espaco: ")
        try:
            nums = [int(x) for x in entrada.split()]
            resultado = create_staircase(nums)
            if resultado:
                print("\nEscada gerada:")
                for r in resultado:
                    print(r)
            else:
                print("\nNao e possivel criar uma escada perfeita.")
        except ValueError:
            print("\nErro: Digite apenas numeros inteiros.")

    elif choice == "3":
        try:
            length = int(input("Tamanho da senha (Enter = 16): ") or "16")
            upper = input("Incluir maiusculas? (s/n): ").lower() == "s"
            lower = input("Incluir minusculas? (s/n): ").lower() == "s"
            digits = input("Incluir numeros? (s/n): ").lower() == "s"
            sym = input("Incluir simbolos? (s/n): ").lower() == "s"
            if not any([upper, lower, digits, sym]):
                print("\nSelecione ao menos um tipo de caractere.")
                return
            senha = gerar_senha(length, upper, lower, digits, sym)
            print(f"\nSenha gerada: {senha}")
        except ValueError:
            print("\nErro: Tamanho invalido.")

    elif choice == "4":
        cpf = input("Digite o CPF: ")
        if validar_cpf(cpf):
            print("\nCPF valido!")
        else:
            print("\nCPF invalido.")

    elif choice == "5":
        texto = input("Texto: ")
        try:
            shift = int(input("Deslocamento: "))
        except ValueError:
            print("\nErro: Deslocamento invalido.")
            return
        op = input("Cifrar ou Decifrar? (c/d): ").lower()
        decrypt = op == "d"
        resultado = cifra_cesar(texto, shift, decrypt)
        print(f"\nResultado: {resultado}")

    elif choice == "6":
        value = input("Valor: ")
        try:
            from_b = int(input("Base de origem (2, 8, 10, 16): "))
            to_b = int(input("Base de destino (2, 8, 10, 16): "))
        except ValueError:
            print("\nErro: Base invalida.")
            return
        try:
            resultado = converter_base(value, from_b, to_b)
            print(f"\nResultado: {resultado}")
        except (ValueError, IndexError):
            print("\nErro: Valor invalido para a base informada.")

    elif choice == "7":
        print("Digite o texto (linha em branco para finalizar):")
        lines: list[str] = []
        while True:
            line = input()
            if not line:
                break
            lines.append(line)
        texto = "\n".join(lines)
        if not texto.strip():
            print("\nTexto vazio.")
            return
        result = analisar_frequencia(texto)
        print(f"\nTotal de palavras: {result['total_palavras']}")
        print(f"Palavras unicas: {result['palavras_unicas']}")
        print(f"Total de frases: {result['total_frases']}")
        print(f"Total de caracteres: {result['total_caracteres']}")
        print("\nPalavras mais frequentes:")
        for palavra, count in result["palavras_topo"]:
            print(f"  {palavra}: {count}x")
        print("\nCaracteres mais frequentes:")
        for char, count in result["caracteres_topo"]:
            print(f"  '{char}': {count}x")

    elif choice == "0":
        print("Saindo...")
        sys.exit(0)
    else:
        print("Opcao invalida.")


if __name__ == "__main__":
    while True:
        main()
        input("\nPressione Enter para continuar...")
