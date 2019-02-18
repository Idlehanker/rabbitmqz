<?php
require '../config.php';
# $channel->exchange_declare('upload-pictures', 'fanout', false, true, false);

$channel->exchange_declare('upload-pictures', 'fanout', false, true, false);
$channel->queue_declare('resize-piture', false, true, false, false);
$channel->queue_bind('resize-piture', 'upload-pictures');

$consumer_callback = function($msg){
    echo 'command:%s',$msg->body; 
    if ($msg->body == 'quit'){
        $msg->delivery_info['channel']->
            basic_cancel($msg->delivery_info['consumer_tag']);
    }

    $meta = json_decode($msg->body, true);
    resize_picture($meta['image_id'],  $meta['image_path']);

    $msg->delivery_info['channel']
            ->basic_ack($msg
                ->delivery_info['delivery_tag']);

    echo ' [x] Receive ', $meta, '\n';
};

function resize_picture($image_id, $image_path){
    echo sprintf("Resizing picture: %s %s\n", $image_id, $image_path);
}

$channel->basic_consume('resize-piture',
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