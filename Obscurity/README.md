# Obscurity
![banner](https://user-images.githubusercontent.com/87484792/188477619-07de5c58-16ee-4c04-832b-d7b4b311e31b.png)

## Datos de interés
Obscurity esta diseñada con tematica de "Security through obscurity". Este principio aplica que si algo "no es visible" para el atacante, le resultará dificil ser comprometido. Empezaremos con un fuzzeo de un directorio oculto para encontrar un codigo fuente de "desarrolladores" de la propia pagina web en producción. Tras revisar el código veremos que hay definido un metodo que nos dará acceso a injección de codigo en Python. Una vez injectado codigo y obtenido una shell, veremos que hay un usuario disponible llamado "robert", el cual accederemos gracias a archivos encriptados en su carpeta personal, previo desencriptado. Finalmente, obtendremos root gracias a un permiso SUDO, aunque hay varios caminos disponibles para la obtención de root.

## Enumeración

Empezamos con una enumeración basica de la maquina victima. En este caso tendremos dos puertos abiertos (y dos cerrados, lo obviaremos).

![image](https://user-images.githubusercontent.com/87484792/188515254-0e6b1ea0-20c0-4f71-a49b-873c3f7ce277.png)

En este caso tendremos **SSH** y **HTTP** por el puerto *8080*

Encontramos una pagina web simple.

![image](https://user-images.githubusercontent.com/87484792/188631527-51987c76-88ab-476b-91e0-35c27a63db59.png)

Bajando un poco más, podemos encontrar un mensaje para developers. Esto puede ser crucial. Nos dice que hay un directorio oculto donde se encuentra un archivo de python.

![image](https://user-images.githubusercontent.com/87484792/188658448-98f4e9ad-17fc-4813-ad9c-06047288dcae.png)

No conocemos la ruta, pero si el archivo. Podriamos tratar de fuzzear para ver que directorio nos devuelve un 200.

![image](https://user-images.githubusercontent.com/87484792/188658574-fb9df87c-0fce-49d8-85cd-d7dec097aa8c.png)

Como se puede ver, hemos encontrado la ruta "oculta" a raiz de un archivo que se encontraba dentro. Si accedemos a la ruta, podemos ver el codigo fuente.

![image](https://user-images.githubusercontent.com/87484792/188662942-21933a0a-99f0-4cc9-b79d-d6bcdf585305.png)

Me lo bajaré y lo inspeccionaré en mi maquina atacante. Este archivo según nos cuentan, esta en producción. Quiere decir que todo lo que podamos encontrar en el código fuente, nos servirá para atacar a la pagina web.



