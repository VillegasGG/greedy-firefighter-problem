import ctypes

clibrary = ctypes.CDLL("./clibrary.so")
# clibrary.display(b"Get", 18)

# func = clibrary.display

# func.argtypes = [ctypes.c_char_p, ctypes.c_int]
# func.restype = ctypes.c_char_p

# string = ctypes.c_char_p(b"Get")
# print(string)

# string.value = b"Hello"
# print(string)

# func(string, 18)

#Other example

# alloc_func = clibrary.alloc_memory
# alloc_func.restype = ctypes.POINTER(ctypes.c_char_p)

# free_func = clibrary.free_memory
# free_func.argtypes = [ctypes.POINTER(ctypes.c_char_p)]

# cstring_pointer = alloc_func()
# cstring = ctypes.c_char_p.from_buffer(cstring_pointer)
# print(cstring.value)

# free_func(cstring_pointer)

# num = ctypes.c_int(100)
# num2 = ctypes.c_int(200)


# ptr = ctypes.pointer(num)
# print(ptr.contents)

# ptr2 = ctypes.POINTER(ctypes.c_int)     # this is faster
# ptr2.contents = num
# print(ptr2.contents)

# ptr2.contents = num2
# print(ptr2.contents)

values = (ctypes.c_int * 10)()

for i in range(len(values)):
    values[i] = i

# for i in range(len(values)):
#     print(values[i])

# sum = clibrary.sumArray(values, len(values))    
# print("Sum: ", sum)

# for i in range(len(values)):
#     print(values[i])

clibrary.getArray.restype = ctypes.POINTER(ctypes.c_int)
array_result = clibrary.getArray()    
# print(array_result.contents)

for i in range(10):
    print(array_result[i])

# do something with the array and free memory
clibrary.free_memory(array_result)