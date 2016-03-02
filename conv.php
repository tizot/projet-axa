<?php

$data = explode("\n", file_get_contents('reg.log'));
$sub = explode("\n", file_get_contents('submission.txt'));

$data2 = array();
foreach($data as $d) {
    if (preg_match('#^[0-9.-]+#', $d)) {
        $data2[] = max(0, floor(floatval($d)));
    }
}

foreach($sub as $k => &$s) {
    if ($k > 0) {
        $s = preg_replace("#\t0#", "\t" . $data2[$k-1], $s);
    }

    echo $s . "\n";
}
?>
