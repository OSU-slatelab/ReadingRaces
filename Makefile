INCS=`pkg-config --cflags --libs pocketsphinx sphinxbase`
PYTHON=/usr/include/python2.7
BOOST=/home/meghan/Documents/boost_1_62_0
DEFS=-DMODELDIR=\"`pkg-config --variable=modeldir pocketsphinx`\"

#hello_ps: hello_ps.cpp
#	g++ -fpic -c -o hello_ps.o hello_ps.cpp $(DEFS) $(INCS) -I $(PYTHON) -I $(BOOST) 
#	g++ -o hello_ps.so -shared hello_ps.o -lboost_python -lpython2.7

hello_ps.so: hello_ps.cpp
	g++ -fPIC -c -o hello_ps.o hello_ps.cpp $(DEFS) $(INCS) -I $(PYTHON) -I $(BOOST)
	g++ -o hello_ps.so -shared hello_ps.o $(DEFS) $(INCS) -lboost_python -lpython2.7

n_best.so: n_best.cpp
	g++ -fPIC -c -o n_best.o n_best.cpp $(DEFS) $(INCS) -I $(PYTHON) -I $(BOOST)
	g++ -o n_best.so -shared n_best.o $(DEFS) $(INCS) -lboost_python -lpython2.7
