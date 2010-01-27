<?php
/*
XSLTranformer -- Class to transform XML files using XSL with the Sablotron libraries.
Justin Grant (2000-07-30)
Thanks to Bill Humphries for the original examples on using the Sablotron module.
*/

class XSLTransformer {
	var $xsl, $xml, $output, $error, $processor;

	/* Constructor  */	 
	function XSLTransformer() { 
		$this->processor = xslt_create(); 
	} 

 	/* Destructor */ 
	function destroy() { 
		xslt_free ($this->processor); 
	} 

	/* output methods */
	function setOutput ($string) {
		$this->output = $string;
	}

	function getOutput() {
		return $this->output;
	}

	/* set methods */
	function setXml ($uri) { 
		if ( $doc = new docReader ($uri) ) { 
			$this->xml	= $doc->getString(); 
			return true; 
		} 
        else { 
			$this->setError ("Could not open $xml"); 
			return false; 
		} 
	} 	

	function setXsl($uri) {
		if ( $doc = new docReader ($uri) ) {
			$this->xsl	= $doc->getString();
			return true;
		} 
        else {
			$this->setError ("Could not open $uri");
			return false;
		}
	}

	/* transform method */
    function transform()
    {

		$args = array ( '/_xml' => $this->xml, '/_xsl' => $this->xsl );		

        $result = xslt_process ($this->processor, 'arg:/_xml', 'arg:/_xsl', NULL, $args); 

		if (xslt_error($this->processor)!='') {
			echo "class.XSLTransformer41.php<br>"; 
			echo "xslt_error:".xslt_error($this->processor)."<br>"; 
			echo "result:".$result."<br>";
		}
		if (strlen($result)==0) {
			echo "class.XSLTransformer41.php<br>"; 
			echo "xslt_error:".xslt_error($this->processor)."<br>"; 
			echo "result:".$result."<br>";
		}

        if ($result) {
		    $this->setOutput ($result);
		}
		else {
			echo "class.XSLTransformer41.php<br>"; 
            $err = "<br/>Error: " . xslt_error ($this->processor) . "<br/>Errorcode: " . xslt_errno ($this->processor);
		    $this->setError ($err);
		}
    }
    
	/* Error Handling */ 
	function setError ($string) { 
		$this->error = $string; 
	} 

 	function getError() { 
		return $this->error; 
	} 
}

/* docReader -- read a file or URL as a string */ 
class docReader { 
	var $string;	// public string representation of file 
	var $type;		// private URI type: 'file','url' 
	var $bignum		= 500000; 

	/* public constructor */ 
	function docReader ($uri) {  // returns integer 
		$this->setUri ($uri); 
		$this->setType(); 
		$fp = fopen ($this->getUri(),"r"); 

		if ($fp) { 
 			// get length 
			if ( $this->getType() == 'file' ) { 
				$length = filesize ($this->getUri()); 
			}  
            else { 
				$length = $this->bignum; 
 			} 
			$this->setString (fread ($fp, $length));
			// valido a partir de php 4.3.? $this->setString( file_get_contents( $this->getUri() )) ;
			fclose($fp);

			return 1; 
		} 
        else { 
			return 0; 
		} 
	} 

	/* determine if a URI is a filename or URL */ 
	function isFile ($uri) { 	// returns boolean 
		if (strstr ($uri,'http://') == $uri) { 
			return false; 
		} 
        else { 
			return true; 
		} 
	} 

	/* set and get methods */ 
	function setUri ($string) { 
		$this->uri = $string; 
	} 

	function getUri() { 
		return $this->uri; 
	} 

	function setString ($string) { 
		$this->string = $string; 
	} 

	function getString() { 
		return $this->string; 
	} 

	function setType() { 
		if ( $this->isFile ($this->uri) ) { 
			$this->type = 'file'; 
		} 
        else { 
			$this->type = 'url'; 
		}	 
	} 

	function getType() { 
		return $this->type; 
	} 
} 

?>
