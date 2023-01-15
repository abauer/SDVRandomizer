<html>
<body>

<?php
$command = escapeshellcmd('python ../app/cropsShuffler.py '.$_POST['harvestShuffle'])
echo $command
//shell_exec($command)

?>

</body>
</html>