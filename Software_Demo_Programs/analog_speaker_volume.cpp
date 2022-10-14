#include "mbed.h"
PwmOut myled(LED1);
AnalogIn mypotentiometer(p20);
int main()
{
    while(1) {
        float scale = mypotentiometer.read();
        printf("VOLUME SCALE: %lf\n\r", scale);
        myled = mypotentiometer;
        wait(0.1);
    }
}
