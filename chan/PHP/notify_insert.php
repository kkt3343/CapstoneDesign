<?php
	$userid = $_POST['userid'];
	$model = $_POST['model'];
	$caryear_from = $_POST['caryear_from'];
	$caryear_to = $_POST['caryear_to'];
	$distance_from = $_POST['distance_from'];
	$distance_to = $_POST['distance_to'];
	$price_from = $_POST['price_from'];
	$price_to = $_POST['price_to'];
	
	/* $userid = $_GET['userid'];
	$model = $_GET['model'];
	$caryear_from = $_GET['caryear_from'];
	$caryear_to = $_GET['caryear_to'];
	$distance_from = $_GET['distance_from'];
	$distance_to = $_GET['distance_to'];
	$price_from = $_GET['price_from'];
	$price_to = $_GET['price_to']; */
	
	$con = mysqli_connect("localhost", "dbAdmin", "xoduqrb", "usedcardb") or die ("MySQL 접속 실패!!");
	$sql = "INSERT INTO Notification VALUES(NULL, '{$userid}', '{$model}', {$caryear_from}, {$caryear_to}, {$distance_from}, {$distance_to}, {$price_from}, {$price_to})";
	$ret = mysqli_query($con, $sql);
	
	$sql2 = "SELECT LAST_INSERT_ID() as LAST";
	$ret = mysqli_query($con, $sql2);
	$row = mysqli_fetch_array($ret);
	print $row['LAST'];
	mysqli_close($con);
?>