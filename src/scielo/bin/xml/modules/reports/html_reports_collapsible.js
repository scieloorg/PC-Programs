<script language="JavaScript" type="text/javascript">
<!--
var selected_tab_id = null;
var open_report_id = null;

function openClose(theID) {
    if (document.getElementById(theID).style.display == "none" || document.getElementById(theID).style.display != "block") { 
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


function display_article_report(clicked_report_id, label_id, location) {
    window.location = '#' + location;
    document.getElementById(label_id).style.textDecoration = "line-through"
    if (open_report_id != null) {
        if (open_report_id != clicked_report_id) {
            if (document.getElementById(open_report_id).style.display != "none" || document.getElementById(open_report_id).style.display == "block") {
                document.getElementById(open_report_id).style.display = "none"
                open_report_id = null
            }
        }
    }
    if (document.getElementById(clicked_report_id).style.display == "none" || document.getElementById(clicked_report_id).style.display != "block") {
        open_report_id = clicked_report_id
        document.getElementById(clicked_report_id).style.display = "block"
        //document.getElementById('label-' + clicked_report_id).className = "read"
    } else {
        document.getElementById(clicked_report_id).style.display = "none"
        open_report_id = null
    }
    window.location = '#' + location;
}

// -->
</script>


<!-- Read more : http://www.ehow.com/how_5772308_expand-collapse-text.html -->
