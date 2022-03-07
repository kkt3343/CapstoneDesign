<?php
	$userid = $_POST['userid'];
	
	$con = mysqli_connect("localhost", "dbAdmin", "xoduqrb", "usedcardb") or die ("MySQL 접속 실패!!");
	$sql = "SELECT count(*) as count FROM userTable WHERE userid = '{$userid}'";
	$ret = mysqli_query($con, $sql);
	$row = mysqli_fetch_array($ret);
	if ($row['count'] == 1) {
		print 'True';
		$sql2 = "UPDATE userTable SET token = NULL, isLogin = 0 WHERE userid = '{$userid}'";
		$ret = mysqli_query($con, $sql2);
	}
	else {
		print 'False';
	}
	mysqli_close($con);
?>