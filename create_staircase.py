def create_staircase(nums):
    step = 1
    subsets = []
    
    while nums:
        if len(nums) >= step:
            subset = nums[:step]
            subsets.append(subset)
            nums = nums[step:]
            step += 1
        else:
            return False
            
    return subsets

# Exemplos de uso
if __name__ == "__main__":
    # Teste 1: Exemplo válido
    nums1 = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    result1 = create_staircase(nums1.copy())
    print(f"Entrada: {nums1}")
    print(f"Resultado: {result1}")
    print()
    
    # Teste 2: Outro exemplo válido
    nums2 = [1, 2, 3, 4, 5, 6]
    result2 = create_staircase(nums2.copy())
    print(f"Entrada: {nums2}")
    print(f"Resultado: {result2}")
    print()
    
    # Teste 3: Exemplo inválido
    nums3 = [1, 2, 3, 4, 5]
    result3 = create_staircase(nums3.copy())
    print(f"Entrada: {nums3}")
    print(f"Resultado: {result3}")
    print()
    
    # Teste 4: Lista vazia
    nums4 = []
    result4 = create_staircase(nums4.copy())
    print(f"Entrada: {nums4}")
    print(f"Resultado: {result4}")
