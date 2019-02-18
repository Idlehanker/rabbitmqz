<?php
require '../config.php';
use PhpAmqpLib\Message\AMQPMessage;

$channel->exchange_declare('upload-pictures', 
                            'fanout',
                            false,
                            true,
                            false);

$image_id = $argv[1];
$user_id = $argv[2];
$image_path = $argv[3];

$metadata = json_encode(array(
    'image_id' => $image_id,
    'user_id' => $user_id,
    'image_path' => $image_path
));

$msg = new AMQPMessage($metadata, array(
    'content_type' => 'application/json',
    'delivery_mode' => 2
));

$channel->basic_publish($msg, 'upload-pictures');
$channel->close();
$connection->close();

?>
