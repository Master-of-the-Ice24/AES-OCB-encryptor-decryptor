from kivy.lang import Builder
from kivy.app import App
from kivy.core.window import Window
from Crypto.Cipher import AES


class mainApp(App):
    def build(self):
        Window.maximize()
        return Builder.load_file('gui.kv')

    def encryptMsg(self):
        encryptionMessage = self.root.ids.encryptionMessage
        encryptionKey = self.root.ids.encryptionKey
        encryptedText = self.root.ids.encryptedText
        encryptionTag = self.root.ids.encryptionTag
        encryptionNonce = self.root.ids.encryptionNonce

        data = encryptionMessage.text.encode()
        aes_key = encryptionKey.text.encode()
        
        cipher = AES.new(aes_key, AES.MODE_OCB)
        ciphertext, tag = cipher.encrypt_and_digest(data)

        assert len(cipher.nonce) == 15
        
        encryptedText.text = ciphertext.hex()
        encryptionTag.text = tag.hex()
        encryptionNonce.text = cipher.nonce.hex()

    def decryptMsg(self):
        ciphertext = self.root.ids.decryptionMessage.text
        aes_key = self.root.ids.decryptionKey.text.encode()
        decryptedText = self.root.ids.decryptedText
        tag = self.root.ids.decryptionTag.text
        nonce = self.root.ids.decryptionNonce.text
        
        ciphertext = bytes.fromhex(ciphertext)
        tag = bytes.fromhex(tag)
        nonce = bytes.fromhex(nonce)

        assert len(nonce) == 15
        
        cipher = AES.new(aes_key, AES.MODE_OCB, nonce=nonce)
        plaintext = cipher.decrypt_and_verify(ciphertext, tag)

        decryptedText.text = plaintext.decode()



if __name__ == '__main__':
    mainApp().run()