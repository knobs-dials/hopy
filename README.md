# hopy
Live plotting of data from a USB-enabled HOPI HP-9800 power meter

## screenshot
![Screenshot](https://raw.githubusercontent.com/scarfboy/hopy/main/screenshots/more.png)


## Acknowledgments
Most work taken from other similar projects:
- https://github.com/lornix/hopi_hp-9800
- https://gist.github.com/raplin/76da6392f34934738ff865891a7b672f#file-hopi_hp-9800_python_simple-py


## Requirements

for hopy.py, which is just the readout, you will need to install pyserial

for hopi_plot.py, which uses that to draw the last few minutes of data, you will need to install matplotlib

So probably:
```
pip3 install pyserial matplotlib
```


## TODO
- See if it makes sense to show both apparent and real power

- don't assume 230V 50Hz

- rewrite it async style?
