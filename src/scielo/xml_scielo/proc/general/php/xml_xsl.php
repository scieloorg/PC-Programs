<?
	include("class.XSLTransformer.php");
	include("XML.php");
	
//	phpinfo();
	$XML_XSL = new XSL_XML();
	$xml = $XML_XSL->returnContent($argv[1]);
	$xsl = $argv[2];
	$xml = $XML_XSL->xml_xsl($xml, $xsl, "");
	
	$fp = fopen($argv[3], "w");
	if ($fp){
		fwrite($fp, $xml);
	}
?>