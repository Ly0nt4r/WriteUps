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
Por lo que de momento vamos a pasar de él y vamos a observar que contiene los directorios "resources" y "assets" pero solo vamos a centrarnos en resources </br>

Bien, vamos a disponernos a entrar en dicho directorio y a ver que encontramos:
![index_resources](https://user-images.githubusercontent.com/87484792/127791465-988c2be9-5d1d-4714-b8d8-37affb39f605.png)
</br></br>
¡Vaya!, parece que hay unos cuantos archivos aqui dentro.. me llama la atención ese README.txt, veamos que se esconde en su interior:

![resources_readme](https://user-images.githubusercontent.com/87484792/127791991-f73a8823-071b-4d14-9848-9fbfc96209a4.png)
> El propietario de este archivo nos comenta que hay una cuenta 'test' que aún no han deshabilitado en "portal", y que deben de enlaza su programa a la base de datos...
</br>

Vamos entonces a Portal a ver que podemos encontrar. Nos volvemos a dirigir a la pagina principal y pinchamos en ***Portal***. Aparecerá esto:
![portal php](https://user-images.githubusercontent.com/87484792/127792215-631d2d24-cbfd-4341-924f-ba9e7f86468c.png)

Vamos a pinchar, en este sitio no parece mucho que podamos hacer. Una vez redirigidos, entramos aqui:

![log_submit php](https://user-images.githubusercontent.com/87484792/127792249-6bdc9934-5138-4f3b-8d0b-a07cedade16b.png)

> Parece una especie de db-exploit versión minimalista, probé a rellenar con varias cosas pero solo imprime lo escrito, no interpreta.

Miré el codigo fuente a ver que hacia este especie de formulario, encontré un archivo .js, y al mirarlo encontré esto:

![bountylog_view-source](https://user-images.githubusercontent.com/87484792/127792397-3100e324-4b6c-4d1e-8bb0-d5f24421ace2.png)

Vaya por donde... estas haciendo uso de XML. Y vaya por donde... me puedo aprovechar de ello.

# Explotación

> Haremos uso de una vulnerabilidad conocida como XXE, donde inyectaremos codigo, en este caso una entidad que actuará de variable para guardar datos. </br>

Para hacer este tipo de inyeccion, utilizaremos el codigo del formulario, modificando unicamente (de manera opcional, aunque recomendable) el tipo de encoding a **UTF-8**
¿Recordais ese archivo db.php que podia contener información confidencial? Vamos a intentar recopilar su información a traves de esta vulnerabilidad.

Abriremos la consola de nuestro navegador, y ejecutaremos el siguiente comando: 

```
var xml = `<?xml  version="1.0" encoding="UTF-8"?>

<!DOCTYPE replace [<!ENTITY xxe SYSTEM "php://filter/read=convert.base64-encode/resource=/var/www/html/db.php">]>
<bugreport>
   <title>&xxe;</title>
   <cwe>texto</cwe>
   <cvss>texto</cvss>
   <reward>texto</reward>
 </bugreport>`
```

Como podeis ver la ejecución es muy sencilla, agregamos una entidad llamada xxe, y la llamamos en un nodo xml para que se interprete. En este caso, estamos utilizando un payload de PHP, estos payload lo podeis encontrar por internet facilmente.

Despues de ejecutarlo, debemos llamar a la siguiente función que nos devolverá la data, luego nos reportará esto:
![base64-xxe](https://user-images.githubusercontent.com/87484792/127793257-1bbc2b97-e0b2-45ce-ab4f-2e94b38e367f.png)


¡Efectivamente! estabamos en lo cierto. Ese archivo db.php contiene datos que nos pueden ayudar, pero esta encryptado en lo que parece ser Base64. Esto tiene facil solución.
Nos copiamos ese trozo de codigo, y en la consola lo guardamos en un archivo. Dicho archivo lo desencryptaremos con un simple ``base64 -d`` tal que asi: 

![decodeb64linux](https://user-images.githubusercontent.com/87484792/127793110-a20b8c15-7dcc-4e3d-8b16-1974828b1f9a.png)
> Una vez desencryptado obtenemos credenciales que probaremos a continuación.

La base de datos se encuentra en localhost, por lo que no tenemos alcance, ni siquiera esta operativa según nos comentaban al probar el "db-exploit minimalista"
Pero las credenciales si que nos pueden servir. Recordamos que tenemos el servicio SSH abierto, podemos probar las credenciales a ver si entramos.

>En este punto probé con 'test', 'bounty', 'root y un largo etc.. pero no parecía funcionar.

# Accediendo al sistema

Es aquí cuando debemos pensar como obtener el usuario. ¿Que archivo del sistema recoge información de los usuarios del sistema? Efectivamente ``/etc/passwd/``
Y como podemos mirarlo? Pues volviendo a utilizar XXE. 
> Existe una forma alternativa, podemos utilizar fuerza bruta con hydra por ejemplo para obtener el user, pero demora bastante.
</br>
Lanzamos un nuevo ataque XXE y obtenemos la lista de usuarios del sistema:

![Sin título](https://user-images.githubusercontent.com/87484792/127793546-4c84852e-be21-4744-973a-4aa0db054b09.png)
> Recuerda cambiar el Payload, ahora no buscamos archivos PHP sino un file del sistema.

Y alli tenemos el usuario.. ***development***
probamos con el SSH tal que asi:
``` ssh development@10.10.11.100 ``` 
Y acto seguido introducimos la contraseña encontrada. Finalmente...

![ssh development](https://user-images.githubusercontent.com/87484792/127793730-5720bed3-c845-4449-9b0f-00226a60f923.png)

Ya tenemos acceso como usuario! por lo que podemos ver la flag de usuario:
![catuser](https://user-images.githubusercontent.com/87484792/127793820-64ad893f-267e-4e73-9862-9306aacd4025.png)

> Leemos aquí tambien una nota del que parece ser nuestro jefe John, diciendonos que tenemos que probar un programa y que por ello nos va a dar "permisos especiales". ¿Root? ¿Eres tú?
</br>

Vamos a comprobar entonces que permisos tenemos, para ello bastará con un simple ``sudo -l``

![sudo-l](https://user-images.githubusercontent.com/87484792/127793943-5534cf20-6632-47a6-8e60-b8b7659f12b8.png)
> Vaya, al parece necesitamos debuguear un archivo en python3 que valida tickets.



EN PROCESO DE FINALIZAR

![root](https://user-images.githubusercontent.com/87484792/127794042-efe621d9-b890-4080-9268-8b7430f8046f.png)
AA
![ticket_valido](https://user-images.githubusercontent.com/87484792/127794331-b7281ad3-953a-4343-bf5a-2feb0dacec7a.png)

