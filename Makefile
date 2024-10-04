CC=gcc
CFLAGS=-O2 -Wall -Wextra -Werror


ifeq ($(PREFIX),)
    PREFIX := /usr/local
endif


.PHONY: all install uninstall clean

all: safe

install: safe
	install -m 755 safe $(PREFIX)/bin/

uninstall: safe
	rm -f $(PREFIX)/bin/safe

clean:
	rm -f safe


safe: main.c
	$(CC) -o $@ $^
