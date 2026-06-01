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
        
        # Procurar por dados estruturados no conteúdo
        # Tentar encontrar JSON ou outros formatos estruturados
        json_patterns = [
            r'\{[^{}]*\}',
            r'\[[^\[\]]*\]',
        ]
        
        structured_data = None
        for pattern in json_patterns:
            matches = re.findall(pattern, content)
            for match in matches:
                try:
                    data = json.loads(match)
                    if isinstance(data, (list, dict)):
                        structured_data = data
                        break
                except:
                    continue
            if structured_data:
                break
        
        # Se não encontrar dados estruturados, procurar por padrões de texto
        if not structured_data:
            # Extrair todo o texto visível
            text_pattern = r'>([^<]+)<'
            text_matches = re.findall(text_pattern, content)
            full_text = ' '.join(text_matches)
            
            # Procurar por padrões de coordenadas no texto
            # O formato parece ser: número caractere número
            patterns = [
                r'(\d+)([░█])(\d+)',
                r'(\d+)\s+([░█])\s+(\d+)',
                r'(\d+),\s*([░█]),\s*(\d+)',
                r'x-coordinate\s+(\d+)\s+Character\s+([░█])\s+y-coordinate\s+(\d+)',
            ]
            
            matches = []
            for pattern in patterns:
                matches = re.findall(pattern, full_text)
                if matches:
                    break
            
            if not matches:
                # Tentar extrair do conteúdo bruto
                print("Tentando extrair do conteúdo bruto...")
                
                # Procurar por sequências que pareçam coordenadas
                brute_pattern = r'(\d{1,3})([░█])(\d{1,3})'
                matches = re.findall(brute_pattern, content)
        
        if not matches:
            print("Nenhum dado de coordenada encontrado no documento")
            print("Tentando mostrar trechos do conteúdo...")
            
            # Mostrar alguns trechos do conteúdo para debug
            content_samples = [
                content[i:i+500] for i in range(0, min(len(content), 2000), 500)
            ]
            for i, sample in enumerate(content_samples):
                print(f"Trecho {i+1}:")
                print(sample)
                print("-" * 50)
            return
        
        print(f"Encontrados {len(matches)} pares de coordenadas-caracteres")
        
        # Armazenar caracteres em dicionário e calcular limites da grade
        char_dict = {}
        max_x = 0
        max_y = 0
        
        for match in matches:
            if len(match) == 3:
                x_str, char, y_str = match
                x = int(x_str)
                y = int(y_str)
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
