# Zenoh apps

This is mainly for testing and getting used to the terminology used in Zenoh. What I have learnt so far,

* `path` is the counterpart of `topic` in ROS/ROS2
* `selector` is what I would consider the namespace of the topics involved, a listener to the selector `/example/**` will pick up messages from paths like `/example/path1`, `/example/path2`, etc
* `locator` is used to target a particular `Zenoh` session on the network, if it is `None`, dynamic discovery is used, however I have not managed to get it working in a distributed manner yet, I believe dynamic discovery might only be best for same-machine transmission between apps.

## Setup

Installation and setup should be done for both servers and clients,

```bash
# install zenoh
echo "deb [trusted=yes] http://pkgs.adlink-labs.tech/debian/18.04 ./" | sudo tee -a /etc/apt/sources.list > /dev/null
sudo apt update && sudo apt install zenoh

# install the python SDK and its dependencies
pip3 install scikit-build cmake eclipse-zenoh

# pull in the repository to get access to the examples
git clone https://github.com/eclipse-zenoh/zenoh-python
```

## Distributed tests

Some of the tests and examples I followed the examples of 

Start the server on the main/server work station,

```bash
zenohd --verbose
```

At the same time, check the main/server work station's IP address using `ip a`, assuming it is `SESSION_IP`.

Start a subscription for a simple throughput test on the server, note that we are not specifying the `locator` as we are running the subscription on the same machine as the active `Zenoh` session, hence dynamic discovery will do just fine.

```bash
cd zenoh-python/examples/zenoh-net
python3 zn_sub_thr.py --path "/example/chatter"
```

On the other/client work station, start the publisher for the throughput test, this time we need to specify the `locator`, otherwise it will not find any active `Zenoh` session,

```bash
cd zenoh-python/examples/zenoh-net
python3 zn_pub_thr.py --size 70 --locator SESSION_IP --path "/example/chatter"
```

The subscription-side should start printing the rate of which messages are received, like so,

```bash
86199.539867 msgs/sec
89812.722511 msgs/sec
88794.963550 msgs/sec
85926.967233 msgs/sec
91303.605488 msgs/sec
91984.811468 msgs/sec
90945.055545 msgs/sec
```
