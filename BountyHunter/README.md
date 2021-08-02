# BOUNTYHUNTER 
![Bounty](https://user-images.githubusercontent.com/87484792/127788465-c99206d0-c1d8-491f-8e33-ea743e4c4165.png)
</br>
<img src= "https://img.shields.io/badge/difficulty:: -3FE716?style=plastic&logo=hackthebox&logoColor=white&labelColor=16E798"> </img>
<img src= "https://img.shields.io/badge/Easy-16E798?style=plastic"> </img> 
<img src= "https://img.shields.io/badge/Medium-E77816?style=plastic"> </img>
</br>

##

# Datos previos de Interés  

***Esta maquina cuenta con una dificultad facil-media y con una puntuación de los usuarios de: <img src= "https://img.shields.io/badge/4,4 stars -16DEE7?style=plastic&logo=RiseUp&logoColor=white&labelColor=16E798"> </img>*** 
</br></br>
***Su explotación esta registrada en la conocida "OWASP TOP-10"***
</br></br>
***Se necesita algún conocimiento previo de programación (Python a ser posible) para el entendimiento de la escalada***

# ENUMERACIÓN DE PUERTOS

En primera instancia, vamos a enumerar los puertos que tiene abierta la maquina. Para ello vamos a utilizar la herramienta ``NMAP`` 
Dicha herramienta se encuentra por defecto tanto en parrot como en linux y otras distribuciones orientadas a la rama de ciberseguridad.

Para ello, vamos a empezar abriendo la consola y ejecutando dicho comando:

     sudo nmap --min-rate 5000 --open -vvv -n -sS -Pn -p- -oG <NombreFicheroGuardarEscanero> <IP_Victim>

Una vez ejecutado, tendremos algo como esto: </br>
  ![nmap_enumeration2](https://user-images.githubusercontent.com/87484792/127789907-a45d7bb4-0d20-45de-88c8-476fdc3e6c3d.png)
</br>
Como podemos observar, tenemos el puerto **80** y el puerto **22** open, lo que significa que tenemos una pagina web escuchando por el puerto 80, y ssh escuchando en el 22
</br> </br>

Bien vamos a empezar mirando que nos encontramos en dicha pagina web, una vez entramos en Firefox (o cualquier navegador) y ponemos la ip de la maquina, podemos ver lo siguiente:
![web_1](https://user-images.githubusercontent.com/87484792/127790103-6438ccb8-47ba-4ddb-a01e-a6ddf85525bf.png)

A simple vista no parece que haya gran cosa, se trata de una pagina normal con 3 enlaces que nos redigiran a otros sitios de la web (About, Contact y **PORTAL**)
Recalco **PORTAL** porque tanto About como Contact no tienen un hiper-enlace dentro de la web, por lo que esta "inservible". </br>
Según wappalyzer (extensión que nos muestra mucha información de la web) no esta corriendo nada importante, así que vamos a obviar esa parte. 

# ENUMERACIÓN DE DIRECTORIOS

Bien como hemos visto, la pagina no tiene mucho que ofrecer, sin embargo...¿Porque no buscamos directorios "ocultos"? **Fuzzear** la web, sería mi siguiente paso en busca de información valiosa. Para ello vamos a utilizar la herramienta ``dirsearch``. Podeis Utilizar cualquier otra herramienta tales como wfuzz, dirbuster, etc...
En este caso es posible que algúnas versiones no traigan de serie la herramienta. Os dejo aquí un enlace directo para descargarla.</br>
<img src= "https://img.shields.io/badge/dirsearch-16E798?style=plastic&logo=github&logoColor=white"> </img> </br> (https://github.com/maurosoria/dirsearch) </br>

Una vez lo tengamos instalado procedemos a su ejecución, en este caso sería tal que así:
``python3 <RutaDelDirsearch>/dirsearch.py -u <IP_Victim> -w <LibreriaParaFuzzearRuta> -e <extensiones>``</br></br>
En mi caso fue tal que así, pero podeis probar según veais necesario (como más extensiones, u otras libreria): </br>
 ```python3 dirsearch/dirsearch.py -u 10.10.11.100 -e .txt,.php```
> Como podeis comprobar, yo utilizé la libreria que viene por defecto en dirsearch y este fue el resultado:
![fuzz_1](https://user-images.githubusercontent.com/87484792/127791094-ad8c81b2-ccc2-4be6-92ac-cd8266ca610b.png)</br>

¡Bien! en este caso hemos encontrado varios archivos php, entre ellos me llama la atención bd.php
> Puede que aquí se oculten credenciales potenciales 
</br>
Si lo intentamos abrir vamos a ver que esta aparentemente vacio, no podemos visualizar si existe contenido dentro.
Por lo que de momento vamos a pasar de él y vamos a observar que contiene los directorios "resources" y "assets"</br>
> Este ultimo no contiene nada interesante ni que podamos visualizar 
 Nos centraremos en resources
</br>

Bien, vamos a disponernos a entrar en dicho directorio y a ver que encontramos:
![index_resources](https://user-images.githubusercontent.com/87484792/127791465-988c2be9-5d1d-4714-b8d8-37affb39f605.png)
</br></br>
¡Vaya!, parece que hay unos cuantos archivos aqui dentro.. me llama la atención ese Readme.txt

