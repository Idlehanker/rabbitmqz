#!/bin/bash
# sudo brew services stop rabbitmq && 
sudo RABBITMQ_NODE_PORT=5672 RABBITMQ_NODENAME=rabbit_0@idelhost rabbitmq-server -detached && 
sudo RABBITMQ_NODE_PORT=5673 RABBITMQ_NODENAME=rabbit_1@idelhost rabbitmq-server -detached && 
sudo RABBITMQ_NODE_PORT=5674 RABBITMQ_NODENAME=rabbit_2@idelhost rabbitmq-server -detached &&

sudo rabbitmqctl -n rabbit_1@idelhost stop_app && 
sudo rabbitmqctl -n rabbit_1@idelhost reset && 
sudo rabbitmqctl -n rabbit_1@idelhost join_cluster rabbit_0@idelhost && 
sudo rabbitmqctl -n rabbit_1@idelhost start_app && 

sudo rabbitmqctl -n rabbit_2@idelhost stop_app && 
sudo rabbitmqctl -n rabbit_2@idelhost reset &&
sudo rabbitmqctl -n rabbit_2@idelhost join_cluster --ram rabbit_0@idelhost && 
sudo rabbitmqctl -n rabbit_2@idelhost start_app && 

sudo rabbitmqctl -n rabbit_0@idelhost cluster_status 
