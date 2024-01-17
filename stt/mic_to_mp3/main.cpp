#include <cstring>
#include <iostream>
#include <stdlib.h>
#include <stdio.h>
#include "utilities.hpp"

#define SAMPLE_RATE 44100
#define FRAMES_PER_BUFFER 512 // Lavere buffere gir raskere display speed

int main(){
    // Initialize PortAudio
    PaError error;
    error = Pa_Initialize();

    int device = check_and_set_device(); // 7

    PaStreamParameters input_parameters;

    memset(&input_parameters, 0, sizeof(input_parameters)); // Set all bytes to 0
    input_parameters.channelCount = 1;
    input_parameters.device = device;
    input_parameters.hostApiSpecificStreamInfo = nullptr;
    input_parameters.sampleFormat = paFloat32;

    // Check that device index is valid before setting suggested latency to default
    const PaDeviceInfo* device_info = Pa_GetDeviceInfo(device);
    if(device_info == nullptr){
        std::cout << "PortAudio error: Invalid device index." << std::endl;
        exit(EXIT_FAILURE);
    }
    input_parameters.suggestedLatency = device_info->defaultLowInputLatency;

    SF_INFO sfinfo;
    sfinfo.channels = 1;    // mono
    sfinfo.samplerate = SAMPLE_RATE;
    sfinfo.format = SF_FORMAT_WAV | SF_FORMAT_FLOAT; // 32-bit float samples

    SNDFILE* outfile = sf_open("test.wav", SFM_WRITE, &sfinfo);

    if(!outfile){
        std::cout << "libsndfile error: cannot open output file." << std::endl;
        exit(EXIT_FAILURE);
    }

    AudioData audio_data;
    audio_data.outfile = outfile;

    PaStream* stream;
    error = Pa_OpenStream(&stream,
                          &input_parameters,
                          nullptr,  // no output
                          SAMPLE_RATE,
                          FRAMES_PER_BUFFER,
                          paNoFlag,
                          portaudio_callback,
                          &audio_data);

    check_error(error);

    error = Pa_StartStream(stream);
    check_error(error);

    Pa_Sleep(3 * 1000); // Record for 3 seconds

    error = Pa_StopStream(stream);
    check_error(error);

    // Close WAV file after stopping the stream
    sf_close(outfile);

    return EXIT_SUCCESS;
}