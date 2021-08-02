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

# ENUMERACIÓN 

En primera instancia, vamos a enumerar los puertos que tiene abierta la maquina. Para ello vamos a utilizar la herramienta **NMAP** 
Dicha herramienta se encuentra por defecto tanto en parrot como en linux y otras distribuciones orientadas a la rama de ciberseguridad.

Para ello, vamos a empezar abriendo la consola y ejecutando dicho comando:

     sudo nmap --min-rate 5000 --open -vvv -n -sS -Pn -p- -oG <NombreFicheroGuardarEscanero> <IP>

Una vez ejecutado, tendremos algo como esto: </br>
  ![nmap_enumeration2](https://user-images.githubusercontent.com/87484792/127789907-a45d7bb4-0d20-45de-88c8-476fdc3e6c3d.png)
</br>
Como podemos observar, tenemos el puerto **80** y el puerto **22** open, lo que significa que tenemos una pagina web escuchando por el puerto 80, y ssh escuchando en el 22
</br> </br>

Bien vamos a empezar mirando que nos encontramos en dicha pagina web, una vez entramos en Firefox (o cualquier navegador) y ponemos la ip de la maquina, podemos ver lo siguiente
![web_1](https://user-images.githubusercontent.com/87484792/127790103-6438ccb8-47ba-4ddb-a01e-a6ddf85525bf.png)
