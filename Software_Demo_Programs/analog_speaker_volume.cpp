#include "mbed.h"
PwmOut myled(LED1);
AnalogIn mypotentiometer(p20);
Serial pc(USBTX, USBRX); // tx, rx

int main()
{
    while(1) {
        float scale = mypotentiometer.read();
        int percent = int(scale * 100);

        pc.printf("%d\n", percent);
        myled = mypotentiometer;
        
        wait(0.1);
    }
}

