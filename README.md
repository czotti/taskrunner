# Taskrunner

Use redis on localhost to send and receive task.

Far from perfect.

Does not support:

* Working in different directory
* Multiple worker

# Install

Install the redis server on Ubuntu 14.04:

```bash
$ sudo apt-get install redis-server
$ sudo service redis-server restart
```

Install taskrunner:

```bash
$ git clone https://github.com/czotti/taskrunner.git
$ cd taskrunner
$ sudo python3 setup.py install
```


# Run it

Simply go inside your project directory and run:

```bash
taskrunner run your_command parameters1 parameters2
```


