import requests
import re
from bs4 import BeautifulSoup

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
        
        # Usar BeautifulSoup para parsear HTML
        soup = BeautifulSoup(content, 'html.parser')
        
        # Extrair todo o texto do documento
        text_content = soup.get_text()
        
        # Procurar por padrões de coordenadas no texto
        # Tentar diferentes padrões regex
        patterns = [
            r'\((\d+),(\d+)\)\s*:\s*(.)',
            r'(\d+),(\d+)\s*:\s*(.)',
            r'\((\d+),(\d+)\)\s+(.)',
            r'(\d+),(\d+)\s+(.)'
        ]
        
        matches = []
        for pattern in patterns:
            matches = re.findall(pattern, text_content)
            if matches:
                break
        
        if not matches:
            # Se não encontrar padrões específicos, procurar por coordenadas e caracteres separadamente
            print("Procurando por padrões alternativos...")
            
            # Procurar por todos os pares de coordenadas
            coord_pattern = r'\((\d+),(\d+)\)'
            coords = re.findall(coord_pattern, text_content)
            
            # Procurar por caracteres especiais que possuem sido usados
            char_pattern = r'[^\w\s\(\)\d,]'  # Caracteres que não são alfanuméricos, espaços, parênteses, dígitos ou vírgulas
            chars = re.findall(char_pattern, text_content)
            
            print(f"Coordenadas encontradas: {len(coords)}")
            print(f"Caracteres especiais encontrados: {len(chars)}")
            
            if coords and chars:
                # Tentar combinar coordenadas com caracteres
                min_len = min(len(coords), len(chars))
                matches = [(coords[i][0], coords[i][1], chars[i]) for i in range(min_len)]
        
        if not matches:
            print("Nenhum dado de coordenada encontrado no documento")
            print("Primeiros 500 caracteres do conteúdo:")
            print(text_content[:500])
            return
        
        print(f"Encontrados {len(matches)} pares de coordenadas-caracteres")
        
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
        
        print(f"Limites da grade: X=0..{max_x}, Y=0..{max_y}")
        
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
