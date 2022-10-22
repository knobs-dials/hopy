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

So probably:
```
pip3 install pyserial matplotlib
```


## TODO /  CONSIDER
- add date-and-time to axis

- fix the CRC code  (right now the check is disabled)

- command line arguments parsing

- add separate script to log data

- test on linux

- See if it makes sense to show both apparent and real power

- rewrite it async style?
