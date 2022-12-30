NAME		:= libnauty.a
BUILD_DIR	:= .build
INCS_DIR	:= includes
SRCS_DIR	:= srcs
CC			:= gcc
CFLAGS		:= -Wall -Wextra -O2 -DNDEBUG -MMD -MP -I $(INCS_DIR)
SRCS_EXT	:= .c
SRCS		:= $(wildcard $(SRCS_DIR)/*$(SRCS_EXT))
OBJS_EXT	:= .o
OBJS		:= $(SRC:$(SRCS_DIR)/%$(SRCS_EXT)=$(BUILD_DIR)/%$(OBJS_EXT))

all: $(NAME)

$(NAME): $(OBJS)
	ar -rcs $@ $^

clean:
	rm -rf $(NAME)

test:

$(BUILD_DIR):
	mkdir $@

$(BUILD_DIR)/%$(OBJS_EXT): $(SRCS_DIR)/%$(SRCS_EXT) | $(BUILD_DIR)
	$(CC) $(CFLAGS) -c $< -o $@

-include $(OBJS:%$(OBJS_EXT)=%.d)

.PHONY: all clean test
