import socket
from des import des_process

def server():
    shared_key = "133457799BBCDFF1"
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('localhost', 12345))
    s.listen(1)
    print("=============================================")
    print("              SERVER (DEVICE 2)              ")
    print("=============================================")
    conn, addr = s.accept()
    
    while True:
        data = conn.recv(1024).decode('utf-8')
        if not data: break
        
        print(f"\n[NOTIFIKASI] Pesan masuk (HEX): {data}")
        cipher_input = input("Masukkan Ciphertext (HEX) untuk proses dekripsi: ")
        
        if cipher_input.upper() == data.upper():
            dec_hex = des_process(cipher_input, shared_key, 'decrypt')
            try:
                dec_text = bytes.fromhex(dec_hex).decode('utf-8').strip()
                print(f"\n--- HASIL DEKRIPSI ---")
                print(f"Pesan asli ditemukan: '{dec_text}'")
                print(f"Hexadecimal asli    : {dec_hex}")
                print("-" * 22)
            except:
                print(f"\nDecrypted (hex): {dec_hex}")
        else:
            print("Error: HEX tidak sesuai!")

        msg_reply = input("\nBalas pesan ke Client (8 char): ").ljust(8)[:8]
        reply_hex = msg_reply.encode('utf-8').hex()
        cipher_reply = des_process(reply_hex, shared_key, 'encrypt')
        conn.send(cipher_reply.encode('utf-8'))
        print(f"Balasan terkirim ke Client.")

    conn.close()

if __name__ == "__main__": server()
