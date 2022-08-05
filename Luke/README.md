# Luke

![0](https://user-images.githubusercontent.com/87484792/183135778-076b0153-fce6-4c29-9681-b17879f5888a.png)

## Datos previos de Interés

Siento que esta maquina ha sido bastante buena para tocar temas de autenticación. Aprenderemos a manejar un poco mejor curl para hacer peticiones para descubrir como esta formado el token de autorización que nos falta. En esta maquina no tendremos una escalada de privilegios como tal, pues accederos al sistema directamente como root desde una consola web, pero enseñaré una de las miles formas en las que podemos meternos con una shell interactiva al sistema. 

## Enumeración de puertos

Empezamos con una enumeración basica, buscaremos puertos abiertos en la maquina victima.

` sudo nmap --min-rate 5000 --open -vvv -n -sS -Pn -p- -oG openPorts.txt 10.10.10.137`

Con la ejecución tendremos algo así:
![Screenshot_2022-08-05_14_19_28](https://user-images.githubusercontent.com/87484792/183140637-bb80500c-41f6-4f5f-8539-89e5ea2b2f54.png)

## FTP

Empezaremos por orden, el puerto 21 es un servidor FTP, intentaremos conectarnos con anonymous access.

![image](https://user-images.githubusercontent.com/87484792/183141482-ac8c5350-c5a5-43ea-b67e-9b824d5caa29.png)

Podemos observar que el acceso anonimo esta habilitado, de hecho es el único acceso disponible que se permite.
Dentro podemos observar una carpeta llamada **webapp**. Esta carpeta contiene dentro un archivo de texto llamado **"for_Chihiro.txt"**
Este documento contiene la siguiente información:

![3](https://user-images.githubusercontent.com/87484792/183142241-cfaf75d6-3a43-4d01-bff3-cb289f7c1bb4.png)

A modo de resumen, Derry nos cuenta que ha dejado unos archivos para que Chihiro pueda aprender un poco de front.
Con esto podemos sacar en cuenta que tenemos dos usuarios potencialmente validos *Derry* y *Chihiro*.

## SSH

El siguiente puerto sería el 22, este servidor contiene SSH, por lo que sin credenciales validas, no nos servirá de mucho.
Con los dos usuarios que tenemos, podriamos intentar hacer fuerza bruta. Pero no es la idea.

## WEB

### Pasaremos al puerto 80
Esta alojando una pagina web, cuyo contenido principal es este:

![Screenshot_2022-08-05_14_53_34](https://user-images.githubusercontent.com/87484792/183143076-913ae85c-7fbf-43fc-acc9-7b80dd9f6e09.png)
 
Es una pagina simple, los enlaces no son funcionales y el código fuente no nos aporta mucha información.
Haré un pequeño fuzzing con dirsearch para ver si consigo ver algo interesante, mientras investigo los demás puertos abiertos.

El escaneo del fuzzing nos muestra los siguientes resultados:

![fuzz](https://user-images.githubusercontent.com/87484792/183144513-d0480711-f4cf-4829-b447-c9bfb9f67e7a.png)

El resultado del escaneo nos muestra cosas interesantes.
Lo primero que me llama la atención es ese archivo de configuración **config.php** </br>
Hay otra cosa que me llama la atención, hay reportes con código de estado *401*, eso quiere decir que nos hará falta credenciales si queremos poder acceder a ellos.
El login.php tambien parece interesante, pero ya adelanto que no servirá para nada, es un rabbit hole.

En el interior de config.php podemos ver unas credenciales. 

![config](https://user-images.githubusercontent.com/87484792/183145474-444df030-ce0f-47bb-a5fa-bc828c5673f1.png)

Sería interesante guardarlas, de momento podemos probarlas en login.php o en las rutas con estado 401, sin embargo no conseguimos acceder.

### Puerto 8000

En el puerto 8000 nos encontramos con un panel de login. 
![8000](https://user-images.githubusercontent.com/87484792/183146455-ad29a029-763c-4695-a856-4cd0c8c89ea0.png)

De momento contamos con unas credenciales, sin embargo, nuevamente vuelven a no ser correctas. Fuzzear tampoco sirve de mucho, no nos reporta nada.
Dejaremos este punto para más adelante.

### Puerto 3000

![json](https://user-images.githubusercontent.com/87484792/183146921-b7f579ee-8a11-42b7-93d2-8d1fc1d02891.png)

Aquí encontraremos un mensaje JSON avisando de que no esta seteada el token de autenticación. La pagina espera una cookie de la cual no disponemos.
Hagamos un poco de fuzzing, para ver que podemos encontrar. Luego trataremos de formar esa cookie.

![f2](https://user-images.githubusercontent.com/87484792/183147971-43dda29d-a3a6-4793-b315-15e96c0f74e0.png)



