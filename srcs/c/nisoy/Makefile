NAME		:= nisoy
BUILD_DIR	:= .build
INCS_DIRS	:= includes ../nauty
SRCS_DIR	:= srcs
CC			:= gcc
CFLAGS		:= -Wall -Wextra -MMD -MP $(foreach dir,$(INCS_DIRS),-I $(dir))
LDFLAGS		:= ../nauty/nauty.a
SRCS_EXT	:= .c
SRCS		:= $(wildcard $(SRCS_DIR)/*$(SRCS_EXT))
OBJS_EXT	:= .o
OBJS		:= $(SRCS:$(SRCS_DIR)/%$(SRCS_EXT)=$(BUILD_DIR)/%$(OBJS_EXT))

all: $(NAME)

$(NAME): $(OBJS)
	$(CC) $(CFLAGS) -o $@ $^ $(LDFLAGS)

clean:
	rm -rf $(NAME) $(BUILD_DIR)

run: $(NAME)
	./$< ../../../data/molecules/7.txt

$(BUILD_DIR):
	mkdir $@

$(BUILD_DIR)/%$(OBJS_EXT): $(SRCS_DIR)/%$(SRCS_EXT) | $(BUILD_DIR)
	$(CC) $(CFLAGS) -c $< -o $@

-include $(OBJS:%$(OBJS_EXT)=%.d)

.PHONY: all clean run
