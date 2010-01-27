<?

define('XML_PROCESSING_INSTRUCTION','<?xml version="1.0" encoding="ISO-8859-1"?>');

class XSL_XML  {

	function xml_xsl ( $xmlContent, $xslFile, $debug )
	{

		if ($xmlContent=='') die("falta o XML");
		if ($xslFile=='') die("falta XSL para transformar\n".$xmlContent);
		if (!file_exists($xslFile)){die($xslFile." not found.");}
		$xslt = new XSLTransformer();
		
		$xslt->xml = $this->insertProcessingInstruction(trim($xmlContent));		
		if ( $debug == "XML" ) { die($xslt->xml); }
		$xslt->setXsl($xslFile);

		if ( $debug == "XSL" ) { die($xslt->xsl.'<!--'.$xslFile.'-->'); }
		$xslt->transform();

		//$r = utf8_decode($xslt->getOutput());
		$r = $xslt->getOutput();
		
		return $r.$hidden;

	}

	function returnContent($fileName){
			if ($fileName) {
				$fp = fopen ($fileName,"r");
				if ($fp) {
					$content = fread($fp,filesize($fileName));
				}
			}
			return $content;
		}			


	function returnXML_HTTP_INFO($HTTP_POST_VARS,$HTTP_GET_VARS, $HTTP_SERVER_VARS, $scriptVars, $root='http-info') {
		$i = 0;	
		if ($HTTP_POST_VARS) $VARS = $HTTP_POST_VARS;
		if ($HTTP_GET_VARS) $VARS = $HTTP_GET_VARS;
		
	    $VARS['currentDate'] = date('YmdHisD');

		$xmlList[$i++] = $this->returnHTTP_VARS($VARS,'cgi', $scriptVars);	
		$xmlList[$i++] = $this->returnHTTP_VARS($HTTP_SERVER_VARS,'server');
						
		return $this->concatXML($xmlList,$root);
	}


	function returnHTTP_VARS($HTTP_VARS, $root='HTTP_VARS', $scriptVars) {
		//$HTTP_VARS may be $HTTP_GET_VARS or $HTTP_POST_VARS
	
	       $xmlString = "<$root>\n";
		   $xmlString .= $this->arrayToXml($HTTP_VARS);
		   $xmlString .= $this->arrayToXml($scriptVars);	
	       $xmlString .= "</$root>";
	
	       return $xmlString;
	
	}

	
	function arrayToXml($HTTP_VARS){
	        reset($HTTP_VARS);
	
	        $myKey =  key($HTTP_VARS);
	        while ($myKey){
	             if (count($HTTP_VARS[$myKey]) <= 1) {
	                $xmlString .= "		<$myKey>" . $this->correctValue($HTTP_VARS[$myKey]) . "</$myKey>\n";
	             } else {
	                for($i = 0; $i < count($HTTP_VARS[$myKey]); $i++) {
	                  $xmlString .= "		<$myKey>" . $this->correctValue($HTTP_VARS[$myKey][$i]) . "</$myKey>\n";
	                }
	             }
	             next ($HTTP_VARS);
	             $myKey = key($HTTP_VARS);
	       }
		   return $xmlString;
	}

	
	function correctValue ($value){
		$value = str_replace("&amp;","&",stripslashes($value));
		$value = str_replace("&","&amp;",$value);
	
		return $value;
	}

	
	
	function concatXML($array_of_xml, $root = "root") {
		$content = XML_PROCESSING_INSTRUCTION;
		if ($root)		$content .= "\n<" . $root . ">\n";
		
		for ($i = 0; $i < count($array_of_xml); $i++) {
			$content .= $this->extractContent($array_of_xml[$i]) . "\n";
		}
		if ($root)		$content .= "</" . $root . ">";
		
		return trim($content);
	}

	

	function insertProcessingInstruction($xml) {
		$xml = trim($this->extractContent($xml));
//		if (substr(trim($xml),0,5) != substr(XML_PROCESSING_INSTRUCTION,0,5)){
			$xml = XML_PROCESSING_INSTRUCTION.$xml;
//		}
		return trim($xml);
	}

	
	
	function debugScript ($param, $xml, $xsl) {
		$param = strtolower($param);
		switch ($param) {
			case "xml":
				die($xml);
			case "xsl":
				die($xsl);
			case "phpinfo":
				die(phpinfo());
			default:
				die("invalid option to debug parameter!");
		}
	}

	
	
