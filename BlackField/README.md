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

