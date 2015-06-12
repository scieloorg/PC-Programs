<script language="JavaScript" type="text/javascript">
<!--
var selected_tab_id = null;

function openClose(theID) {
    if (document.getElementById(theID).style.display == "none") { 
        document.getElementById(theID).style.display = "block" 
        document.getElementById('hide'+theID).style.display = "block" 
        document.getElementById('show'+theID).style.display = "none" 
    }
    else { 
        document.getElementById(theID).style.display = "none" 
        document.getElementById('hide'+theID).style.display = "none" 
        document.getElementById('show'+theID).style.display = "block" 
        window.location = '#begin_' + theID;
        
    } 
}


function display_tab_content(theID, selected) {
	if (selected_tab_id == null) {
		selected_tab_id = selected
	}
    if (selected_tab_id) {
    	document.getElementById('tab-content-' + selected_tab_id).style.display = "none" 
    	document.getElementById('tab-label-' + selected_tab_id).className = "not-selected-tab"
    }
    selected_tab_id = theID
    document.getElementById('tab-label-' + theID).className = "selected-tab"
    document.getElementById('tab-content-' + theID).style.display = "block"         
}
// -->
</script>


<!-- Read more : http://www.ehow.com/how_5772308_expand-collapse-text.html -->
