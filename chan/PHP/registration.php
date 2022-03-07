<?php
	$userid = $_POST['userid'];
	$userpw = $_POST['userpw'];
	$username = $_POST['username'];
	$email = $_POST['email'];
	$age = $_POST['age'];
	$gender = $_POST['gender'];
	
	$con = mysqli_connect("localhost", "dbAdmin", "xoduqrb", "usedcardb") or die ("MySQL 접속 실패!!");
	$sql = "INSERT INTO userTable VALUES(NULL, '{$userid}', '{$userpw}', '{$username}', '{$email}', {$age}, '{$gender}', 0)";
	$ret = mysqli_query($con, $sql);
	mysqli_close($con);
?>