import requests
import re
import json

def decipher_secret_message(doc_url):
    """
    Decifra mensagem secreta de um documento Google Docs publicado.
    
    Args:
        doc_url (str): URL do Google Docs publicado com dados da grade
        
    A função baixa o conteúdo do documento, extrai coordenadas e caracteres,
    constrói uma grade 2D e imprime a mensagem secreta formatada.
    """
    try:
        # Tentar diferentes abordagens para obter o conteúdo
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        response = requests.get(doc_url, headers=headers)
        response.raise_for_status()
        content = response.text
        
        # Procurar por padrões de coordenadas no conteúdo
        # O formato parece ser: número caractere número
        patterns = [
            r'(\d+)([░█])(\d+)',
            r'(\d+)\s+([░█])\s+(\d+)',
            r'(\d+),\s*([░█]),\s*(\d+)',
        ]
        
        matches = []
        for pattern in patterns:
            matches = re.findall(pattern, content)
            if matches:
                break
        
        if not matches:
            print("Nenhum dado de coordenada encontrado no documento")
            return
        
        print(f"Encontrados {len(matches)} pares de coordenadas-caracteres")
        
        # Filtrar apenas matches válidos (onde todos os grupos são números ou caracteres válidos)
        valid_matches = []
        for match in matches:
            if len(match) == 3:
                x_str, char, y_str = match
                try:
                    x = int(x_str)
                    y = int(y_str)
                    if char in ['░', '█']:  # Verificar se é um caractere válido
                        valid_matches.append((x, char, y))
                except ValueError:
                    continue
        
        print(f"Matches válidos: {len(valid_matches)}")
        
        if not valid_matches:
            print("Nenhum match válido encontrado")
            return
        
        # Armazenar caracteres em dicionário e calcular limites da grade
        char_dict = {}
        max_x = 0
        max_y = 0
        
        for x, char, y in valid_matches:
            char_dict[(x, y)] = char
            max_x = max(max_x, x)
            max_y = max(max_y, y)
        
        print(f"Limites da grade: X=0..{max_x}, Y=0..{max_y}")
        print(f"Total de caracteres: {len(char_dict)}")
        
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
