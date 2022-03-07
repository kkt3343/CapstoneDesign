<?php
	$token = $_GET['token'];
	
	$con = mysqli_connect("localhost", "dbAdmin", "xoduqrb", "usedcardb") or die ("MySQL 접속 실패!!");
	$sql1 = "INSERT INTO testToken VALUES('".$token."')";
	
	$ret = mysqli_query($con, $sql1);
	mysqli_close($con);
?>