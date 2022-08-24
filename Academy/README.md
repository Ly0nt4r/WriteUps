En proceso 24/08/2022
# ACADEMY 

![Academy](https://user-images.githubusercontent.com/87484792/186432393-eb7af503-7ecd-438a-928b-1cd0cb754b90.png)

## Datos de interés 

**Academy** es una máquina que fue diseñada junto al inicio de la academia oficial de HackTheBox. **Academy** es una buena máquina y muy entretenida.
Empezaremos con un panel de registro muy parecido al de HackTheBox, tras modificar un parametro del registro podemos iniciar como una cuenta Admin.
Descubriremos un subdominio que tras la explotación de una deserializacion en Lavarel obtendremos una shell gracias a RCE. Encontraremos una contraseña de usuario en un archivo *.env*, dicho usuario tendrá permisos de ADM por lo que podremos leer archivos de log, en ellos encontramos un inicio de sesión que nos permitirá un movimiento lateral a otro user del sistema. Dicho usuario contrendrá permisos de SUDO ante un binario vulnerable que nos otorgará acceso como root.
