PROJECT_ROOT=/home/meghan/Documents/rr/add_story
PYTHON=/usr/include/python2.7
BOOST=/home/meghan/Documents/boost_1_62_0
INCS_PS=`pkg-config --cflags --libs pocketsphinx sphinxbase`
DEFS_PS=-DMODELDIR=\"`pkg-config --variable=modeldir pocketsphinx`\"

pocketsphinx_wrapper.so: pocketsphinx_wrapper.cpp
	g++ -fPIC -c -o pocketsphinx_wrapper.o pocketsphinx_wrapper.cpp $(DEFS_PS) $(INCS_PS) -I $(PYTHON) -I $(BOOST)
	g++ -o pocketsphinx_wrapper.so -shared pocketsphinx_wrapper.o $(DEFS_PS) $(INCS_PS) -lboost_python -lpython2.7
