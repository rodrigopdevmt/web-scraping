import requests
import re

def decipher_secret_message(doc_url):
    """
    Decifra mensagem secreta de um documento Google Docs publicado.
    
    Args:
        doc_url (str): URL do Google Docs publicado com dados da grade
        
    A função baixa o conteúdo do documento, extrai coordenadas e caracteres,
    constrói uma grade 2D e imprime a mensagem secreta formatada.
    """
    try:
        # Baixar conteúdo do documento
        response = requests.get(doc_url)
        response.raise_for_status()
        content = response.text
        
        # Extrair dados de coordenadas e caracteres
        pattern = r'\((\d+),(\d+)\)\s*:\s*(.)'
        matches = re.findall(pattern, content)
        
        if not matches:
            print("Nenhum dado de coordenada encontrado no documento")
            return
        
        # Armazenar caracteres em dicionário e calcular limites da grade
        char_dict = {}
        max_x = 0
        max_y = 0
        
        for x_str, y_str, char in matches:
            x = int(x_str)
            y = int(y_str)
            char_dict[(x, y)] = char
            max_x = max(max_x, x)
            max_y = max(max_y, y)
        
        # Construir grade (invertendo eixo y para impressão correta)
        # Imprimir de cima para baixo (y máximo para 0)
        for y in range(max_y, -1, -1):
            row = ""
            for x in range(max_x + 1):
                if (x, y) in char_dict:
                    row += char_dict[(x, y)]
                else:
                    row += " "
            print(row)
            
    except requests.RequestException as e:
        print(f"Erro ao baixar documento: {e}")
    except Exception as e:
        print(f"Erro ao processar dados: {e}")

# Testar com URL fornecida
if __name__ == "__main__":
    url = "https://docs.google.com/document/d/e/2PACX-1vSvM5gDlNvt7npYHhp_XfsJvuntUhq184By5xO_pA4b_gCWeXb6dM6ZxwN8rE6S4ghUsCj2VKR21oEP/pub"
    decipher_secret_message(url)
