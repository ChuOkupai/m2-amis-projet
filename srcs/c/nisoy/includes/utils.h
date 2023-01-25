#pragma once
#include <stdint.h>

typedef int8_t i8;
typedef int16_t i16;
typedef int32_t i32;
typedef int64_t i64;

typedef enum e_error_code {
	SUCCESS,
	INVALID_ATOM,
	INVALID_FORMAT,
	INVALID_LINK,
	INVALID_NB_ATOMS,
	INVALID_NB_LINKS
}	t_error_code;


typedef struct s_edge {
	i16 from;
	i16 to;
	i8 type;
}	t_edge;
