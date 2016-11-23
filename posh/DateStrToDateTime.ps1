$fileName = "20160614_KA_HI_6789_plktokari_M060_D2_E230.505_16241AC2_Driving_Test"
$Datestr = $fileName.split('_')[0]

[DateTime]$dt = new-object DateTime

[DateTime]::TryParseExact( $DateStr, "yyyyMMdd", [System.Globalization.Cultureinfo]::InvariantCulture, [System.Globalization.DateTimeStyles]::None, [ref]$dt )



