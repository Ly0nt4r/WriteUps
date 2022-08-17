# MONITORS

<img width="593" alt="monitors" src="https://user-images.githubusercontent.com/87484792/185144891-1929fa9f-e63a-42cc-97f4-c0f7f429c681.png">

## Datos de Interés

Esta máquina la catalogaría de excelente. Son conceptos básicos lo que explotaremos, pero requieres tener buen ojo donde buscar. # Completar


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
