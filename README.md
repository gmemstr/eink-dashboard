E-Ink Dashboard
===

Experimental dashboard for the [Waveshare 2in13_V2](https://www.waveshare.com/wiki/2.13inch_e-Paper_HAT)
e-ink/e-paper display.

Requires `PIL` and `spidev`

This application is two parts; a client (with a fallback) and a server, which
the client will reach out to expecting an image to display. Dependencies are 
kept to a minimum where possible, so running should be as simple as installing
the mentioned libraries then running 
`python client/main.py http://<desktop ip address>/generate_clock` on the Pi 
Zero and `python server/main.py` on your desktop.

[Read more about it](https://dev.to/gmemstr/tiny-eink-dashboard-29a4)