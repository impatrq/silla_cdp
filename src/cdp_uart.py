from machine import UART
from utime import sleep_ms

class ControlUART():
    def __init__(self, baud:int, tx_pin: int, rx_pin: int):
        self.__uart = UART(2, baudrate=baud, tx=tx_pin, rx=rx_pin)
        print(f"Inicializado UART en los pines tx = {tx_pin}, rx = {rx_pin}")

    def send_bytes(self, msg: str):
        self.__uart.write(msg)

    def read_bytes(self) -> bytes:
        if self.__uart.any():
            r = self.__uart.read()
            return r
        return b'0'

    def read_string(self) -> str:
        rb = self.read_bytes()
        return rb.decode()

    def dummy_read(self, msg: str, times: int):
        i = 0
        while i < times:
            self.send_bytes(msg)
            sleep_ms(500)
            print(self.read_bytes())
            i += 1

    def send_and_receive(self, msg: str):
        self.send_bytes(msg)
        sleep_ms(500)
        return self.read_string()
