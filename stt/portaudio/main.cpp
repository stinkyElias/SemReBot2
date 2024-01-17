#include <stdlib.h>
#include <stdio.h>
#include <portaudio.h>

#include <cstring>
#include <iostream>

#define SAMPLE_RATE 44100
#define FRAMES_PER_BUFFER 512 // Lavere buffere gir raskere display speed

static void check_error(PaError error){
    if(error != paNoError){
        std::cout << "PortAudio error: " << Pa_GetErrorText(error) << std::endl;
        exit(EXIT_FAILURE);
    }
}

static inline float max(float a, float b){
    return a > b ? a: b;
}

static int pa_test_callback(const void* input_buffer,
                            void* output_buffer,
                            unsigned long frames_per_buffer,
                            const PaStreamCallbackTimeInfo* time_info,
                            PaStreamCallbackFlags status_flags,
                            void* user_data)
{
    float* in_buffer = (float*)input_buffer;
    (void)output_buffer;

    int display_size = 100;
    std::cout << "\r";

    float volume_left = 0;
    float volume_right = 0;

    for(unsigned long i=0; i<frames_per_buffer*2; i+=2){
        volume_left = max(volume_left, std::abs(in_buffer[i]));
        volume_right = max(volume_right, std::abs(in_buffer[i+1]));
    }

    for(int i=0; i<display_size; i++){
        float bar_proportion = i / (float)display_size;

        if(bar_proportion <= volume_left && bar_proportion <= volume_right){
            std::cout << "█";
        }else if(bar_proportion <= volume_left){
            std::cout << "▀";
        }else if(bar_proportion <= volume_right){
            std::cout << "▄";
        }else{
            std::cout << " ";
        }
    }
    std::cout.flush();

    return EXIT_SUCCESS;
}

int main(){
    PaError error;
    error = Pa_Initialize();
    check_error(error);
    
    int num_devices = Pa_GetDeviceCount();
    std::cout << "Number of devices: " << num_devices << std::endl;

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
        std::cout << "Device " << i << ": " << device_info->name << std::endl;
        std::cout << "Max input channels: " << device_info->maxInputChannels << std::endl;
        std::cout << "Max output channels: " << device_info->maxOutputChannels << std::endl;
        std::cout << "Default sample rate: " << device_info->defaultSampleRate << "\n" << std::endl;
    }

    int device = 7;

    PaStreamParameters input_parameters;
    PaStreamParameters output_parameters;

    memset(&input_parameters, 0, sizeof(input_parameters));
    input_parameters.channelCount = 2;
    input_parameters.device = device;
    input_parameters.hostApiSpecificStreamInfo = NULL;
    input_parameters.sampleFormat = paFloat32;
    input_parameters.suggestedLatency = Pa_GetDeviceInfo(device)->defaultLowInputLatency;

    memset(&output_parameters, 0, sizeof(output_parameters));
    output_parameters.channelCount = 2;
    output_parameters.device = device;
    output_parameters.hostApiSpecificStreamInfo = NULL;
    output_parameters.sampleFormat = paFloat32;
    output_parameters.suggestedLatency = Pa_GetDeviceInfo(device)->defaultLowInputLatency;

    PaStream* stream;
    error = Pa_OpenStream(&stream,
                          &input_parameters,
                          &output_parameters,
                          SAMPLE_RATE,
                          FRAMES_PER_BUFFER,
                          paNoFlag,
                          pa_test_callback,
                          NULL
    );
    check_error(error);

    error = Pa_StartStream(stream);
    check_error(error);

    Pa_Sleep(10*1000);

    error = Pa_StopStream(stream);
    check_error(error);

    error = Pa_CloseStream(stream);
    check_error(error);


    error = Pa_Terminate();
    check_error(error);

    return EXIT_SUCCESS;
}