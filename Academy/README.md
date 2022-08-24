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

Al parecer es otro login, pero como se puede ver en el titulo, es un login de cuentas administradores.
Podiamos intentar buscar las credenciales, o bruteforcearlo, pero antes de todo.. echemos un ojo al comportamiento de la web cuando registramos una cuenta nueva.
Utilizaremos BurpSuite para enviar las request a traves de un proxy, en él, visualizaremos la data que enviamos.

![image](https://user-images.githubusercontent.com/87484792/186492718-7f9b21c1-ac7c-4293-9c42-81e046afe846.png)

**roleid** parece ser un controlador que asigna a la cuenta un "Rol". El valor inicial es un 0, pero... ¿que pasa si lo cambiamos de valor? en este caso un 1.
La creación de la cuenta es exitosa, y al probarlo en el admin.php nos da como resultado el poder adentrarnos en una "lista/tabla de tareas"

![image](https://user-images.githubusercontent.com/87484792/186493573-fa1110cb-2096-487b-9409-65cab9fe9274.png)

Tenemos un subdominio nuevo que seria muy raro que pudiesemos encontrar en un diccionario común, así que agregemoslo al */etc/hosts*


