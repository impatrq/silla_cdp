#ifndef F_CPU
#define F_CPU 16000000UL
#endif

#include <avr/io.h>
#include <avr/interrupt.h>
#include <util/delay.h>
#include <string.h>
#include <stdio.h>
#include "uart_hal.h"
#include "adc_hal.h"

uint8_t print_buffer[64] = {};

typedef enum {
	NONE,
	BAR,
	LUM1,
	LUM2,
	LUM3,
	LUM4,
	ASS1,
	ASS2,
	APB	
} ASK;

// ¿Para facilitar la lectura?
ASK ask_value_to_enum(char* ask_value) {
	if (strncmp(ask_value, "bar", 3) == 0) {
		return BAR;
	}
	else if (strncmp(ask_value, "lu1", 3) == 0) {
		return LUM1;
	}
	else if (strncmp(ask_value, "lu2", 3) == 0) {
		return LUM2;
	}
	else if (strncmp(ask_value, "lu3", 3) == 0) {
		return LUM3;
	}
	else if (strncmp(ask_value, "lu4", 3) == 0) {
		return LUM4;
	}
	else if (strncmp(ask_value, "as1", 3) == 0) {
		return ASS1;
	}
	else if (strncmp(ask_value, "as2", 3) == 0) {
		return ASS2;
	}
	else if (strncmp(ask_value, "apb", 3) == 0) {
		return APB;
	}
	else {
		return NONE;
	}
}

int main(void)
{
	uint16_t len = 6;
	uint16_t convert = 0;
	uint8_t reading[len];
	uint8_t ask_value[len/2];
	uint8_t pin_value = 0;
	
	ASK ask_state = 0;
	
	// Inicializar PORTB
	DDRB = 0x02;	// PB1 como salida
	DDRD = 0x60;	// PD5, PD6 como salida
	
	// Inicializar UART (baudrate = 9600, single)
	uart_init(9600, 0);
	
	// Inicializar pines ADC
	adc_init();
	adc_pin_enable(ADC0_PIN);
	adc_pin_enable(ADC1_PIN);
	adc_pin_enable(ADC2_PIN);
	adc_pin_enable(ADC3_PIN);
	adc_pin_enable(ADC4_PIN);
	adc_pin_enable(ADC5_PIN);
	
	// Habilitar interrupciones
	sei();
	
    while (1) 
    {
		// Esperar lectura de 6 bytes
		uart_wait_read_string(reading, len);
		
		// Entrar si los primeros 3 bytes son "ask"
		if (strncmp((char*)reading, "ask", 3) == 0) {
			// Meter en ask_value los ultimos 3 bytes
			sprintf((char*)ask_value, (char*)reading + 3);
			
			// Limpiar print_buffer y convertir ask_value a una int (para usar un switch case)
			memset(print_buffer, 0, sizeof(print_buffer));
			ask_state = ask_value_to_enum((char*)ask_value);
			
			switch (ask_state) {
				// Estos dos son pines digitales, vienen de una compuerta AND.
				case BAR: pin_value = (PINB & (1 << PINB2)) >> PINB2; sprintf((char*)print_buffer, "%d", pin_value); break;
				case APB: pin_value = (PINB & (1 << PINB3)) >> PINB3; sprintf((char*)print_buffer, "%d", pin_value); break;
				
				// Los que siguen son de entradas analogicas, vienen directo de los piezoelectricos.
				case LUM1: 
					adc_pin_select(ADC0_PIN);
					convert = adc_convert();
					sprintf((char*)print_buffer, "%u", convert);
				break;
				case LUM2:
					adc_pin_select(ADC1_PIN);
					convert = adc_convert();
					sprintf((char*)print_buffer, "%u", convert);
				break;
				case LUM3:
					adc_pin_select(ADC2_PIN);
					convert = adc_convert();
					sprintf((char*)print_buffer, "%u", convert);
				break;
				case LUM4:
					adc_pin_select(ADC3_PIN);
					convert = adc_convert();
					sprintf((char*)print_buffer, "%u", convert);
				break;
				case ASS1:
					adc_pin_select(ADC4_PIN);
					convert = adc_convert();
					sprintf((char*)print_buffer, "%u", convert);
				break;
				case ASS2:
					adc_pin_select(ADC5_PIN);
					convert = adc_convert();
					sprintf((char*)print_buffer, "%u", convert);
				break;
				
				// En caso que no se haya pedido correctamente.
				default: sprintf((char*)print_buffer, "ERR"); break;
			}
			
			// Enviar print_buffer
			uart_send_string(print_buffer);
		}
		else if (strncmp((char*)reading, "mux", 3) == 0) {
			// Meter en ask_value los ultimos 3 bytes
			sprintf((char*)ask_value, (char*)reading + 3);
			
			// Limpiar print_buffer
			memset(print_buffer, 0, sizeof(print_buffer));
			
			unsigned int i = 0;
			
			// Convertir y setear
			// MSB - Bit 2
			i = ask_value[0] - '0';
			PORTB ^= (-i ^ PORTB) & (1 << PINB1);
			
			// Bit 1
			i = ask_value[1] - '0';
			PORTD ^= (-i ^ PORTD) & (1 << PIND6);
			
			// LSB - Bit 1
			i = ask_value[2] - '0';
			PORTD ^= (-i ^ PORTD) & (1 << PIND5);
			
			// Enviar mensaje de confirmación
			sprintf((char*)print_buffer, "ADDRSET");
			uart_send_string(print_buffer);
		}
    }
}

