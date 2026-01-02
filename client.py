import socket
import base64
from des import des_process

def client():
    shared_key = "133457799BBCDFF1"
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(('localhost', 12345))
    print("=============================================")
    print("             CLIENT (DEVICE 1)               ")
    print("=============================================")
    
    while True:
        user_input = input("\nMasukkan pesan untuk dikirim: ")
        original_text = user_input.ljust(8)[:8]
        original_hex = original_text.encode('utf-8').hex()
        
        print(f"Pesan diproses: '{original_text}'")
        print(f"Pesan dalam format HEX: {original_hex}")

        cipher_hex = des_process(original_hex, shared_key, 'encrypt')
        cipher_bytes = bytes.fromhex(cipher_hex)
        base64_encoded = base64.b64encode(cipher_bytes).decode('utf-8')
        
        print(f"\n--- HASIL ENKRIPSI ---")
        print(f"Ciphertext (HEX)    : {cipher_hex}")
        print(f"Ciphertext (Base64) : {base64_encoded}")
        print("-" * 22)
        
        s.send(cipher_hex.encode('utf-8'))
        print("Ciphertext terkirim otomatis...")

        reply_data = s.recv(1024).decode('utf-8')
        print(f"\n[NOTIFIKASI] Balasan masuk (HEX): {reply_data}")
        
        cipher_reply_input = input("Masukkan Ciphertext (HEX) balasan untuk dekripsi: ")
        
        if cipher_reply_input.upper() == reply_data.upper():
            dec_hex = des_process(cipher_reply_input, shared_key, 'decrypt')
            try:
                dec_text = bytes.fromhex(dec_hex).decode('utf-8').strip()
                print(f"\n--- HASIL DEKRIPSI BALASAN ---")
                print(f"Pesan Balasan Asli : '{dec_text}'")
                print(f"Hexadecimal Balasan: {dec_hex}")
                print("-" * 30)
            except:
                print(f"Pesan Balasan (HEX): {dec_hex}")
        else:
            print("Error: HEX balasan tidak sesuai!")

    s.close()

if __name__ == "__main__": client()
