INCS=`pkg-config --cflags --libs pocketsphinx sphinxbase`
PYTHON=/usr/include/python2.7
BOOST=/home/meghan/Documents/boost_1_62_0
DEFS=-DMODELDIR=\"`pkg-config --variable=modeldir pocketsphinx`\"

n_best.so: n_best.cpp
	g++ -fPIC -c -o n_best.o n_best.cpp $(DEFS) $(INCS) -I $(PYTHON) -I $(BOOST)
	g++ -o n_best.so -shared n_best.o $(DEFS) $(INCS) -lboost_python -lpython2.7
