from kivy.lang import Builder
from kivy.app import App
from kivy.core.window import Window
from Crypto.Cipher import AES


class mainApp(App):
    def build(self):
        Window.maximize()
        return Builder.load_file('gui.kv')

    def on_start(self):
        self.encryptionMessage = self.root.ids.encryptionMessage
        self.encryptionKey = self.root.ids.encryptionKey
        self.encryptedText = self.root.ids.encryptedText
        self.encryptionTag = self.root.ids.encryptionTag
        self.encryptionNonce = self.root.ids.encryptionNonce

        self.ciphertext = self.root.ids.decryptionMessage
        self.aes_key = self.root.ids.decryptionKey
        self.decryptedText = self.root.ids.decryptedText
        self.tag = self.root.ids.decryptionTag
        self.nonce = self.root.ids.decryptionNonce
    
    def encryptMsg(self):
        data = self.encryptionMessage.text.encode()
        aes_key = self.encryptionKey.text.encode()
        
        cipher = AES.new(aes_key, AES.MODE_OCB)
        ciphertext, tag = cipher.encrypt_and_digest(data)

        assert len(cipher.nonce) == 15
        
        self.encryptedText.text = ciphertext.hex()
        self.encryptionTag.text = tag.hex()
        self.encryptionNonce.text = cipher.nonce.hex()

    def decryptMsg(self):
        ciphertext = self.ciphertext.text
        aes_key = self.aes_key.text.encode()
        tag = self.tag.text
        nonce = self.nonce.text

        ciphertext = bytes.fromhex(ciphertext)
        tag = bytes.fromhex(tag)
        nonce = bytes.fromhex(nonce)

        assert len(nonce) == 15
        
        cipher = AES.new(aes_key, AES.MODE_OCB, nonce=nonce)
        plaintext = cipher.decrypt_and_verify(ciphertext, tag)

        self.decryptedText.text = plaintext.decode()



if __name__ == '__main__':
    mainApp().run()
