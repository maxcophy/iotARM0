<!doctype html>
<html lang="en">
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
<script type="text/JavaScript">
    $(document).ready(function() {
        $("#search").click(function() {
            $.ajax({
                type: "GET",
                url: "service.php?number= " + $("#keyword").val(),
                dataType: "json",
                success: function(data) {
                    if (data.number) {
                        $("#searchResult").html(
                            '[找到員工] 員工編號：' +data.number + ', 姓名：' + data.name + ', 性別：' + data.sex
                        );
                    } else {
                        $("#searchResult").html(data.msg);
                    }
                },
                error: function(jqXHR) {
                    alert("發生錯誤: " + jqXHR.status);
                }
            })
        })

        $("#save").click(function() {
            $.ajax({
                type: "POST",
                url: "service.php",
                dataType: "json",
                data: {
                    name: $("#staffName").val(),
                    number: $("#staffNumber").val(),
                    sex: $("#staffSex").val()
                },
                success: function(data) {
                    if (data.name) {
                        $("#createResult").html('員工：' + data.name + '，儲存成功！');
                    } else {
                        $("#createResult").html(data.msg);
                    }
                },
                error: function(jqXHR) {
                    alert("發生錯誤: " + jqXHR.status);
                }
            })
        })
    });
</script>

<script src="https://cdnjs.cloudflare.com/ajax/libs/tether/1.2.0/js/tether.min.js"
        integrity="sha384-Plbmg8JY28KFelvJVai01l8WyZzrYWG825m+cZ0eDDS1f7d/js6ikvy1+X+guPIB"
        crossorigin="anonymous"></script>
</body>
</html>