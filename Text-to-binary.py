# encode_decode.py
"""Text <-> Binary <-> Hex converter (works with UTF-8)."""

def text_to_binary(s: str) -> str:
    # Convert each unicode codepoint to UTF-8 bytes, then to binary groups
    return ' '.join(format(b, '08b') for b in s.encode('utf-8'))

def text_to_hex(s: str) -> str:
    return ' '.join(format(b, '02x') for b in s.encode('utf-8'))

def binary_to_text(bstr: str) -> str:
    # Accepts space-separated 8-bit binary bytes
    bytes_list = [int(x, 2) for x in bstr.split()]
    return bytes(bytes_list).decode('utf-8', errors='replace')

def hex_to_text(hstr: str) -> str:
    parts = hstr.split()
    bytes_list = bytes(int(x, 16) for x in parts)
    return bytes_list.decode('utf-8', errors='replace')

def interactive():
    print("1) Text -> Binary/Hex")
    print("2) Binary -> Text")
    print("3) Hex -> Text")
    choice = input("Choose (1/2/3): ").strip()
    if choice == '1':
        s = input("Enter text: ")
        print("Binary:", text_to_binary(s))
        print("Hex   :", text_to_hex(s))
    elif choice == '2':
        b = input("Enter binary (space-separated bytes): ")
        print("Text:", binary_to_text(b))
    elif choice == '3':
        h = input("Enter hex (space-separated bytes): ")
        print("Text:", hex_to_text(h))
    else:
        print("Invalid choice")

if __name__ == "__main__":
    interactive()
