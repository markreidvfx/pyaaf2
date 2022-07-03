all: classdefs.py typedefs.py

classdefs.py: classdefs_gen
	./classdefs_gen > classdefs.py
	cp -v classdefs.py ../../src/aaf2/model/

classdefs_gen: classdefs_gen.cpp typedefs_names.h
	g++ classdefs_gen.cpp -o classdefs_gen

typedefs.py: typedefs_gen
	./typedefs_gen > typedefs.py
	cp -v typedefs.py ../../src/aaf2/model/

typedefs_gen: typedefs_gen.cpp typedefs_names.h
	g++ typedefs_gen.cpp -o typedefs_gen

clean:
	rm classdefs_gen typedefs_gen datadefs_gen classdefs.py typedefs.py datadefs.py
