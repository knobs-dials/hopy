Live plotting of data from a USB-enabled HOPI HP-9800 power meter

## Screenshot
![Screenshot](https://raw.githubusercontent.com/scarfboy/hopy/main/screenshots/more.png)


## Acknowledgments
Most lower-level work taken from other similar projects:
- https://github.com/lornix/hopi_hp-9800
- https://gist.github.com/raplin/76da6392f34934738ff865891a7b672f#file-hopi_hp-9800_python_simple-py


## Requirements
- python 3
- pyserial
- matplotlib (unless you're using this only for the readout code)

From scratch, [download and install python 3](https://www.python.org/downloads/) and run:
```
pip3 install pyserial matplotlib
```


## TODO
- command line argument parsing
- figure out port naming and priorities on linux
- see if it makes sense to show both apparent and real power (divide by power factor)
- wrap into executable, so we don't have to require you install python and some packges

CONSIDER
- make the interface connect to devices as you plug them in (also to be able to report, and not just fail silently)
- rewrite it async style?
- fix the CRC code  (right now the check on incoming data is  disabled - I'm not sure whether it's just my HOPI or a general issue)
- web USB version?
