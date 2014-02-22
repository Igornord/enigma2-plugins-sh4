installdir = $(libdir)/enigma2/python/Plugins/Extensions/DuckBA/bin
install_DATA = *.txt *.sh *.spark *.spark7162 fw_setenv nandwrite flash_erase 
install-data-hook:
	chmod 0755 $(DESTDIR)$(libdir)/enigma2/python/Plugins/Extensions/DuckBA/bin/*.sh \
	$(DESTDIR)$(libdir)/enigma2/python/Plugins/Extensions/DuckBA/bin/flash_erase \
	$(DESTDIR)$(libdir)/enigma2/python/Plugins/Extensions/DuckBA/bin/fw_setenv \
	$(DESTDIR)$(libdir)/enigma2/python/Plugins/Extensions/DuckBA/bin/nandwrite
