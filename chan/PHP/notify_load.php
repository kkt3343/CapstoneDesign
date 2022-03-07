<?php
	$userid = $_POST['userid'];
	
	$con = mysqli_connect("localhost", "dbAdmin", "xoduqrb", "usedcardb") or die ("MySQL 접속 실패!!");
	$sql1 = "SELECT * FROM Notification WHERE userid = '{$userid}'";
	
	$ret = mysqli_query($con, $sql1);
	while ($row = mysqli_fetch_array($ret)) {
		$res['noti_num'] = urlencode($row['noti_num']);
		$res['userid'] = urlencode($row['userid']);
		$res['model'] = urlencode($row['model']);
		$res['caryear_from'] = urlencode($row['caryear_from']);
		$res['caryear_to'] = urlencode($row['caryear_to']);
		$res['distance_from'] = urlencode($row['distance_from']);
		$res['distance_to'] = urlencode($row['distance_to']);
		$res['price_from'] = urlencode($row['price_from']);
		$res['price_to'] = urlencode($row['price_to']);
		$arr["result"][] = $res;
	}
	
	if (mysqli_num_rows($ret) > 0){
		$json = json_encode($arr);
		$json = urldecode($json);
		print $json;
	}
	else {
		print "NULL";
	}
	mysqli_close($con);
?>