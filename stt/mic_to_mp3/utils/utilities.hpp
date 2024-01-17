#ifndef UTILITIES_HPP
#define UTILITIES_HPP

#include <portaudio.h>
#include <sndfile.h>

struct AudioData{
    SNDFILE* outfile;
};

void check_error(PaError error);
int portaudio_callback(const void* input_buffer,
                              void* output_buffer,
                              unsigned long frames_per_buffer,
                              const PaStreamCallbackTimeInfo* time_info,
                              PaStreamCallbackFlags status_flags,
                              void* user_data);

int check_and_set_device();


#endif // UTILITIES_HPP