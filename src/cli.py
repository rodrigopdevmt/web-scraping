import sys
from src.decipher import decipher_secret_message, DEFAULT_URL
from src.staircase import create_staircase


def main() -> None:
    print("=" * 30)
    print("SISTEMA DE PROCESSAMENTO")
    print("=" * 30)
    print("1. Decifrar Mensagem (Google Docs)")
    print("2. Criar Escada (Staircase)")
    print("3. Sair")

    choice = input("\nEscolha uma opção: ")

    if choice == "1":
        url = input("Digite a URL do Google Docs (ou Enter para usar a padrão): ").strip()
        if not url:
            url = DEFAULT_URL
        print("\nProcessando...\n")
        result = decipher_secret_message(url)
        if result:
            print(result)
        else:
            print("Nenhuma mensagem encontrada ou erro ao processar.")

    elif choice == "2":
        entrada = input("Digite os números separados por espaço: ")
        try:
            nums = [int(x) for x in entrada.split()]
            resultado = create_staircase(nums)
            if resultado:
                print("\nEscada gerada:")
                for r in resultado:
                    print(r)
            else:
                print("\nNão é possível criar uma escada perfeita com esses números.")
        except ValueError:
            print("\nErro: Por favor, digite apenas números inteiros.")

    elif choice == "3":
        print("Saindo...")
        sys.exit(0)
    else:
        print("Opção inválida.")


if __name__ == "__main__":
    while True:
        main()
        input("\nPressione Enter para continuar...")
