#include <pocketsphinx.h>
#include <stdio.h>
#include <string.h>
#include <vector>
#include <iostream>
#include <boost/python.hpp>
#include <Python.h>
#include <boost/python/suite/indexing/vector_indexing_suite.hpp>

using namespace boost::python;

class NBest
{
    private:
        int n;
        int ptr;
        std::vector<std::string> hyps;
        std::vector<std::string> call_nbest(int);
    public:
        NBest(int num) {
            n = num; 
            ptr = 0;
            hyps = call_nbest(n);
        }
        bool hasNext() { return (ptr < n); }
        std::string next() {
            std::string val = hyps.at(ptr);
            ptr++;
            return val;
        }
        void reset() {ptr = 0;}
        std::vector<std::string> getList() { return hyps; }
};

std::vector<std::string> NBest::call_nbest(int n)
{
    ps_decoder_t *ps = NULL;
    cmd_ln_t *config = NULL;
    ps_nbest_t *nbest;
    FILE *fh;
    std::vector<std::string> hyps;

    config = cmd_ln_init(NULL, ps_args(), TRUE,
        "-jsgf", "hypotheses.jsgf", 
        "-hmm", MODELDIR "/en-us/en-us",
        "-dict", "phone.dict",
        "-beam", "1e-20",
        "-pbeam", "1e-20",
        "-lw", "2.0",
        "-logfn", "log.log",
        NULL);
    if (config == NULL) {
        fprintf(stderr, "Failed to create config object, see log for details\n");
        return hyps;
    }

    ps = ps_init(config);
    if (ps == NULL) {
        fprintf(stderr, "Failed to create recognizer, see log for details\n");
        return hyps;
    }

    printf("Search type: %s\n", ps_get_search(ps));

    fh = fopen("computer-generated-16k.wav", "rb");
    if (fh == NULL) {
        fprintf(stderr, "Unable to open input file computer-generated-16k.wav\n");
        return hyps;
    }

    ps_decode_raw(ps, fh, -1);
    fclose(fh);

    int32 score, i;
    char const *hyp = ps_get_hyp(ps, &score);
    hyps.push_back(std::string(hyp, 0, 100));
    std::cout << "NBEST 0: " << hyps.at(0) << std::endl;

    for (i = 1, nbest = ps_nbest(ps); nbest && i < n; nbest = ps_nbest_next(nbest), i++) {
        hyp = ps_nbest_hyp(nbest, &score);
        hyps.push_back(std::string(hyp, 0, 100));
        std::cout << "NBEST " << i << ": " << hyps.at(i) << std::endl;
    }
    if (nbest)
        ps_nbest_free(nbest);

    ps_free(ps);
    cmd_ln_free_r(config);

    return hyps;
}

BOOST_PYTHON_MODULE(n_best)
{
    class_<std::vector<std::string> >("StringVec")
        .def(vector_indexing_suite<std::vector<std::string> >() );

    class_<NBest>("NBest", init<int>())
        .def("hasNext", &NBest::hasNext)
        .def("next", &NBest::next)
        .def("reset", &NBest::reset)
        .def("getList", &NBest::getList)
    ; 
}
