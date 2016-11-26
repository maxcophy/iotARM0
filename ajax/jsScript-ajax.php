<!doctype html>
<html lang="zh-hant">
<head>
    <meta charset="UTF-8">
    <meta name="viewport"
          content="width=device-width, user-scalable=no, initial-scale=1.0, maximum-scale=1.0, minimum-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="ie=edge">
    <title>Document</title>
</head>
<body>
<h1>查詢員工</h1>
<label for="keyword">請輸入員工編號：</label>
<input type="text" id="keyword">

<button id="search">查詢</button>
<p id="searchResult"></p>

<h1>新建員工</h1>
<label for="staffNumber">請輸入員工編號：</label>
<input type="text" id="staffNumber"><br>

<label for="staffName">請輸入員工姓名：</label>
<input type="text" id="staffName"><br>

<label for="staffSex">請輸入員工性別：</label>
<select id="staffSex">
    <option value="男">男</option>
    <option value="女">女</option>
</select><br>

<button id="save">保存</button>
<p id="createResult"></p>
<script type="text/javascript">
    document.getElementById('search').onclick = function(){
        var request = new XMLHttpRequest();
        request.open("GET","staff.php?number="+document.getElementById("keyword").value);
        request.send();

        request.onreadystatechange = function(){
            if(request.readyState === 4){
                if(request.status === 200){
                    var type = request.getResponseHeader("Content-Type");
                    if(type.indexOf("application/json") === 0){
                        var data = JSON.parse(request.responseText);

                        if(data.number){
                            document.getElementById('searchResult').innerHTML =
                                '[找到員工] 員工編號：' +data.number + ', 姓名：' +
                                data.name + ', 性別：' + data.sex;
                        }else{
                            document.getElementById("searchResult").innerHTML = data.msg;
                        }
                    }
                }else{
                    alert("發生錯誤"+request.status);
                }
            }
        }
    }

    document.getElementById('save').onclick = function(){
        var request = new XMLHttpRequest();
        request.open("POST","staff.php");

        var data = "name=" + document.getElementById("staffName").value +
            "&number=" + document.getElementById("staffNumber").value +
            "&sex=" + document.getElementById("staffSex").value;
        request.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
        request.send(data);

        request.onreadystatechange = function(){
            if(request.readyState === 4){
                if(request.status === 200){
                    var type = request.getResponseHeader("Content-Type");
                    if(type.indexOf("application/json") === 0){
                        var data = JSON.parse(request.responseText);
                        if(data.name){
                            document.getElementById("createResult").innerHTML = '員工：' + data.name + '，儲存成功！';
                        } else {
                            document.getElementById("createResult").innerHTML = data.msg;
                        }
                    }
                }else{
                    alert("發生錯誤"+request.status);
                }
            }
        }
    }
</script>
</body>
</html>