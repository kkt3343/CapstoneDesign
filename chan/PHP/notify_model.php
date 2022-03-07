<?php
	$con = mysqli_connect("localhost", "dbAdmin", "xoduqrb", "usedcardb") or die ("MySQL 접속 실패!!");
	$sql1 = "SELECT DISTINCT model FROM carModel ORDER BY model ASC";
	
	$ret = mysqli_query($con, $sql1);
	while ($row = mysqli_fetch_array($ret)) {
		$res['model'] = urlencode($row['model']);
		$arr["result"][] = $res;
	}

	$json = json_encode($arr);
	$json = urldecode($json);
	print $json;


	mysqli_close($con);
?>