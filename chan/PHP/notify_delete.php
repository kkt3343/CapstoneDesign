<?php
	$noti_num = $_POST['noti_num'];
	
	$con = mysqli_connect("localhost", "dbAdmin", "xoduqrb", "usedcardb") or die ("MySQL 접속 실패!!");
	$sql = "DELETE FROM Notification WHERE noti_num = ($noti_num)";
	$ret = mysqli_query($con, $sql);
	
	mysqli_close($con);
?>