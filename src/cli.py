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
from src.algorithms import remove_duplicates, max_sum_subarray, is_palindrome, merge_sorted, chunked, flatten
from src.storage import to_csv, to_json, read_csv


def main() -> None:
    print("=" * 50)
    print("   SISTEMA DE PROCESSAMENTO v3")
    print("=" * 50)
    print(" 1. Decifrar Mensagem (Google Docs)")
    print(" 2. Criar Escada (Staircase)")
    print(" 3. Gerar Senha Segura")
    print(" 4. Validar CPF")
    print(" 5. Cifra de Cesar")
    print(" 6. Conversor de Bases")
    print(" 7. Analisar Texto")
    print("--- Avancado ---")
    print(" 8. Algoritmos de Listas")
    print(" 9. Manipular Arquivos (CSV/JSON)")
    print(" 0. Sair")

    choice = input("\nEscolha: ")

    if choice == "1":
        url = input("URL (Enter = padrao): ").strip() or DEFAULT_URL
        print()
        result = decipher_secret_message(url)
        print(result or "Nada encontrado.")

    elif choice == "2":
        entrada = input("Numeros: ")
        try:
            nums = [int(x) for x in entrada.split()]
            r = create_staircase(nums)
            if r:
                for row in r:
                    print(row)
            else:
                print("Invalido.")
        except ValueError:
            print("Erro.")

    elif choice == "3":
        try:
            length = int(input("Tamanho (16): ") or "16")
            senha = gerar_senha(length)
            print(f"Senha: {senha}")
        except ValueError:
            print("Erro.")

    elif choice == "4":
        cpf = input("CPF: ")
        print("Valido!" if validar_cpf(cpf) else "Invalido.")

    elif choice == "5":
        texto = input("Texto: ")
        try:
            shift = int(input("Deslocamento: "))
        except ValueError:
            print("Erro.")
            return
        op = input("Cifrar ou Decifrar? (c/d): ").lower()
        print(cifra_cesar(texto, shift, op == "d"))

    elif choice == "6":
        value = input("Valor: ")
        try:
            fb = int(input("Base origem (2/8/10/16): "))
            tb = int(input("Base destino (2/8/10/16): "))
            print(converter_base(value, fb, tb))
        except (ValueError, IndexError):
            print("Valor invalido para a base.")

    elif choice == "7":
        print("Texto (Enter duas vezes para finalizar):")
        lines = []
        while True:
            line = input()
            if not line:
                break
            lines.append(line)
        texto = "\n".join(lines)
        if not texto.strip():
            return
        r = analisar_frequencia(texto)
        print(f"Palavras: {r['total_palavras']}, Unicas: {r['palavras_unicas']}")
        for p, c in r["palavras_topo"]:
            print(f"  {p}: {c}x")

    elif choice == "8":
        print("--- Algoritmos de Listas ---")
        print("1. Remover duplicatas")
        print("2. Max sum subarray (janela deslizante)")
        print("3. Verificar palindromo")
        print("4. Mesclar arrays ordenados")
        print("5. Dividir em chunks")
        print("6. Achatar lista aninhada")
        opt = input("\nEscolha: ")

        if opt == "1":
            nums = [int(x) for x in input("Numeros: ").split()]
            k = remove_duplicates(nums)
            print(f"Resultado: {nums[:k]} ({k} elementos)")
        elif opt == "2":
            nums = [int(x) for x in input("Numeros: ").split()]
            k = int(input("Tamanho da janela: "))
            r = max_sum_subarray(nums, k)
            print(f"Soma maxima: {r}")
        elif opt == "3":
            s = input("Texto: ")
            print("Palindromo!" if is_palindrome(s) else "Nao e palindromo.")
        elif opt == "4":
            a = [int(x) for x in input("Array A: ").split()]
            b = [int(x) for x in input("Array B: ").split()]
            print(f"Mesclado: {merge_sorted(a, b)}")
        elif opt == "5":
            nums = [int(x) for x in input("Numeros: ").split()]
            size = int(input("Tamanho do chunk: "))
            print(list(chunked(nums, size)))
        elif opt == "6":
            print("Exemplo: [1, [2, [3, 4]], 5]")
            nested = [[1, [2, [3, 4]], 5]]
            print(f"Achatado: {flatten(nested)}")

    elif choice == "9":
        print("--- Manipular Arquivos ---")
        print("1. Criar CSV")
        print("2. Criar JSON")
        print("3. Ler CSV")
        opt = input("\nEscolha: ")
        if opt in ("1", "2"):
            dados = []
            print("Digite nome,valor (linha em branco para finalizar):")
            while True:
                linha = input()
                if not linha:
                    break
                nome, valor = linha.split(",")
                dados.append({"nome": nome.strip(), "valor": valor.strip()})
            if opt == "1":
                path = to_csv(dados)
                print(f"CSV salvo: {path}")
            else:
                path = to_json(dados)
                print(f"JSON salvo: {path}")
        elif opt == "3":
            path = input("Caminho do CSV: ")
            dados = read_csv(path)
            for row in dados:
                print(row)

    elif choice == "0":
        sys.exit(0)


if __name__ == "__main__":
    while True:
        main()
        input("\nEnter para continuar...")
