## Este modulo solo se puede importar en una RPi.
import RPi.GPIO as gpio
import subprocess

offPin = 9

## Esperar por interrupción
gpio.setmode(gpio.BCM)
gpio.setup(offPin, gpio.IN, pull_up_down=PUD_DOWN)
gpio.wait_for_edge(offPin, gpio.FALLING)

## Comando de apagado
subprocess.call(['shutdown', '-h', 'now'], shell = False)
