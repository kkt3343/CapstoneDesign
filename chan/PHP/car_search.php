<?php
	$manufacturer = $_GET['manufacturer'];
	$model = $_GET['model'];
	$model_detail = $_GET['model_detail'];
	
	$con = mysqli_connect("localhost", "dbAdmin", "xoduqrb", "usedcardb") or die ("MySQL 접속 실패!!");
	
	$sql1 = "SELECT * FROM usedCar WHERE manufacturer = '".$manufacturer."'";
	if ($model != "NULL") {
		$sql1 = $sql1." and model = '".$model."'";
	}
	if ($model_detail != "NULL") {
		$sql1 = $sql1." and model_detail = '".$model_detail."'";
	}
	$sql1 = $sql1." ORDER BY carid DESC";
	$ret = mysqli_query($con, $sql1);
	while ($row = mysqli_fetch_array($ret)) {
		$res['carid'] = urlencode($row['carid']);
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
	$sql2 = "SELECT count(*) as 'count', AVG(price) as 'priceAVG', AVG(distance) as 'distAVG' FROM usedCar";
	$sql2 = $sql2." WHERE manufacturer = '".$manufacturer."'";
	if ($model != "NULL") {
		$sql2 = $sql2." and model = '".$model."'";
	}
	if ($model_detail != "NULL") {
		$sql2 = $sql2." and model_detail = '".$model_detail."'";
	}
	$sql2 = $sql2." ORDER BY carid DESC";
	
	$ret = mysqli_query($con, $sql2);
	while ($row = mysqli_fetch_array($ret)) {
		$res2['count'] = urlencode($row['count']);
		$res2['priceAVG'] = urlencode($row['priceAVG']);
		$res2['distAVG'] = urlencode($row['distAVG']);
		$arr["result2"][] = $res2;
	}
	
	$json = json_encode($arr);
	$json = urldecode($json);
	print $json;
	mysqli_close($con);
?>