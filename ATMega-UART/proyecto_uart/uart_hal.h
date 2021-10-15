#ifndef UART_HAL_H_
#define UART_HAL_H_

#include <avr/io.h>
#include <avr/interrupt.h>
#include <util/delay.h>

#define RX_BUFFER_SIZE 128

void uart_init(uint32_t baudrate, uint8_t double_speed);
void uart_send_byte(uint8_t c);
void uart_send_array(uint8_t *c, uint16_t len);
void uart_send_string(uint8_t *c);
uint16_t uart_read_count(void);
uint8_t uart_read(void);
void uart_wait_read_string(uint8_t* str, uint16_t len);

#endif /* UART_HAL_H_ */