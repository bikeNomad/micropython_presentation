# Check for operating system
ifeq ($(OS),Windows_NT)
	HOST_PORT_DIR=ports/windows
	# TODO: Add Windows build directory and instructions
else
	HOST_PORT_DIR=ports/unix
	HOST_BUILD_DIR=build-unix-standard
	HOST_BOARD_DIR=boards/unix-standard
	OSTYPE := $(shell uname -s)
	ifeq ($(OSTYPE),Darwin)
		SHASUM=shasum -a 256 -b
		STATC=stat -f %z
	else
		SHASUM=sha256sum
		STATC=stat -c %s
	endif
endif

# Overrideable variables
# set TOP_DIR to the directory of this Makefile
TOP_DIR ?= $(PWD)
SRC_DIR ?= $(TOP_DIR)/src
MPY_STAGE_DIR ?= $(TOP_DIR)/mpy-stage
SUBMODULES_DIR ?= $(TOP_DIR)/modules
MANIFEST ?= $(TOP_DIR)/manifest.py
UTEMPLATE_DIR ?= $(SUBMODULES_DIR)/utemplate
PORT ?= /dev/ttyACM0
# set V non-zero for verbose build
V ?= 0
PYTHON ?= python

# Check for env variable $IDF_PATH and issue error message if it doesn't exist
ifndef IDF_PATH
$(error IDF_PATH is not set; do "source $(SUBMODULES_DIR)/esp-idf/export.sh" to set it)
endif

# export or set PRE_REPL to run commands before entering the REPL
# for instance, to run the app:
#	export PRE_REPL="exec 'import main'"
# or to run your own code from /my_main.py:
#	export PRE_REPL='exec "import my_main"'
PRE_REPL ?= 

# Variables named the same as in the $(MANIFEST) file
MPY_DIR ?= $(SUBMODULES_DIR)/micropython
MPY_LIB_DIR ?= $(MPY_DIR)/lib/micropython-lib
PORT_DIR ?= $(MPY_DIR)/ports/esp32

# Select the board to build for:
ifdef BOARD_DIR
# Custom board path - remove trailing slash and get the final component of
# the path as the board name.
BOARD = $(notdir $(BOARD_DIR:/=))
else
# If not given on the command line, then default to GENERIC.
BOARD ?= GENERIC
BOARD_DIR ?= $(PORT_DIR)/boards/$(BOARD)
endif

# Set tools paths
MPY_CROSS = $(MPY_DIR)/mpy-cross/build/mpy-cross
MPREMOTE = $(MPY_DIR)/tools/mpremote/mpremote.py
HOST_MICROPYTHON ?= tools/micropython

MPY_MAKE_ARGS=-C $(PORT_DIR) PORT=$(PORT) BOARD_DIR=$(BOARD_DIR) BOARD=$(BOARD) V=$(V)

MPY_CROSS_FLAGS = -march=xtensawin

ROOT_PY_FILES = $(wildcard $(SRC_DIR)/*.py)
SOURCE_PY_FILES = $(wildcard $(SRC_DIR)/**/*.py)
COMPILED_PY_FILES = $(patsubst $(SRC_DIR)/%.py,$(MPY_STAGE_DIR)/%.mpy,$(SOURCE_PY_FILES))

BUILT_HOST_MICROPYTHON = $(MPY_DIR)/$(HOST_PORT_DIR)/$(HOST_BUILD_DIR)/micropython
BOARD_BUILD_DIR=build-$(BOARD)-SPIRAM_OCT
OTA_BINARY=$(PORT_DIR)/$(BOARD_BUILD_DIR)/micropython.bin
FULL_BINARY=$(PORT_DIR)/$(BOARD_BUILD_DIR)/firmware.bin

all:

erase:
	$(MAKE) $(MPY_MAKE_ARGS) erase

flash:
	$(MAKE) $(MPY_MAKE_ARGS) deploy

repl:
	$(MPREMOTE) connect $(PORT) + mount ./src + $(PRE_REPL) + repl

build: install_libs
	$(MAKE) $(MPY_MAKE_ARGS) FROZEN_MANIFEST=$(MANIFEST)

full_build: compile_python $(ROOT_PY_FILES)
	$(MAKE) install_libs
	$(MAKE) $(MPY_MAKE_ARGS) FROZEN_MANIFEST=$(FULL_MANIFEST)

clean: clean_libs clean_mpy
	$(MAKE) $(MPY_MAKE_ARGS) FROZEN_MANIFEST=$(MANIFEST) clean

test:
	$(PYTHON) -B -m unittest discover -s tests

list_boards:
	@echo "**LOCAL:"
	@ls -1 $(TOP_DIR)/boards
	@echo "**PORT_DIR:"
	@find $(PORT_DIR)/boards -mindepth 1 -maxdepth 1 -type d | sed 's#.*/##'

