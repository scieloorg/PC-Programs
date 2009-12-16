<?php
/*XSLTranformer -- Class to transform XML files using XSL with the Sablotron libraries.
Justin Grant (2000-07-30)
Thanks to Bill Humphries for the original examples on using the Sablotron module.
*/
/* test */
 /*  $transformer = new XSLTransformer();
  if ($transform->setXsl("http://www.someurl.com/document.xsl") &&
      $transform->setXml("http://www.someurl.com/document.xml")) {
 	$transformer->transform();
 	echo $transformer->getOutput();
  } else {
 	echo $transformer->getError();
  } 
*/

class XSLTransformer{
	var $xsl, $xml, $output, $error ;

	/* Constructor  */

 	function XSLTransformer() {
		$this->processor = xslt_create();
 	}

  	/* Destructor */
 	function destroy() {
 		xslt_free($this->processor);
 	}

 	/* output methods */
	function setOutput($string) {
		$this->output = $string;
	}

	function getOutput() {
		return $this->output;
	}

	/* set methods */
	function setXml($uri) {
 		if($doc = new docReader($uri)) {
 			$this->xml = $doc->getString();
 			return true;
 		} else {
 			$this->setError("Could not open $xml");
 			return false;
 		}
 	}

	function setXsl($uri) {
		if($doc = new docReader($uri)) {
			$this->xsl = $doc->getString();
			return true;
		} else {
			$this->setError("Could not open $uri");
			return false;
		}
	}	

/*			
	function transform() {
         	xslt_process($this->xsl, $this->xml, $outcome);
 	        $this->setOutput($outcome);
	}
*/		

	/* transform method */	
	function transform() {
//      	xslt_process($this->xsl, $this->xml, &$output, &$err);
//		$this->setOutput($output);
//		$this->setError($err);

		$args = array("/_stylesheet", $this->xsl, "/_xmlinput", $this->xml, "/_output", 0, 0);

		if ($err = xslt_run ($this->processor, "arg:/_stylesheet", "arg:/_xmlinput", "arg:/_output", 0, $args))
		{			
			$output = xslt_fetch_result ($this->processor, "arg:/_output");
			$this->setOutput($output);
		}
		else
		{
			$this->setError($err);
		}
		
		
		
//if (strlen($output)==0) {echo "!3<br>";echo $err;}

	}

	/* Error Handling */
 	function setError($string) {
 		$this->error = $string;
 	}  	

	function getError() {
 		return $this->error; 	
	} 
}

/* docReader -- read a file or URL as a string */

 /* test */
 /* $docUri = new docReader('http://www.someurl.com/doc.html');
    echo $docUri->getString(); */

class docReader {
  	var $string; 	// public string representation of file
 	var $type; 	// private URI type: 'file','url'
 	var $bignum = 500000;

  	/* public constructor */
 	function docReader($uri) {	// returns integer
		$this->setUri($uri); 		
		$this->setType();
  		$fp = fopen($this->getUri(),"r");

 		if($fp) {
			// get length
 			if ($this->getType() == 'file') {
 				$length = filesize($this->getUri());
 			}  else {
 				$length = $this->bignum;
  			}
  			$this->setString(fread($fp,$length));
			fclose($fp);
			return 1;
 		} else {
 			return 0;
 		}
 	}

 	/* determine if a URI is a filename or URL */
 	function isFile($uri) { 	// returns boolean
		if (strstr($uri,'http://') == $uri) {
 			return false;
 		} else {
 			return true;
 		}
 	}  	

	/* set and get methods */
  	function setUri($string) {
 		$this->uri = $string;
 	}

  	function getUri() {
 		return $this->uri;
 	}

  	function setString($string) {
 		$this->string = $string;
 	}

  	function getString() {
 		return $this->string;
 	}

 	function setType() {
 		if ($this->isFile($this->uri)) {
 			$this->type = 'file';
 		} else {
 			$this->type = 'url';
 		}
 	}

  	function getType() {
 		return $this->type;
 	}

}  

?>