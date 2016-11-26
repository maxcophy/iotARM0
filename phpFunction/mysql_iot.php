<?php
/**
 * Created by PhpStorm.
 * User: yvtc
 * Date: 2016/10/27
 * Time: 上午 10:53
 */
$host = '192.168.58.15';
$dbname = 'iot';
$user = 'root';
$passwd = 'aa123123';

try {
    $dbh = new PDO("mysql:host=$host;dbname=$dbname", $user, $passwd);
    $dbh->exec("set names utf8");
    $res = $dbh->query("SELECT * FROM `action`");
    $res = $res->fetch();

} catch (PDOException $e) {
    print "Error!: " . $e->getMessage() . "<br/>";
    die();
}


switch ($_GET['method']) {
    case 'follow':
        $sql = "UPDATE `action` SET `isTrace` = 1 WHERE `action`.`id` = 1";
        $dbh->query($sql);
        break;
    case 'up':
        $sql = "UPDATE `action` SET `movY` = IF(`movY` < 10 ,`movY`+1,`movY`) ,`isXMov`=1 WHERE `action`.`id` = 1";
        $dbh->query($sql);
        break;
    case 'down':
        $sql = "UPDATE `action` SET `movY` = IF(`movY` > -10 ,`movY`-1,`movY`),`isXMov`=1 WHERE `action`.`id` = 1";
        $dbh->query($sql);
        break;
    case 'left':
        $sql = "UPDATE `action` SET `movX` = IF(`movX` > -10 ,`movX`-1,`movX`),`isYMov`=1 WHERE `action`.`id` = 1";
        $dbh->query($sql);
        break;
    case 'right':
        $sql = "UPDATE `action` SET `movX` = IF(`movX` < 10 ,`movX`+1,`movX`) ,`isYMov`=1 WHERE `action`.`id` = 1";
        $dbh->query($sql);
        break;
}
$res2 = $dbh->query("SELECT * FROM `action`");

echo json_encode(array('result' => 'ok', 'sql' => $res2->fetch()));

$dbh = null;