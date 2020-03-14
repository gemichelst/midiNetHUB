/*
#
# midiNetHUB
# DEFAULT WWW JS
# written by Michael Matzat
#
*/

// const DEBUG = false;
if (loadIT == true){

	/////////////////////////////
	//////// DOCUMENT READY /////
	/////////////////////////////

	$(document).ready(function() {

	    console.log('midiDisplay V1');
	    if (DEBUG) { console.log('DEBUG: enabled'); } else { console.log('DEBUG: disabled'); }

	    //// MENU HEADER: Animations, Functions ////
	    var site = 'devices';
	    loadSite(site);
	    $(".menu-columns").click(function() {
	        var site, urlparam;
	        site = $(this).attr('site');
	        urlparam = $(this).attr('urlparam');
	        if (urlparam == "none") { loadSite(site); } else { urlParam(urlparam); }
	    });

	    $(".menu-icon").hover(function() {
	        // inFunction
	        $(this).css({ "transform": "scale(1.25)" });
	        $(this).next().css({ "color": "rgba(255,255,255,0.80)" });
	    }, function() {
	        // outFunction
	        $(this).css({ "transform": "scale(1)" });
	        $(this).next().css({ "color": "rgba(46,94,114,1)", "transform": "scale(1)" });
	    });

	    $(".menu-text").hover(function() {
	        // inFunction
	        $(this).css({ "color": "rgba(255,255,255,0.80)", "transform": "scale(1)" });
	        $(this).prev().css({ "transform": "scale(1.25)" });
	    }, function() {
	        // outFunction
	        $(this).css({ "color": "rgba(46,94,114,1)" });
	        $(this).prev().css({ "transform": "scale(1)" });
	    });

	    //// DEVICES ////
	    $( ".icon-picker_icon" ).click(function() {
	        var icon_fileName = $(this).attr('icon-file-name'),
	            icon_divid = $(this).attr('id');
	        console.log('icon_fileName: ' + icon_fileName);
	        console.log('icon_divid: ' + icon_divid);
	    }).hover(function() {
	        // inFunction
	        console.log('onmouseover');
	        $(this).css({ "transform": "scale(1.25)" });
	        $(this).next().css({ "color": "rgba(255,255,255,0.80)" });
	    }, function() {
	        // outFunction
	        console.log('onmouseleft');
	        $(this).css({ "transform": "scale(1)" });
	        $(this).next().css({ "color": "rgba(46,94,114,1)", "transform": "scale(1)" });
	    });

	});
}