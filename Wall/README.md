# Wall

![1_XItXYcP8tLhBnR8FvyPing](https://user-images.githubusercontent.com/87484792/184016462-429034df-66b4-4f34-8386-107417732885.png)

## Datos de Interés

Siento que esta máquina no tiene un gran nivel de dificultad. Será cuestión de investigar un poco sobre el servicio de monitorización que hostea el puerto 80 en el servidor Web. En este caso se trata de **Centreón**. La escalada de privilegios se hará a traves de un SUID que ya hemos podido explotar en otras maquinas, será el screen con versión 4.5.0. Explicaremos de forma manual algunos scripts para entender la intrusión.

## Enumeración

Empezaremos con la fase de enumeración, usaremos nmap para descubrir puertos abiertos. 

`sudo nmap --min-rate 5000 -vvv -p- -sS -Pn -n -oN openPorts.txt 10.10.10.157`

Esta maquina solamente tiene dos puertos abiertos.

![image](https://user-images.githubusercontent.com/87484792/184020390-8073e636-5782-434b-8c9e-d632cec64022.png)

Por un lado tendremos puerto 22 (SSH) y por otro lado el puerto 80 (HTTP).

##  Reconocimiento 

Con SSH no podemos hacer gran cosa ahora mismo, no tenemos credenciales válidas. Iremos a revisar el otro puerto. Encontramos una pagina web con un "Default Page" de Apache. 

![image](https://user-images.githubusercontent.com/87484792/184023616-68fb0323-61b8-4928-863c-4e1f63d08612.png)

Es buena idea empezar a hacer fuzzing, tiraré de dirsearch, en caso de no encontrar nada usaré otro diccionario o haré uso de wFUZZ. Aunque ya puedo adelantar que con dirsearch me fue suficiente.

![image](https://user-images.githubusercontent.com/87484792/184025529-e16886f4-9fc6-4d8c-9cae-5fb7eb29bdd9.png)

Hay cosas interesantes en el reporte del fuzz. 
- */panel.php* parece ser una pequeña troleada del author de la caja.
- */Monitoring*, no podemos acceder. Necesitamos credenciales.
- */centreon* es un software de monitoreo. No tenemos credenciales pero si que tenemos algo muy importante, **la versión**.

![image](https://user-images.githubusercontent.com/87484792/184026472-c0a47dbd-145d-4564-800e-1f39c039f513.png)

La misma web nos da la información que estamos contra un login de versión 19.04

Esto es muy bueno ya que haciendo una busqueda simple en Google, vemos varios CVE y podemos ver que es vulnerable a **RCE**.
Para poder ejecutar estos CVE necesitamos acceso a una cuenta administrador, pero puesto que no tengo ninguno, intentaré bruteforcearlo.
