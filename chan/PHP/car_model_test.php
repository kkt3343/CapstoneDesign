<?php
	$con = mysqli_connect("localhost", "dbAdmin", "xoduqrb", "usedcardb") or die ("MySQL 접속 실패!!");
	$sql1 = "SELECT DISTINCT manufacturer FROM carModel ORDER BY manufacturer;";
	
	$ret = mysqli_query($con, $sql1);
	while ($row = mysqli_fetch_array($ret)) {
		if ($row['manufacturer'] != "기타"){
			$res['manufacturer'] = urlencode($row['manufacturer']);
			$arr["result"][] = $res;
			$arr["result2"][] = $res;
		}
		else {
			$temp['manufacturer'] = urlencode($row['manufacturer']);
		}
	}
	$arr["result"][] = $temp;
	$arr["result2"][] = $temp;
	$json = json_encode($arr);
	$json = urldecode($json);
	print $json;


	mysqli_close($con);
?>