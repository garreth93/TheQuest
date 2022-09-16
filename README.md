# TheQuest
Proyecto Final Keepcoding: Trata sobre una nave que debe buscar el camino a un nuevo planeta habitable.

Programas necesarios para ejecutar el juego:
Git - https://git-scm.com/downloads
Visual Code Studio - https://code.visualstudio.com/download

Despues de instalar los programas necesarios sigue las instrucciones de instalacion.

1 - Clonacion en instalacion del juego:

   Primero debes ir al repositorio del juego en este enlace https://github.com/garreth93/TheQuest.

   Luego en el boton verde llamado "Code" debes clickar y se desplegarán varias opciones, la mas óptima y facil es mediante "HTTPS".

   Deberás copiar el enlace que te proporciona. Luego, abrir el "Git Bash", y a continuacion navegar hacia la carpeta que desees con los comandos.

   Una vez posicionado en la carpeta deseada, escribir en terminal ```git clone https://github.com/garreth93/TheQuest.git```

   Se creará una carpeta dentro, con el nombre del juego y los archivos necesarios.

   Ahora puedes abrir visual studio code, y desde ahi abrir la carpeta creada anteriormente con clone.

2 - Puesta a punto del juego:

   Ahora una vez abierto con VSC la carpeta del juego, en su terminal deberás escribir el comando ```python -m venv env``` para crear un entorno virtual en el que
   a continuación instalar pygame.

   Hecho el entorno ahora tendrás que escribir en la terminal diferentes comandos dependiendo de tu sistema operativo para poder activar el entorno:

   Para windows -> ```.\env\Scripts\activate```
   Para Linux y Mac -> ```source /env/bin/activate```

   Una vez dentro del entorno virtual sabrás que estas dentro por que el prompt cambia. 

   Dentro deberás instalar el modulo pygame con ```pip install pygame```

   Cuando acabe de instalarse nos dispondremos a configurar la base de datos por último.

3 - Base de datos:

   Para que el juego pueda mantener una pantalla en la que se guarde la puntuacion de los jugadores, hay que hacer antes un paso importante. Deberas eliminar "records.db" en la carpeta data, y renombrar el records-copy.db con el nombre "records.db". 

Con esto el juego ya deberia funcionar perfectamente.
