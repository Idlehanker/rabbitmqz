<?php
require '../config.php';
# $channel->exchange_declare('upload-pictures', 'fanout', false, true, false);

$channel->exchange_declare('upload-pictures', 'fanout', false, true, false);
$channel->queue_declare('add-points', false, true, false, false);
$channel->queue_bind('add-points', 'upload-pictures');

$consumer_callback = function($msg){
    echo 'command:%s',$msg->body; 
    if ($msg->body == 'quit'){
        $msg->delivery_info['channel']->
            basic_cancel($msg->delivery_info['consumer_tag']);
    }

    $meta = json_decode($msg->body, true);
    $msg->delivery_info['channel']
            ->basic_ack($msg
                ->delivery_info['delivery_tag']);

    echo ' [x] Receive ', $meta, '\n';
};

$channel->basic_consume('add-points',
                        '',
                        false,
                        false,
                        false,
                        false,
                        $consumer_callback);

while(count($channel->callbacks)){
    $channel->wait();
}

$channel->close();
$connection->close();

?>