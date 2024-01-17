#include <iostream>
#include <cstring>

#include "utilities.hpp"

void check_error(PaError error){
    if(error != paNoError){
        std::cout << "PortAudio error: " << Pa_GetErrorText(error) << std::endl;
        exit(1);
    }
}

int portaudio_callback(const void* input_buffer,
                              void* output_buffer,
                              unsigned long frames_per_buffer,
                              const PaStreamCallbackTimeInfo* time_info,
                              PaStreamCallbackFlags status_flags,
                              void* user_data)
{
    float* in_buffer = (float*)input_buffer;
    AudioData* audio_data = (AudioData*)user_data;

    // Check if audio_data is nullptr
    if(audio_data == nullptr || audio_data->outfile == nullptr) {
        // Handle the error or return an appropriate value
        std::cout << "PortAudio error: user_data is nullptr." << std::endl;
        exit(EXIT_FAILURE);
        return paAbort;
    }

    SNDFILE* outfile = audio_data->outfile;

    (void)output_buffer;

    if(sf_writef_float(outfile, in_buffer, frames_per_buffer) != frames_per_buffer) {
        // Handle the error or print an error message
        std::cerr << "libsndfile error: Cannot write to the WAV file." << std::endl;
        exit(EXIT_FAILURE);
    }

    sf_writef_float(outfile, in_buffer, frames_per_buffer);

    return paContinue;
}

int check_and_set_device(){
    // Check for microphone devices and print info
    int num_devices = Pa_GetDeviceCount();
    // std::cout << "Number of devices: " << num_devices << std::endl;

    if(num_devices < 0){
        std::cout << "PortAudio error: cannot get device count." << std::endl;
        exit(EXIT_FAILURE);
    }else if(num_devices == 0){
        std::cout << "PortAudio error: no devices found." << std::endl;
        exit(EXIT_SUCCESS);
    }

    const PaDeviceInfo* device_info;

    for(int i=0; i<num_devices; i++){
        device_info = Pa_GetDeviceInfo(i);
        // std::cout << "Device " << i << ": " << device_info->name << std::endl;
        // std::cout << "Max input channels: " << device_info->maxInputChannels << std::endl;
        // std::cout << "Max output channels: " << device_info->maxOutputChannels << std::endl;
        // std::cout << "Default sample rate: " << device_info->defaultSampleRate << "\n" << std::endl;

        if(strcmp(device_info->name, "pulse") == 0){
            return i;
        }
    }

    std::cout << "No pulseaudio device found." << std::endl;
    exit(EXIT_FAILURE);

    return -1;
}