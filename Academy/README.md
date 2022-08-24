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

En el panel de Register me registro con `admin2:admin2`, parece funcional y tiene pinta de que puedo loguearme con estas credenciales.

![image](https://user-images.githubusercontent.com/87484792/186457342-4fe2fca4-9bda-4422-aafd-3907ac18ec52.png)
