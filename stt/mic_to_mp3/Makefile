EXEC = audiocapture

CLIB = -I./lib/portaudio/include -I./utils -I./lib/libsndfile/include ./lib/portaudio/lib/.libs/libportaudio.a ./lib/libsndfile/src/.libs/libsndfile.so -lrt -lasound -ljack -pthread -lm

$(EXEC): main.cpp utils/utilities.cpp
	g++ -o $@ $^ $(CLIB)

install-deps:
	mkdir -p lib

	curl https://files.portaudio.com/archives/pa_stable_v190700_20210406.tgz | tar -zx -C lib
	cd lib/portaudio && ./configure && $(MAKE) -j

	curl -L https://github.com/libsndfile/libsndfile/archive/refs/tags/1.2.2.tar.gz | tar -zx -C lib
	mv lib/libsndfile-1.2.2 lib/libsndfile
	cd lib/libsndfile && autoreconf -vif && ./configure --enable-werror && $(MAKE) && $(MAKE) check
.PHONY: install-deps

uninstall-deps:
	cd lib/portaudio && $(MAKE) uninstall
	rm -rf lib/portaudio

	cd lib/libsndfile && $(MAKE) uninstall
	rm -rf lib/libsndfile
.PHONY: uninstall-deps

clean: 
	rm -f $(EXEC)
.PHONY: clean