	function extractContent($xml){
		$return = $xml;
		$temp = trim($xml);
		$p = strpos($temp,'<?');
		$p2 = strpos($temp,'?>');
		if ((substr($temp,0,2) == '<?') && (!$p)){
			if ($p2){
				$return = substr($temp,$p2+2);
			}
		}
		return $return;
	}

	
/*	
	function validate ($xmlContent){

		$version = split ("\.", phpversion());
		$return = $xmlContent;

	    if ( $version[0] > 4 || ($version[0] == 4 && $version[1] >= 1) ) {
			$return = domxml_open_mem($xmlContent);
	    }
	    else {
			// $return = xmldoc($xmlContent); old function
			$return = domxml_open_mem($xmlContent);
	    }

		return $return;
	}
*/
	
	
	function new_recursiveFind($xml, $init, $end, $trim=true){
		$i = 0;
		$res = array();
		$r = $this->new_find($xml, $init, $end, $pNext);
		if ($trim) $r = trim($r);
		if ($r!=''){
			$res[$i++] = $r;	
		}

		while ($pNext){
			$xml = substr($xml, $pNext);
			$r = $this->new_find($xml, $init, $end, $pNext);
			if ($trim) $r = trim($r);
			if ($r!=''){
				$res[$i++] = $r;
			}
		}
		return $res;
	}
	//  retorna o conteúdo de um elemento cujo inicio é $ini e cujo fim é $end 
	function new_find($xml, $init, $end, &$pNext){
		$pNext = 0;
		$r = '';
		$p = strpos($xml,$init);
		
		if (($p) || (strcmp($init, substr($xml,$p,strlen($init)))==0) ){
			$pNext = $p;
			$r = substr($xml,$p + strlen($init));
			$p = strpos($r,$end);
			if (($p) || (strcmp($end, substr($r,$p,strlen($end)))==0) ){
				$r = substr($r,0,$p);
				$pNext = $pNext + strlen($init.$r.$end);
			}
		}
		return $r;
	}



	// retorna o conteúdo de um elemento cujo inicio é $ini e cujo fim é $end 
	function find($xml, $init, $end, &$foundElement){		
//		return $this->old_find($xml, $init, $end, $foundElement);
		return $this->new_find($xml, $init, $end, $foundElement);
	}

	
	
	function recursiveFind($xml, $init, $end, $trim=true){
//		return $this->old_recursiveFind($xml, $init, $end);
		return $this->new_recursiveFind($xml, $init, $end, $trim);
	}

	
	
	function old_find($xml, $init, $end, &$foundElement){
		$foundElement = false;
		$r = '';
		$p = strpos($xml,$init);
		if (($p) || (strcmp($init, substr($xml,$p,strlen($init)))==0) ){
			$r = substr($xml,$p + strlen($init));
			$p = strpos($r,$end);
			$r = substr($r,0,$p);
			$foundElement = true;
		}
		return $r;
	}

	
	
	function old_recursiveFind($xml, $init, $end){
		$i = 0;
		$res = array();
		$r = $this->old_find($xml, $init, $end);
		if ($r!=''){
			$res[$i++] = $r;	
		}
		while ($r!=''){
			$pos = strpos($xml, $init.$r.$end)+strlen($init.$r.$end);
			$xml = substr($xml,$pos);
			$r = $this->old_find($xml, $init, $end);
			if ($r!=''){
				$res[$i++] = $r;	
			}
		}
		return $res;
	}

	
	
	function insertElement($content, $element="root"){
		$xml = "<".$element.">".$this->extractContent($content)."</".$element.">";
		return $xml;
	}

	

	function deleteElement($xml, $element){
		$content = "<".$element.">".$this->find($xml, "<".$element.">", "</".$element.">")."</".$element.">";
		$r = str_replace($content, '', $xml);
		return $r;
	}

	

	function setAttribute($xml, $nodePath, $position, $attrName, $attrValue, $mode=''){
		if ($attrValue || ($mode=='update')){
			$xmlList[count($xmlList)] = "<xml>".$this->extractContent($xml)."</xml>";
			$xmlList[count($xmlList)] = "<selection>";		
			
			$xmlList[count($xmlList)] = "<nodePath>".$nodePath."</nodePath>";		
			$xmlList[count($xmlList)] = "<position>".$position."</position>";
			$xmlList[count($xmlList)] = "<attribute>".$attrName."</attribute>";
			$xmlList[count($xmlList)] = "<value>".$attrValue."</value>";
			$xmlList[count($xmlList)] = "</selection>";
			$xml = $this->xml_xsl($this->concatXML($xmlList), XSL_SET_ATTRIBUTE);
//	die($xml);	
		}
		return $xml;
	}
	function setElement($xml, $nodePath, $position, $elementName, $arrayElementValue, $mode='add'){
		if ($arrayElementValue || ($mode=='update')){
			$xmlList[count($xmlList)] = "<xml>".$this->extractContent($xml)."</xml>";
			$xmlList[count($xmlList)] = "<selection>";		
			
			$xmlList[count($xmlList)] = "<nodePath>".$nodePath."</nodePath>";		
			$xmlList[count($xmlList)] = "<position>".$position."</position>";
			$xmlList[count($xmlList)] = "<elementName>".$elementName."</elementName>";
			$xmlList[count($xmlList)] = "<elementValue>";
			
			if (is_array($arrayElementValue)){
				foreach ($arrayElementValue as $elementValue){
					$xmlList[count($xmlList)] = "<".$elementName.">".$elementValue."</".$elementName.">";
				}
			} else {
				$xmlList[count($xmlList)] = "<".$elementName.">".$arrayElementValue."</".$elementName.">";
			}
			$xmlList[count($xmlList)] = "</elementValue>";
			$xmlList[count($xmlList)] = "<mode>".$mode."</mode>";
			
			$xmlList[count($xmlList)] = "</selection>";
			$xml = $this->xml_xsl($this->concatXML($xmlList), XSL_SET_ATTRIBUTE);
		}
		return $xml;
	}
	
}
?>