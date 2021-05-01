## Este modulo solo se puede importar en una RPi.
import RPi.GPIO as gpio
import subprocess

offPin = 9

## Codigo comentado porque no se puede probar pines en una RPi emulada.
gpio.setmode(gpio.BCM)
gpio.setup(offPin, gpio.IN, pull_up_down=PUD_DOWN)
gpio.wait_for_edge(offPin, gpio.FALLING)

## Reemplazo temporal para probar el apagado
# while True:
#	cmd = raw_input("Input:")
#	if cmd=="shutdown":
#		break
#	else:
#		print(cmd)

## Verdadero comando de apagado
subprocess.call(['shutdown', '-h', 'now'], shell = False)
