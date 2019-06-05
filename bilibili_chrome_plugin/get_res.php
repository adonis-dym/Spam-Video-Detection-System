<?php
$dbhost = 'localhost';  // mysql服务器主机地址
$dbuser = '*******';            // mysql用户名
$dbpass = '*******';          // mysql用户名密码
$dbname = 'bilibili';

// 浏览器同源策略
header('content-type:application:json;charset=utf8');
header('Access-Control-Allow-Origin:*');
header('Access-Control-Allow-Methods:POST,GET');
header('Access-Control-Allow-Headers:x-requested-with,content-type');
 


$conn = new mysqli($dbhost, $dbuser, $dbpass, $dbname);
if(! $conn )
{
    die('连接失败: ' . mysqli_error($conn));
}

// 设置编码，防止中文乱码
mysqli_query($conn , "set names utf8");

if(isset($_GET["aid"])){

    $aid = addslashes($_GET["aid"]);

    $sql = 'SELECT pred_combined
            FROM res
            WHERE aid='.(string)$aid.
            ' LIMIT 1';
    
    //echo $sql;

    $retval = mysqli_query( $conn, $sql );
    if(! $retval )
    {
        die(0);
    }

    while($row = mysqli_fetch_array($retval, MYSQLI_ASSOC))
    {
        echo "{$row['pred_combined']}";
    }
}
mysqli_close($conn);
?>