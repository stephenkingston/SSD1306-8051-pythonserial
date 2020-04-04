MAKE_HEX = packihx
CC = sdcc
BIN_TOOL = makebin

OUTPUT = SSD1306_UART

SRCS += main.c \
		include/g_lcd.c \
		include/8051_UART.c \

INCLUDE += include

CFLAGS += -mmcs51 -c --std-sdcc99
BUILD_DIR = build
BIN_DIR = bin

C_FILES = $(notdir $(SRCS))
C_PATHS = $(dir $(SRCS))
vpath %.c $(C_PATHS)
OBJS = $(addprefix $(BUILD_DIR)/, $(C_FILES:.c=.rel))

IHX = $(BUILD_DIR)/$(OUTPUT).ihx

HEX = $(BIN_DIR)/$(OUTPUT).hex
BIN = $(BIN_DIR)/$(OUTPUT).bin


####### TARGETS ########

all: $(HEX) $(IHX) $(BIN) $(BUILD_DIR)

$(BIN_DIR):
	@mkdir "$@"

$(BIN): $(HEX)
	$(BIN_TOOL) -p "$<" "$@"

$(HEX): $(IHX)
	@$(MAKE_HEX) "$<" > "$@"

$(BUILD_DIR):
	@mkdir "$@"

$(IHX): $(BUILD_DIR) $(OBJS)
	@$(CC) -o $@ $(OBJS)

$(BUILD_DIR)/%.rel: %.c
	@$(CC) $(CFLAGS) $(addprefix -I,$(INCLUDE)) -o "$@" "$<"
	
clean:
	rm -rf $(BUILD_DIR) *.lst *.rst *.rel *.bin *.hex