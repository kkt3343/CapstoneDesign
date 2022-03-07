<?php
	$userid = $_POST['userid'];
	$userpw = $_POST['userpw'];
	$usertoken = $_POST['token'];
	
	$con = mysqli_connect("localhost", "dbAdmin", "xoduqrb", "usedcardb") or die ("MySQL 접속 실패!!");
	$sql = "SELECT count(*) as count FROM userTable WHERE userid = '{$userid}' and userpw = '{$userpw}'";
	$ret = mysqli_query($con, $sql);
	$row = mysqli_fetch_array($ret);
	if ($row['count'] == 1) {
		$sql2 = "SELECT * FROM userTable WHERE userid = '{$userid}'";
		$ret2 = mysqli_query($con, $sql2);
		$row2 = mysqli_fetch_array($ret2);
		
		if ($row2['isLogin'] == 0) { // 로그인 성공시
			print '1';
		}
		else { // 중복 로그인시
			print '2';
		}
		$sql3 = "UPDATE userTable SET token = '{$usertoken}', isLogin = 1 WHERE userid = '{$userid}'";
		mysqli_query($con, $sql3);
	}
	else { // 로그인 실패
		print '3';
	}
	mysqli_close($con);
?>