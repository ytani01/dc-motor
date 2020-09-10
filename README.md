# 

DCモーター・ライブラリ

## 1. install

### 1.1 create python3 venv

```bash
$ cd ~
$ python3 -m venv env1
```

### 1.2 activate venv

```bash
$ . ~/env1/bin/activate
(env1)$ 
```

### 1.3 download

```bash
(env1)$ cd ~/env1
(env1)$ git clone https://www.github.com/ytani01/dc-motor.github
```

### 1.4 install python packages

```bash
(env1)$ cd ~/env1/dc-motor
(env1)$ pip3 install -r requirements.txt
```


## 2. Example

see usage as follows:
```bash
$ sudo pigpiod
$ ./sample1.py -h
```
