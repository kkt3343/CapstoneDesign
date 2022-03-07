<?php
	$con = mysqli_connect("localhost", "dbAdmin", "xoduqrb", "usedcardb") or die ("MySQL 접속 실패!!");
	$sql1 = "SELECT * FROM usedCar ORDER BY carid DESC";
	
	$ret = mysqli_query($con, $sql1);
	while ($row = mysqli_fetch_array($ret)) {
		$res['url'] = urlencode($row['url']);
		$res['site'] = urlencode($row['site']);
		$res['title'] = urlencode($row['title']);
		$res['carnumber'] = urlencode($row['carnumber']);
		$res['cartype'] = urlencode($row['cartype']);
		$res['manufacturer'] = urlencode($row['manufacturer']);
		$res['model'] = urlencode($row['model']);
		$res['model_detail'] = urlencode($row['model_detail']);
		$res['price'] = urlencode($row['price']);
		$res['distance'] = urlencode($row['distance']);
		$res['displacement'] = urlencode($row['displacement']);
		$res['caryear'] = urlencode($row['caryear']);
		$res['carcolor'] = urlencode($row['carcolor']);
		$res['carfuel'] = urlencode($row['carfuel']);
		$res['imglink'] = urlencode($row['imglink']);
		$arr["result"][] = $res;
	}
	
	$json = json_encode($arr);
	$json = urldecode($json);
	print $json;
	mysqli_close($con);
?>