# MONITORS

<img width="593" alt="monitors" src="https://user-images.githubusercontent.com/87484792/185144891-1929fa9f-e63a-42cc-97f4-c0f7f429c681.png">

## Datos de Interés

Esta máquina la catalogaría de excelente. Son conceptos básicos lo que explotaremos, pero requieres tener buen ojo donde buscar. # Completar


## Enumeración

Empezamos con una enumeración basica de puertos:
`sudo nmap --min-rate 5000 -vvv -p- -sSCV --open -Pn -n -oN servicesPorts.txt 10.10.10.238`

**NMAP** nos reporta dos puertos conocidos: "22 (SSH) & 80 (HTTP)"

![image](https://user-images.githubusercontent.com/87484792/185152874-93dc1d57-3473-4bf3-91c1-706727d65b5c.png)

