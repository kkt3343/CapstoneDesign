<?php
	$manufacturer = $_GET['manufacturer'];
	$model = $_GET['model'];
	
	$con = mysqli_connect("localhost", "dbAdmin", "xoduqrb", "usedcardb") or die ("MySQL 접속 실패!!");
	$sql1 = "SELECT model_detail FROM carModel WHERE manufacturer = '"
			.$manufacturer."' and model = '".$model."' ORDER by model_detail";
	
	$ret = mysqli_query($con, $sql1);
	while ($row = mysqli_fetch_array($ret)) {
		$res['model_detail'] = urlencode($row['model_detail']);
		$arr["result"][] = $res;
	}

	$json = json_encode($arr);
	$json = urldecode($json);
	print $json;


	mysqli_close($con);
?>