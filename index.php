<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<!-- This is the web page for setting the alarm time for clock6.py -->
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
<meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
<meta name="apple-mobile-web-app-capable" content="yes" />
<link rel="shortcut icon" href="favicon.ico" />
<link rel="desktop icon" href="sunrise.ico" />
<title>Alarm Clock</title>
<style type="text/css" media="screen">
body { background: #e7e7e7; font-family: Verdana, sans-serif; font-size: xx-large; }
<!--#page { background: #ffffff; margin: 50px; border: 2px solid #c0c0c0; padding: 10px; }
#header { background: #4b6983; border: 2px solid #7590ae; text-align: center; padding: 10px; color: #ffffff; }
#header h1 { color: #ffffff; }
#body { padding: 10px; }
span.tt { font-family: monospace; }
span.bold { font-weight: bold; }
a:link { text-decoration: none; font-weight: bold; color: #C00; background: #ffc; }
a:visited { text-decoration: none; font-weight: bold; color: #999; background: #ffc; }
a:active { text-decoration: none; font-weight: bold; color: #F00; background: #FC0; }
a:hover { text-decoration: none; color: #C00; background: #FC0; }
-->
</style>
</head>

<body>
<div id="page">
	<div id="header">
		<h1> Clock 6.0 </h1>
	</div>

	<div id="body">
 	   <form method="post" action="index.php">
		  Set alarm time: 
			<input type="text" name="newalarmtime">
			<input type="submit" value="Submit">
	  </form>
	  <?php
		echo "Server time : " . date("H:i", time()) . "<br>";
		if ($_POST){
			$fname=$_POST['newalarmtime'];
			echo "New alarm time : ";
			echo $fname;
			echo "<br>";
			$f=fopen("/home/pi/alarmtime","w") or die("Could not open alarmtime file for writing"); 
			fwrite($f, $fname);
			fclose($f); 
			$f=fopen("/home/pi/selftest","w") or die("Could not open selftest file for writing"); 
			fwrite($f, "1");
			fclose($f); 
		} 
		$lines = file('/home/pi/alarmtime');
		echo "Alarm time:   ". $lines[0] ."<br>";
		$lines = file('/home/pi/ledstate');
		echo "LED state:   ". $lines[0] ."<br>";
	  ?>
		<center>
			<img src="sunrise.jpg" alt="sunrise picture" > 
		</center>
	</div>
</div>
</body>
</html>
