<?php
require_once __DIR__ . '/vendor/autoload.php';

use PhpAmqpLib\Connection\AMQPStreamConnection;

$connection = new AMQPStreamConnection('localhost', 5672, 'guest', 'guest');
$channel = $connection->channel();

$channel->queue_declare('halo', false, false, false, false);

echo "[*] Waiting for message. To exit press CTRL+C\n";

$callback = function ($msg){
    echo ' [x] Received ', $msg->body, "\n";
};

$channel->basic_consume('halo', '', false, true, false, false, $callback);

while(count($channel->callbacks)){
    $channel->wait();
}
?>

    
