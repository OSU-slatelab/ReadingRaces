#include <pocketsphinx.h>
#include <stdio.h>
#include <string.h>
#include <vector>
#include <iostream>
#include <boost/python.hpp>
#include <Python.h>
#include <boost/python/suite/indexing/vector_indexing_suite.hpp>

using namespace boost::python;

class PocketSphinxWrapper
{
    private:
        int n;
        int ptr;
        std::string audio; // "computer-generated-16k.wav"
        std::string jsgf; // "hypotheses.jsgf"
        std::string hmm;
        std::string lm;
        std::string dict;
        std::vector<std::string> hyps;
        std::vector<int32> scores;
        std::vector<std::string> call_nbest(int);
    public:
        PocketSphinxWrapper(int num, std::string audio_path, std::string jsgf_path) {
            n = num;
            audio = audio_path;
            jsgf = jsgf_path;
            hmm = MODELDIR "/en-us/en-us";
            lm = MODELDIR "/en-us/en-us-phone.lm.bin";
            dict = "resources/phone.dict";
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
        std::vector<std::string> getList() {return hyps; }
        std::vector<int32> getScores() {return scores; }
};


std::vector<std::string> PocketSphinxWrapper::call_nbest(int n)
{
    ps_decoder_t *ps = NULL;
    cmd_ln_t *config = NULL;
    ps_nbest_t *nbest;
    FILE *fh;
    std::vector<std::string> hyps;

    if (!jsgf.empty()) {
        config = cmd_ln_init(NULL, ps_args(), TRUE,
            "-jsgf", jsgf.c_str(), 
            "-hmm", hmm.c_str(),
            "-dict", dict.c_str(),
            "-beam", "1e-20",
            "-pbeam", "1e-20",	// Beam width applied to phone transitions, def 1e-48
            "-lw", "2.0",		// Language model probability weight, def 6.5
            "-logfn", "log.log",
            NULL);
    } else {
        config = cmd_ln_init(NULL, ps_args(), TRUE,
            "-hmm", hmm.c_str(),
            "-allphone", lm.c_str(),
            "-beam", "1e-20",
            "-pbeam", "1e-20",
            "-lw", "2.0",
            "-logfn", "log.log",
            NULL);
    }
 
    if (config == NULL) {
        fprintf(stderr, "Failed to create config object, see log for details\n");
        return hyps;
    }

    ps = ps_init(config);
    if (ps == NULL) {
        fprintf(stderr, "Failed to create recognizer, see log for details\n");
        return hyps;
    }

    fh = fopen(audio.c_str(), "rb");
    if (fh == NULL) {
        fprintf(stderr, "Unable to open input file %s\n", audio.c_str());
        return hyps;
    }

    ps_decode_raw(ps, fh, -1);
    fclose(fh);

    int32 score, i;
    char const *hyp = ps_get_hyp(ps, &score);
    hyps.push_back(std::string(hyp, 0, 100));
    //fprintf(stdout, "Score value %d\n", score);
    scores.push_back(score);

    for (i = 1, nbest = ps_nbest(ps); nbest && i < n; nbest = ps_nbest_next(nbest), i++) {
        hyp = ps_nbest_hyp(nbest, &score);
        hyps.push_back(std::string(hyp, 0, 100));
        scores.push_back(score);
    }
    if (nbest)
        ps_nbest_free(nbest);

    ps_free(ps);
    cmd_ln_free_r(config);

    return hyps;
}

BOOST_PYTHON_MODULE(pocketsphinx_wrapper)
{
    class_<std::vector<std::string> >("StringVec")
        .def(vector_indexing_suite<std::vector<std::string> >() );
    class_<std::vector<int32> >("IntVec")
        .def(vector_indexing_suite<std::vector<int32> >() );

    class_<PocketSphinxWrapper>("PocketSphinxWrapper", init<int, std::string, std::string>())
        .def("hasNext", &PocketSphinxWrapper::hasNext)
        .def("next", &PocketSphinxWrapper::next)
        .def("reset", &PocketSphinxWrapper::reset)
        .def("getList", &PocketSphinxWrapper::getList)
        .def("getScores", &PocketSphinxWrapper::getScores)
    ; 
}
