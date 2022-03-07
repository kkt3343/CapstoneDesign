<?php
	$usertoken = $_POST['token'];
	
	$con = mysqli_connect("localhost", "dbAdmin", "xoduqrb", "usedcardb") or die ("MySQL 접속 실패!!");
	$sql = "SELECT count(*) as count FROM userTable WHERE token = '{$usertoken}'";
	$ret = mysqli_query($con, $sql);
	$row = mysqli_fetch_array($ret);
	if ($row['count'] == 1) {
		print 'True';
	}
	else {
		print 'False';
	}
	mysqli_close($con);
?>