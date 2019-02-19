#!/bin/bash
sudo service rabbitmq-server stop && 
sudo RABBITMQ_NODE_PORT=5672 RABBITMQ_NODENAME=rabbit_0@idelhome rabbitmq-server -detached && 
sudo RABBITMQ_NODE_PORT=5673 RABBITMQ_NODENAME=rabbit_1@idelhome rabbitmq-server -detached && 
sudo RABBITMQ_NODE_PORT=5674 RABBITMQ_NODENAME=rabbit_2@idelhome rabbitmq-server -detached &&

sudo rabbitmqctl -n rabbit_1@idelhome stop_app && 
sudo rabbitmqctl -n rabbit_1@idelhome reset && 
sudo rabbitmqctl -n rabbit_1@idelhome join_cluster rabbit_0@idelhome && 
sudo rabbitmqctl -n rabbit_1@idelhome start_app && 

sudo rabbitmqctl -n rabbit_2@idelhome stop_app && 
sudo rabbitmqctl -n rabbit_2@idelhome reset &&
sudo rabbitmqctl -n rabbit_2@idelhome join_cluster --ram rabbit_0@idelhome && 
sudo rabbitmqctl -n rabbit_2@idelhome start_app && 

sudo rabbitmqctl -n rabbit_0@idelhome cluster_status 