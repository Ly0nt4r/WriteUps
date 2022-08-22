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
Tras un vistazo rápido en ambos, encontramos una lista de usuarios (carpetas de usuarios) en **profiles$**.

## Support

Me copiaré el output en un archivo y me quedaré solo con los nombres de usuarios para posteriormente poder trabajar con ellos.
Tras ello, ejecutaré un ataque *asreproast attack* 

`python3 GetNPUsers.py -no-pass -usersfile users.txt BLACKFIELD.local/`

![image](https://user-images.githubusercontent.com/87484792/185952673-a95ce938-5f82-4eaf-948a-5986ccbfd835.png)

Procedemos a crackearlo.

![image](https://user-images.githubusercontent.com/87484792/185954026-279755ca-274f-4ab7-a0ae-0dc3abf4053e.png)

## Support -> Auditor2020

Despues de este paso, recopilaré información del AD, a través de bloodhound-python.

`bloodhound-python -u Support -p '#00^BlackKnight' -ns 10.10.10.192 -d blackfield.local -c all`

Bloodhound es una herramienta que nos permitirá recolectar información, nos conectaremos a traves de neo4j. Para el volcado de información, usaré Bloodhound-python que es una buena alternativa compatible con linux.

![image](https://user-images.githubusercontent.com/87484792/185989059-9c0e0fb7-b52a-478e-adf9-0e6ab0fc198a.png)

Y el volcado sería este:

![image](https://user-images.githubusercontent.com/87484792/185989568-a55a1a1e-dacc-4d45-9276-ab5e6cdf10a8.png)

Necesitamos acceder a BloodHound para subir los Json, para ello primero abriremos neo4j `neo4j start` , y despues, `bloodhound`.

Veremos algo como esto:

![image](https://user-images.githubusercontent.com/87484792/185991118-dc3803b1-3883-42ad-b18a-aa66652d48a5.png)

Ponemos credenciales > uploads data > seleccionar todos los json.

![image](https://user-images.githubusercontent.com/87484792/185992980-11530267-4d1c-4d74-b605-4f53d74ad6b6.png)

Vemos que el usuario Support puede cambiar la contraseña de Audit2020. Esto es bastante bueno, aprovecharemos para hacerlo y poner la contraseña que queramos.

`https://www.thehacker.recipes/ad/movement/dacl/forcechangepassword` 

En esta pagina podemos ver como cambiar la contraseña.

Como el usuario Support entramos en RCPClient > `setuserinfo2 audit2020 23 admin123$`

Y con esto ya tendremos cambiado la contraseña en el usuario audit2020.

## Audit2020 -> Svc_backup

Una vez tenemos el usuario **Audit2020**, procedemos a revisar nuevamente el recurso smb. Esta vez tenemos un nuevo recurso con capacidad de lectura.Todo apunta que los tiros iran por aqui.

![image](https://user-images.githubusercontent.com/87484792/185996425-c8cff322-db4b-4365-b8bd-fe46b3b95325.png)

Dentro de este recurso, hay información bastante importante, sobre todo un volcado de memoria. Esto será util para intentar obtener Hashes.

![image](https://user-images.githubusercontent.com/87484792/185996704-ce6b1ec3-fbc7-4f14-9a67-4a2ced83bbd4.png)

Aqui hay cosas interesantes, el comprimido **lsass.zip** es algo a tener en cuenta. **lsass* es un proceso en los sistemas operativos Microsoft Windows, responsable de hacer cumplir la política de seguridad en el sistema. Verifica que los usuarios inicien sesión en un equipo o servidor Windows, gestiona los cambios de contraseñas y crea tokens de acceso. Aqui podrian existir tokens que nos permitan el acceso a otro usuario.

Obtenemos un archivo *.DMP*, que como nos decian antes, se trata de un volcado de memoria. Aqui podriamos jugar con mimikatz para ver su contenido. Pero para no irme a la maquina virtual de Windows, utilizaré una herramienta alternativa, pypykatz.

`pypykatz lsa minidump lsass.DMP`

![image](https://user-images.githubusercontent.com/87484792/185997502-2cd38f40-31af-41e3-9acb-250b2dd926dc.png)

Con esto, ya tenemos un hash, probemos si es valido.

![image](https://user-images.githubusercontent.com/87484792/185997852-7fd0754e-7eb7-43c3-9f8d-931f9d9b5f28.png)

Sí, **Pwn3d!**. Nos podemos conectar a la maquina victima a traves de winrm!

## svc_backup -> Administrator

Lo primero que hago, y recomiendo hacer, es mirar los privilegios con los que cuenta el usuario en cuestión. En este caso contamos con dos privilegios que me llaman la atención, pero tratandose de una cuenta de **backup**, era de esperar.

![image](https://user-images.githubusercontent.com/87484792/185999814-f0c31c61-8e19-4bee-a84e-c0bc547c2099.png)

```
SeBackupPrivilege             Back up files and directories  Enabled
SeRestorePrivilege            Restore files and directories  Enabled
```

Estos dos privilegios nos permiten convertirnos en administrador a traves de una copia del sistema y un volcado. Para ello dejo esta pagina de apoyo, donde explican claramente (y que seguí) para la escalada de privilegios.

`https://medium.com/r3d-buck3t/windows-privesc-with-sebackupprivilege-65d2cd1eb960` # En mi caso seguí el step (Method #1 — Disk shadow + Robocopy)

Con todos los pasos seguidos, tendremos los dos archivos a punto para ser ejecutados.


