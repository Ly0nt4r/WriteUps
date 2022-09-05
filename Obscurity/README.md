# Obscurity
![banner](https://user-images.githubusercontent.com/87484792/188477619-07de5c58-16ee-4c04-832b-d7b4b311e31b.png)

## Datos de interés
Obscurity esta diseñada con tematica de "Security through obscurity". Este principio aplica que si algo "no es visible" para el atacante, le resultará dificil ser comprometido. Empezaremos con un fuzzeo de un directorio oculto para encontrar un codigo fuente de "desarrolladores" de la propia pagina web en producción. Tras revisar el código veremos que hay definido un metodo que nos dará acceso a injección de codigo en Python. Una vez injectado codigo y obtenido una shell, veremos que hay un usuario disponible llamado "robert", el cual accederemos gracias a archivos encriptados en su carpeta personal, previo desencriptado. Finalmente, obtendremos root gracias a un permiso SUDO, aunque hay varios caminos disponibles para la obtención de root.

## Enumeración

Empezamos con una enumeración basica de la maquina victima. En este caso tendremos dos puertos abiertos (y dos cerrados, lo obviaremos).

![image](https://user-images.githubusercontent.com/87484792/188515254-0e6b1ea0-20c0-4f71-a49b-873c3f7ce277.png)

En este caso tendremos **SSH** y **HTTP** por el puerto *8080*

**En proceso** 