print_environment:
	@echo "OSTYPE: $(OSTYPE)"
	@echo "SHA256SUM: $(SHASUM)"
	@echo "STATC: $(STATC)"
	@echo "TOP_DIR: $(TOP_DIR)"
	@echo "SRC_DIR: $(SRC_DIR)"
	@echo "SUBMODULES_DIR: $(SUBMODULES_DIR)"
	@echo "MODULES_DIR: $(MODULES_DIR)"
	@echo "UTEMPLATE_DIR: $(UTEMPLATE_DIR)"
	@echo "PORT: $(PORT)"
	@echo "BOARD: $(BOARD)"
	@echo "MPY_DIR: $(MPY_DIR)"
	@echo "MPY_LIB_DIR: $(MPY_LIB_DIR)"
	@echo "PORT_DIR: $(PORT_DIR)"
	@echo "BOARD_DIR: $(BOARD_DIR)"
	@echo "COMPILED_TEMPLATES: $(COMPILED_TEMPLATES)"
	@echo "EXPANDED_TEMPLATES: $(EXPANDED_TEMPLATES)"
	@echo "MPY_STAGE_DIR" $(MPY_STAGE_DIR)
	@echo "MANIFEST: $(MANIFEST)"
	@echo "FULL_MANIFEST: $(FULL_MANIFEST)"
	@echo "ROOT_PY_FILES: $(ROOT_PY_FILES)"
	@echo "VARIANT_DIR: $(HOST_BOARD_DIR)"
	@echo "HOST_BUILD_DIR: $(HOST_BUILD_DIR)"
	@echo "BUILT_HOST_MICROPYTHON: $(BUILT_HOST_MICROPYTHON)"
	@echo "BOARD BUILD DIR: $(BOARD_BUILD_DIR)"
	@echo "OTA_BINARY: $(OTA_BINARY)"
	@echo "FULL_BINARY: $(FULL_BINARY)"
	@echo "COMPILED_PY_FILES: $(COMPILED_PY_FILES)"


# list the full and OTA binaries
list_binaries:
	@echo "complete binary with bootloader and partition table:"
	@ls -l $(FULL_BINARY)
	@echo "binary for OTA update:"
	@ls -l $(OTA_BINARY)


# builds tools/micropython for the host system
host_micropython: tools_dir $(HOST_MICROPYTHON)
	
# removes tools/micropython
clean_host_micropython:
	rm -f $(HOST_MICROPYTHON)
	rm -rf $(MPY_DIR)/$(HOST_PORT_DIR)/$(HOST_BUILD_DIR)

tools_dir:
	mkdir -p tools

# Build a local (linux) version of micropython
$(BUILT_HOST_MICROPYTHON):
	$(MAKE) -C $(MPY_DIR)/$(HOST_PORT_DIR) V=$(V) \
		VARIANT_DIR=$(TOP_DIR)/$(HOST_BOARD_DIR) \
		submodules deplibs $(HOST_BUILD_DIR)/micropython

$(HOST_MICROPYTHON): $(BUILT_HOST_MICROPYTHON)
	cp $(BUILT_HOST_MICROPYTHON) $@

# Get copies of microdot, utemplate, and other libraries into $(MODULES_DIR)
get_libs: 
	./copy_files.sh $(MODULES_DIR) $(SUBMODULES_DIR)

clean_libs:
	rm -rf $(MODULES_DIR)

clean_mpy:
	rm -rf $(MPY_STAGE_DIR)
	rm -f $(SRC_DIR)/app/fw_version.py $(SRC_DIR)/app/frozen_res.py

# Copy filesystem with /app/*.mpy files
sync_target_filesystem: clean_mpy compile_python sync datestamp copy_stage_dir

clean_target_filesystem:
	$(MPREMOTE) connect $(PORT) + \
		exec "from upysh import *; \
		rm('/app', True); \
		rm('/lib', True); \
		rm('/boot.py'); rm('/main.py'); rm('/board_type.py')"


help:
	@echo "make all - build, flash, and run REPL"
	@echo "make build - build the firmware"
	@echo "make clean - clean the build"
	@echo "make clean_mpy - clean the micropython files"
	@echo "make clean_host_micropython - clean the host micropython files"
	@echo "make clean_libs - clean the libs"
	@echo "make compile_python - compile the python files"
	@echo "make compile_templates - compile the templates"
	@echo "make erase - erase the flash"
	@echo "make flash - flash the firmware"
	@echo "make host_micropython - build the host micropython"
	@echo "make list_boards - list the boards"
	@echo "make list_binaries - list the binaries"
	@echo "make mpy_cross - build the mpy-cross tool"
	@echo "make print_environment - print the environment"
	@echo "make repl - run the REPL"
	@echo "make sync - sync the filesystem"
	@echo "make sync_target_filesystem - sync the filesystem with .mpy files"

mpy_cross: submodules/micropython
	$(MAKE) -C $(MPY_DIR)/mpy-cross clean
	$(MAKE) -C $(MPY_DIR)/mpy-cross


$(MPY_STAGE_DIR)/%.mpy: $(SRC_DIR)/%.py
	mkdir -p $(dir $@)
	$(MPY_CROSS) $(MPY_CROSS_FLAGS) -o $@ $<


.PHONY: host_micropython install_libs print_environment list_binaries build clean all get_libs \
	compile_python sync sync_target_files sync_target_filesystem clean_target_filesystem \
	erase flash repl clean_mpy clean_libs clean_host_micropython help \
	fw_version_datestamp datestamp copy_stage_dir

