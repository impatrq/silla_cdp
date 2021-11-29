#define F_CPU 16000000UL

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
	ASS1,
	ASS2,
	APB,
	SWITCH
} ASK;

// Para facilitar la lectura?
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
	else if (strncmp(ask_value, "as1", 3) == 0) {
		return ASS1;
	}
	else if (strncmp(ask_value, "as2", 3) == 0) {
		return ASS2;
	}
	else if (strncmp(ask_value, "apb", 3) == 0) {
		return APB;
	}
	else if (strncmp(ask_value, "swi", 3) == 0) {
		return SWITCH;
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
	PORTB =	0x10;	// PB4 activar pull-up
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
		// Limpiar print_buffer antes de hacer algo.
		memset(print_buffer, 0, sizeof(print_buffer));
		
		// Esperar lectura de 6 bytes
		uart_wait_read_string(reading, len);
		
		// Entrar si los primeros 3 bytes son "ask"
		if (strncmp((char*)reading, "ask", 3) == 0) {
			// Meter en ask_value los ultimos 3 bytes
			sprintf((char*)ask_value, (char*)reading + 3);
			
			// Convertir ask_value a una int (para usar un switch case)
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
				case ASS1:
					adc_pin_select(ADC2_PIN);
					convert = adc_convert();
					sprintf((char*)print_buffer, "%u", convert);
				break;
				case ASS2:
					adc_pin_select(ADC3_PIN);
					convert = adc_convert();
					sprintf((char*)print_buffer, "%u", convert);
				break;
				
				// Devolver datos de joystick en formato "joy_x-joy_y-joy_sw"
				case SWITCH: ;
					uint16_t convert2 = 0;

					adc_pin_select(ADC4_PIN);
					convert = adc_convert();

					adc_pin_select(ADC5_PIN);
					convert2 = adc_convert();

					pin_value = (PINB & (1 << PINB4)) >> PINB4;

					sprintf((char*)print_buffer, "%u-%u-%d", convert, convert2, pin_value);
				break;
				
				// En caso que no se haya pedido correctamente.
				default: sprintf((char*)print_buffer, "ASKERR"); break;
			}
		}
		else if (strncmp((char*)reading, "mux", 3) == 0) {
			// Meter en ask_value los ultimos 3 bytes
			sprintf((char*)ask_value, (char*)reading + 3);
			
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
			
			// Enviar mensaje de confirmacion
			sprintf((char*)print_buffer, "MUXSET");
		}
		else {
			// Enviar mensaje de Value Error
			sprintf((char*)print_buffer, "VALERR");
		}

		// Enviar print_buffer
			uart_send_string(print_buffer);
    }
}

