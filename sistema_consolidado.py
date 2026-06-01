import requests
import re
import sys

def create_staircase(nums):
    """
    Cria uma estrutura de escada a partir de uma lista de números.
    """
    step = 1
    subsets = []
    
    nums_copy = list(nums)
    while nums_copy:
        if len(nums_copy) >= step:
            subset = nums_copy[:step]
            subsets.append(subset)
            nums_copy = nums_copy[step:]
            step += 1
        else:
            return False
            
    return subsets

def decipher_secret_message(doc_url):
    """
    Decifra mensagem secreta de um documento Google Docs publicado.
    """
    try:
        response = requests.get(doc_url)
        response.raise_for_status()
        content = response.text
        
        # Padrão para extrair X, Char e Y das tabelas do Google Docs
        pattern = r'<td[^>]*><p[^>]*><span[^>]*>(\d+)</span></p></td><td[^>]*><p[^>]*><span[^>]*>([^<])</span></p></td><td[^>]*><p[^>]*><span[^>]*>(\d+)</span></p></td>'
        matches = re.findall(pattern, content)
        
        if not matches:
            # Tentar um padrão alternativo caso o caractere seja especial ou a estrutura mude levemente
            pattern_alt = r'(\d+).*?([░█]).*?(\d+)'
            matches = re.findall(pattern_alt, content)
            
        if not matches:
            return "Nenhum dado de coordenada encontrado no documento."
        
        char_dict = {}
        max_x = 0
        max_y = 0
        
        for x_str, char, y_str in matches:
            x = int(x_str)
            y = int(y_str)
            char_dict[(x, y)] = char
            max_x = max(max_x, x)
            max_y = max(max_y, y)
        
        output = []
        for y in range(max_y, -1, -1):
            row = ""
            for x in range(max_x + 1):
                row += char_dict.get((x, y), " ")
            output.append(row)
            
        return "\n".join(output)
            
    except Exception as e:
        return f"Erro ao processar: {e}"

def main():
    print("="*30)
    print("SISTEMA DE PROCESSAMENTO")
    print("="*30)
    print("1. Decifrar Mensagem (Google Docs)")
    print("2. Criar Escada (Staircase)")
    print("3. Sair")
    
    choice = input("\nEscolha uma opção: ")
    
    if choice == '1':
        url = input("Digite a URL do Google Docs (ou Enter para usar a padrão): ")
        if not url:
            url = "https://docs.google.com/document/d/e/2PACX-1vSvM5gDlNvt7npYHhp_XfsJvuntUhq184By5xO_pA4b_gCWeXb6dM6ZxwN8rE6S4ghUsCj2VKR21oEP/pub"
        print("\nProcessando...\n")
        print(decipher_secret_message(url))
        
    elif choice == '2':
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
            
    elif choice == '3':
        print("Saindo...")
        sys.exit()
    else:
        print("Opção inválida.")

if __name__ == "__main__":
    while True:
        main()
        input("\nPressione Enter para continuar...")
