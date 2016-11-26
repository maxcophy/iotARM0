<?php
/**
 * Created by PhpStorm.
 * User: yvtc
 * Date: 2016/10/28
 * Time: 下午 03:04
 */

header("Content-Type: application/json;charset=UTF-8");

$staff = array(
    array('number' => '1020501', 'name' => '王一傑', 'sex' => '男'),
    array('number' => '1020502', 'name' => '王二傑', 'sex' => '男'),
    array('number' => '1020503', 'name' => '王三傑', 'sex' => '男')
);

if($_SERVER['REQUEST_METHOD'] == 'GET'){
    search($staff);
}else if($_SERVER['REQUEST_METHOD'] == 'POST'){
    create();
}

function search($staff){
    if(!isset($_GET['number']) || empty($_GET['number'])){
        echo json_encode(array('msg'=>'沒有輸入員工編號'));

        return;
    }

    for($i=0,$len=count($staff);$i < $len;$i++){
        if($staff[$i]['number'] == $_GET['number']){
            $result = $staff[$i];
        }
    }

    echo isset($result) ? json_encode($result) : json_encode(array('msg'=>'沒有該員工'));
}

function create(){
    if(!isset($_POST['number']) || empty($_POST['number']) ||
        !isset($_POST['name']) || empty($_POST['name']) ||
        !isset($_POST['sex']) || empty($_POST['sex'])){

        echo json_encode(array('msg'=>'員工資料未填寫完全!'));
        return;
    }
    echo json_encode(array('name'=>$_POST['name']));
}