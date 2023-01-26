#pragma once
#include <stdint.h>

typedef int8_t i8;
typedef int16_t i16;

typedef enum e_error_code {
	SUCCESS,
	INVALID_ATOM,
	INVALID_FORMAT,
	INVALID_LINK,
	INVALID_NB_ATOMS
}	t_error_code;


typedef struct s_edge {
	i16 from;
	i16 to;
	i8 type;
}	t_edge;
