<?php
$host = '192.168.43.20';
$dbname = 'iot';
$user = 'root';
$passwd = 'aa123123';

try {
    $dbh = new PDO("mysql:host=$host;dbname=$dbname", $user, $passwd);
    $dbh->exec("set names utf8");

} catch (PDOException $e) {
    print "Error!: " . $e->getMessage() . "<br/>";
    die();
}

switch ($_GET['move']) {
    case 'up':
        $sql = "UPDATE `action` SET `movY` = IF(`movY` < 10 ,`movY`+0.5,`movY`) WHERE `action`.`id` = 1";
        $dbh->query($sql);
        break;
    case 'down':
        $sql = "UPDATE `action` SET `movY` = IF(`movY` > -10 ,`movY`-0.5,`movY`) WHERE `action`.`id` = 1";
        $dbh->query($sql);
        break;
    case 'left':
        $sql = "UPDATE `action` SET `movX` = IF(`movX` > -10,`movX`-0.5,`movX`) WHERE `action`.`id` = 1";
        $dbh->query($sql);
        break;
    case 'right':
        $sql = "UPDATE `action` SET `movX` = IF(`movX` < 10,`movX`+0.5,`movX`) WHERE `action`.`id` = 1";
        $dbh->query($sql);
        break;
    case 'web':
        $sql = "UPDATE `action` SET `isMov` = '0', `isXMov` = '0', `isYMov` = '0' WHERE `action`.`id` = 1";
        $dbh->query($sql);
        break;
}

//echo json_encode(array('result' => 'ok', 'sql' => $res2->fetch()));

$dbh = null;
