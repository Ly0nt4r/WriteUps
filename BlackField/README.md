# BLACKFIELD

![image](https://user-images.githubusercontent.com/87484792/185927247-84e56c72-0f5e-4dc7-b4bf-1b05adfe5ef9.png)

## Datos de interés

BlackField es una buena maquina para practicar Directorio Activo. Muy recomendable desde mi punto de vista.
Empezaremos con un ataque **asreproast attack**, tras un previo descubrimiento de usuarios en un recurso compartido.
Recopilaremos información con bloodhound, tras lo cual haremos un movimiento lateral a otro usuario del sistema.
Re-volveremos a investigar los recursos compartidos esta vez con el nuevo usuario y encontraremos un volcados de memoria de proceso.
**lsass.exe** será nuestro objetivo. Tras un volcado con pypykatz obtendremos el hash que me permitirá conectarme a la maquina remota a traves de *WINRM*.
Abusaré de los privilegios de backups para leer el archivo ntds.dit que contiene todos los hash para el dominio, para finalmente conseguir el hash de Administrador.

## Reconocimiento

![image](https://user-images.githubusercontent.com/87484792/185928850-d7dfb56d-8a6c-46bb-bff0-59499a198f38.png)

Como se muestra en la imagen, los puertos comunes para una maquina de directorio activo están abiertos, no hay ninguno que llamen en especial la atención.

### SMB - 445

El primer paso será investigar que recursos compartidos tenemos a nivel de red. Sin credenciales válidas, probaré con una sesión nula.

`smbmap -H 10.10.10.192 -u 'null'`

![image](https://user-images.githubusercontent.com/87484792/185932051-41899009-64de-448c-8d24-fde4be501609.png)

Encuentro dos recursos compartidos con capacidad de lectura. 
Tras un vistazo rápido en ambos, encontramos una lista de usuarios (carpetas de usuarios) en **profiles$**
