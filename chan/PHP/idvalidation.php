<?php
	$userid = $_POST['userid'];
	//$email = $_POST['email'];
	//$age = $_GET['age'];
	//$gender = $_GET['gender'];
	
	$con = mysqli_connect("localhost", "dbAdmin", "xoduqrb", "usedcardb") or die ("MySQL 접속 실패!!");
	$sql = "SELECT count(*) as count FROM userTable WHERE userid = '{$userid}'";
	$ret = mysqli_query($con, $sql);
	$row = mysqli_fetch_array($ret);
	$count = $row['count'];
	if ($count >= 1) {
		print 'False';
	}
	else {
		print 'True';
	}
	mysqli_close($con);
?>