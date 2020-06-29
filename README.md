# Taller de Sistemas Embebidos
## Integrantes:
    Edwin David Obando Venegas
    Darwin Josué Paniagua Rodríguez 
    Karol Sofía Rojas Méndez 
    Luis Alonso Vega Badilla 

##Indicaciones

Lo primero es preparar el entorno de trabajo, instalando los requerimientos para poky:
'''
sudo apt-get install gawk wget git-core diffstat unzip texinfo gcc-multilib \
     build-essential chrpath socat cpio python python3 python3-pip python3-pexpect \
     xz-utils debianutils iputils-ping python3-git python3-jinja2 libegl1-mesa libsdl1.2-dev \
     xterm
'''

Luego de elegir una carpeta para trabajar con yocto project, se ejecuta en una terminal:
'''
git clone git://git.yoctoproject.org/poky -b warrior
'''

Luego, dentro de la carpeta poky, se ejecuta:
'''
git clone https://github.com/agherzan/meta-raspberrypi -b warrior
git clone git://git.openembedded.org/meta-openembedded -b warrior
'''

Al ejecutar en ../poky
'''
source oe-init-build-env
'''
Se crea el directorio ../poky/build dentro del cual esta el directorio ../conf

Ya esta listo el entorno de trabajo, seguidamente agregamos los archivos de este repositorio:

1) La carpeta 'meta-py' agregarla a la carpeta poky/
2) Los archivos dentro de la carpeta 'conf' van en poky/conf/

Todo esta listo crear la imagen, ejecutando:
'''
bitbake core-image-base
'''