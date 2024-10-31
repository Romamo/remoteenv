# remote-env

[![GitHub license](https://img.shields.io/github/license/Romamo/remote-env)](

Use remote environment variables

## Description


## Prerequisites


## Install

```bash
pip install git+https://github.com/Romamo/remote-env.git
```
## Usage

```python
from zoo import ZooEnv

zooenv = ZooEnv('prefix', 'zoohost:2181')
zooenv.start()

zooenv.read('mod', 'host1', 'mod/host1')
```
