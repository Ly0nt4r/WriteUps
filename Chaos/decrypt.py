import os, time
from Crypto.Cipher import AES
from Crypto.Hash import SHA256
from Crypto import Random
from optparse import *
def decrypt(key, filename):
	chunksize = 64 * 1024
	outputFile = filename.split('en')[1]

	with open(filename, 'rb') as infile:
		filesize = int(infile.read(16))
		IV = infile.read(16)
		decryptor = AES.new(key, AES.MODE_CBC, IV)

		with open(outputFile, 'wb') as outfile:
			while True:
				chunk = infile.read(chunksize)

				if len(chunk) == 0:
					break

				outfile.write(decryptor.decrypt(chunk))
			outfile.truncate(filesize)
def getKey(password):
            hasher = SHA256.new(password.encode('utf-8'))
            return hasher.digest()
filename = raw_input("Enter filename: ")
password = raw_input("Enter password: ")
key = getKey(password)
decrypt(key,filename)
