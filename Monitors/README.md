# MONITORS

<img width="593" alt="monitors" src="https://user-images.githubusercontent.com/87484792/185144891-1929fa9f-e63a-42cc-97f4-c0f7f429c681.png">

## Datos de Interés

Esta máquina la catalogaría de excelente. Son conceptos básicos lo que explotaremos, pero requieres tener buen ojo donde buscar. Empezaremos con una enumeración basica que tras investigar su puerto 80, nos dará como resultado un dominio existente. En este dominio encontraremos alojado un WordPress. 


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

Por desgracia en el panel de sesión de Wordpress no resultó ser válidos. El usuario no se encontraba como válido, **admin** si era válido, pero esa contraseña no.
En este punto tuve que investigar un poco más archivos que pudieran interesarme. Claves privadas, archivos de logs... nada parece funcionar.

## Shell como www-data

En este punto tenemos un dominio, y una forma de leer archivos arbitrarios de la maquina victima. Se me ocurrió que podria leer:

`/etc/apache2/sites-available/000-default.conf`

En este archivo se encuentran dominios junto al puerto que lo hostea. Echaré un ojo para ver si hay algo interesante que pueda ayudarme.

`view-source:http://monitors.htb/wp-content/plugins/wp-with-spritz/wp.spritz.content.filter.php?url=../../../../../../etc/apache2/sites-available/000-default.conf`

De primeras me costó verlo, pero arriba del todo hay una parte comentada donde tenemos dos dominios. Aunque terminan en *.conf*, realmente parecen ser conocidos.
El primero es el dominio que ya conocemos, el segundo tiene un subdominio extra.

Agregamos este subdominio a nuestro */etc/hosts*:

`cacti-admin.monitors.htb.conf`



