def Trans_Arr_To_Str(arr):   # 데이터 정제 (리스트 -> 문자열)
    if str(type(arr)) == "<class 'int'>":
        return_str = f'{arr}'
        return return_str
    elif str(type(arr)) != "<class 'list'>":
        return '0'
    return_str = ''
    for i in range(len(arr)):
        return_str = return_str + f'{arr[i]}'
        if i+1 != len(arr):
            return_str = return_str + ','
    return return_str
    
def Trans_Str_To_Arr(in_str):  # 데이터 정제 (문자열 -> 리스트) 
    if str(type(in_str)) != "<class 'str'>":                     
        return [0]
    arr_str = in_str.split(',')   
    return_list = []
    for i in arr_str:
        if not i.isdecimal():                
            return [0]
        return_list.append(int(i))
    return return_list
    

# arr = [1, 3, 5, 7, 9]
# arr_np = np.array(arr)
# err_test_int = 1
# err_test_str = 'test'

# if __name__ == '__main__':
#     print(Trans_Str_To_Arr('2,5'))