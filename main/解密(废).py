import base64
import ctypes
from ctypes import wintypes

# Specify the absolute path to advapi32.dll
advapi32_path = r'C:\Windows\System32\advapi32.dll'

try:
    # Load advapi32.dll using ctypes with absolute path
    advapi32 = ctypes.WinDLL(advapi32_path)

    # Define necessary Windows API functions and constants
    LocalFree = ctypes.windll.kernel32.LocalFree
    LocalFree.argtypes = [ctypes.c_void_p]
    LocalFree.restype = wintypes.BOOL

    # Define DATA_BLOB structure dynamically
    class DATA_BLOB(ctypes.Structure):
        _fields_ = [
            ('cbData', wintypes.DWORD),
            ('pbData', ctypes.POINTER(ctypes.c_char))
        ]

    # Check if CryptUnprotectData function is available
    if not hasattr(advapi32, 'CryptUnprotectData'):
        raise RuntimeError('CryptUnprotectData function not found in advapi32.dll')

    CryptUnprotectData = advapi32.CryptUnprotectData
    CryptUnprotectData.argtypes = [
        ctypes.POINTER(DATA_BLOB),
        ctypes.POINTER(ctypes.c_wchar),
        ctypes.POINTER(DATA_BLOB),
        ctypes.c_void_p,
        ctypes.c_void_p,
        wintypes.DWORD,
        ctypes.POINTER(DATA_BLOB)
    ]
    CryptUnprotectData.restype = wintypes.BOOL

    # Example encrypted data in base64 format
    encrypted_data_base64 = '=123'

    # Convert base64 encoded ciphertext to bytes
    ciphertext = base64.b64decode(encrypted_data_base64)

    # Prepare the input and output DATA_BLOB structures
    data_in = DATA_BLOB()
    data_in.cbData = len(ciphertext)
    data_in.pbData = ctypes.cast(ciphertext, ctypes.POINTER(ctypes.c_char))

    data_out = DATA_BLOB()

    # Call CryptUnprotectData
    if not CryptUnprotectData(ctypes.byref(data_in), None, None, None, None, 0, ctypes.byref(data_out)):
        raise ctypes.WinError()

    # Get the decrypted data from data_out
    decrypted_data = ctypes.string_at(data_out.pbData, data_out.cbData)

    # Free memory allocated by CryptUnprotectData
    if data_out.pbData:
        if not LocalFree(data_out.pbData):
            raise ctypes.WinError()

    print(f'Decrypted data: {decrypted_data.decode("utf-8")}')

except Exception as e:
    print(f'Error decrypting data: {str(e)}')
