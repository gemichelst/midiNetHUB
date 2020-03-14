
/*
#
# midiDisplay
# DEFAULT WWW JS
# written by Michael Matzat
#
*/

const DEBUG = true;

////////////////////////
//////// FUNCTIONS /////
////////////////////////

// $.fn.myfunction = function () {
//     // blah
// };

//** MAIN **//
function loadSite(site) {
	var siteFullPath = 'views/' + site + '.html';
	$(".content-viewer > .content").addClass('content-grey').addClass('content-zero');
	$.get(siteFullPath, function(data){
		setTimeout(function() { 
			$(".content-viewer > .content").remove();
			$(".content-viewer").html(data);
		}, 500);
		setTimeout(function() { 
			$(".content-viewer > .content").removeClass('content-zero'); 
			setTimeout(function() { 	
				if (site=='logs'){ loadLog('midiDisplay.log'); }
				if (site=='devices'){ loadDevices(); }
			}, 250);
		}, 1000);
		if(DEBUG!=false){ console.log( "loadSite("+ site + ") ==> " + siteFullPath ); }
	}, 'text');
}
//** MENU HEADER **//
function urlParam(urlparam) {
	window.location.href=urlparam;
	if (urlparam=='#refresh') { 
		window.location.reload();  
		window.location.href='/www';
	}
	if(DEBUG!=false){ console.log( "urlParam(urlparam)::" + urlparam ); }
} 

//** REFRESH **//


//** DEVICES **//
function checkDeviceJSON(deviceID) {
	/* CHECK IF DEVID IS AVAILABLE AND RETURN TRUE/FALSE */
	var jsonFile = 'device_' + deviceID + '.json',
		jsonFilePath = '/conf/devices/' + jsonFile;
		device = [];
	$.getJSON( jsonFilePath, function( data, textStatus ) {
		if (textStatus == "success") {
			if(DEBUG!=false){ console.log( "checkDeviceJSON(" + deviceID+ ")::found ==> " + jsonFile ); }
			return true; 
		} else { 
			if(DEBUG!=false){ console.log( "checkDeviceJSON(" + deviceID+ ")::notfound ==> " + jsonFile ); }
			return false; 
		}
	});
}
function loadDeviceFromJSON(deviceID) {
	/* LOAD DEVICE DATA FROM JSON */
	var jsonFile = 'device_' + deviceID + '.json',
		jsonFilePath = '/conf/devices/' + jsonFile;
		device = [];
	$.getJSON( jsonFilePath, function( data, textStatus ) {
		if (textStatus == "success") {
			$.each( data, function( key, val ) { device[key] = val; });
			var line = '<div class="device" deviceID="' + device['deviceID'] + '"><div onclick="deviceSettings(\'' + device['deviceID'] + '\');" class="settings" id="device' + device['deviceID'] + '" device-id="' + device['deviceID'] + '" device-title="' + device['title'] + '" device-usbid="' + device['usbID'] + '" device-desc="' + device['desc'] + '" device-icon="' + device['icon'] + '"></div><div class="icon" style="background: url(assets/images/icons/' + device['icon'] +')"></div><div class="title">' + device['title'] + '</div><div class="portid">' + device['deviceID'] + ':0</div><div class="midi"><div class="icon"></div><div class="command">none</div></div></div>';
			$("#devices > .devices").append(line);
		} else {
			return false;
		}
	});
}
function loadDevices(){
	var deviceFile = 'logs/midiDisplay.list',
		line;
	var device = [];
	if(DEBUG!=false){console.log( "loadDevices()::loading ==> " + deviceFile );}
	setTimeout(function() { 
		$.get(deviceFile, function(data){
			var lines = data.split("\n");
			if(DEBUG!=false) { console.log( "loadDevices()::lines ==> " + lines ); } 
			for (var i = 0, len = lines.length; i < len; i++) {
				var lineData = lines[i].split(":");
				var deviceID = lineData[1];
				if(DEBUG!=false){
					console.log( "loadDevices()::lineData ==> " + lineData );
					console.log( "loadDevices()::deviceID ==> " + deviceID );
				}
				if (checkDeviceJSON(deviceID)==false) { 
					var line = '<div class="device" deviceID="' + lineData[1] + '"><div onclick="deviceSettings(\'' + lineData[1] + '\');" class="settings" id="device' + lineData[0] + '" device-id="' + lineData[0] + '" device-title="' + lineData[0] + '" device-usbid="' + lineData[1] + ':0" device-desc="none" device-icon="piano.svg"></div><div class="icon"></div><div class="title">' + lineData[0] + '</div><div class="portid">' + lineData[1] + ':0</div><div class="midi"><div class="icon"></div><div class="command">none</div></div></div>';
					if(DEBUG!=false){ console.log('loadDeviceFromJSON('+deviceID+')==false');}
					if (lineData[1]!=undefined && deviceID!=undefined) { $("#devices > .devices").append(line); }
				} else {
					if(DEBUG!=false){ console.log('loadDeviceFromJSON('+deviceID+')==true'); }
					if (deviceID!=undefined) { loadDeviceFromJSON(deviceID); }
				}
			}
			if(DEBUG!=false){ console.log("deviceFile: " + deviceFile + " loaded"); }
		}, 'text');
	}, 25);
}
function saveDeviceAsJSON(deviceID,title,usbid,desc,icon) {
	$.get("/saveDevice", { id: deviceID, devicename: title, usbid: usbid, desc: desc, icon: icon },
    function(data,status){ if(DEBUG!=false){ console.log("Data: " + data + "\nStatus: " + status); }
    });
}
function iconPicker() {
	var toggle = $(".icon-icon").attr('toggle');
	if(toggle=='disabled') { 
		$(".icon-icon").attr({"toggle": "enabled"});
		$( ".icon-picker" ).css({"width": "100%","opacity": 1});
		if(DEBUG!=false){ console.log('iconPicker()::clicked ==> enabled'); }
	} else {
		$(".icon-icon").attr({"toggle": "disabled"});
		$( ".icon-picker" ).css({"width": "0%","opacity": 0});
		if(DEBUG!=false){ console.log('iconPicker()::clicked ==> disabled'); }
	}
}
function iconPickerFocusOut() {
	$(".icon-icon").attr({"toggle": "disabled"});
	$( ".icon-picker" ).css({"width": "0%","opacity": 0});
	if(DEBUG!=false){ console.log('iconPicker()::clicked ==> focus-out > disabled'); }
}
function iconPickerSelectIcon(icon_name) {
	var icon_fullpath = 'assets/images/icons/' + icon_name;
	$( ".icon-image" ).attr({"src": icon_fullpath});
	$( "input#device_icon" ).val(icon_name);
	$( ".icon-picker" ).css({"width": "0%","opacity": 0});
	if(DEBUG!=false){ console.log('iconPicker()::selected ==> ' + icon_name); }
}
function openEditor(deviceicon) {
	var icon_fullpath = 'assets/images/icons/' + deviceicon;
	$( ".icon-image" ).attr({"src": icon_fullpath});
	$( "input#device_icon" ).val(deviceicon);
	$( "#overlay" ).css({"display": "block"});
	setTimeout(function() { 
		$( "#overlay" ).css({"transform": "scaleX(1)","opacity": 1});
		$( "#editor" ).css({"transform": "scaleY(1)","opacity": 1});
	}, 25);
	if(DEBUG!=false) { console.log('openEditor()::clicked ==> '+ this); }
}
function closeEditor() {
	if(DEBUG!=false) { console.log('closeEditor()::clicked ==> '+ this); }
	$( "#editor" ).css({"transform": "scaleY(0)","opacity": 0});
	$( "#overlay" ).css({"transform": "scaleX(0)","opacity": 0});
	setTimeout(function() { $( "#overlay" ).css({"display": "none"}); }, 250);
}
function submitEditor() {
	if(DEBUG!=false) { console.log('form()::submit'); }
	var device_id = $( "input#device_id" ).val(),
		device_icon = $( "input#device_icon" ).val(),
		device_title = $( "input#device_title" ).val(),
		device_usbid = $( "input#device_usbid" ).val(),
		device_desc = $( "input#device_desc" ).val();
	closeEditor();
	saveDeviceAsJSON(device_id,device_title,device_usbid,device_desc,device_icon);
	// return;
	location.reload(true);
}
function deviceSettings(deviceid) {
	var elementid = '#device' + deviceid;
	var deviceid = $(elementid).attr('device-id'),
		devicetitle = $(elementid).attr('device-title'),
		deviceusbid = $(elementid).attr('device-usbid'),
		devicedesc = $(elementid).attr('device-desc'),
		deviceicon = $(elementid).attr('device-icon');
		openEditor(deviceicon);
		$("#device_id").val(deviceid);
		$("#device_title").val(devicetitle);
		$("#device_usbid").val(deviceusbid);
		$("#device_desc").val(devicedesc);
		$("#device_icon").val(deviceicon);
	if(DEBUG!=false) { 
		console.log('deviceSettings('+deviceid+')::clicked ==> ' + elementid);
		console.log('++DEVICE-DATA++\ntitle: '+devicetitle+'\nid: '+deviceid+'\nusbid: '+deviceusbid+'\ndesc: '+devicedesc+'\nicon: '+deviceicon);
	}
}

//** PORTS **//


//** LOGS **//
function loadLog(logFile){
	var logFile = 'logs/' + logFile;
	$.get(logFile, function(data){
		$("#file-viewer > p").remove();
		$("#file-viewer").html('<p></p>');
		var lines = data.split("\n");
		for (var i = 0, len = lines.length; i < len; i++) {
			if(i < 10){ ii = '0' + i; } else { ii = i; }
			var line = '<div class="lines"><div class="line-row-num">' + ii + '</div><div class="line-row">' + lines[i] + "</div><br/>";
			if (lines[i]!='') { $("#file-viewer > p").append(line); }
		}
		if(DEBUG!=false){console.log("logFile: " + logFile + " loaded");}
	}, 'text');
}

//** SETTINGS **//



/////////////////////////////
//////// DOCUMENT READY /////
/////////////////////////////

$( document ).ready(function() {

	console.log('midiDisplay V1');
	if(DEBUG!=false) { console.log('DEBUG: enabled'); } else { console.log('DEBUG: disabled'); } 

	//++ MENU HEADER: Animations, Functions ++//
	var site = 'devices';
	loadSite(site);
	$(".menu-columns").click(function() {
		var site, urlparam;
		site=$(this).attr('site');
		urlparam=$(this).attr('urlparam');
		if (urlparam=='none'){ loadSite(site); } else { urlParam(urlparam); }
	})

	$(".menu-icon").hover(function(){
		// inFunction
		$(this).css({"transform": "scale(1.25)"});
		$(this).next().css({"color": "rgba(255,255,255,0.80)"});
	},function(){
		// outFunction
		$(this).css({"transform": "scale(1)"});
		$(this).next().css({"color": "rgba(46,94,114,1)","transform": "scale(1)"});
	})

	$(".menu-text").hover(function(){
		// inFunction
		$(this).css({"color": "rgba(255,255,255,0.80)","transform": "scale(1)"});
		$(this).prev().css({"transform": "scale(1.25)"});
	},function(){
		// outFunction
		$(this).css({"color": "rgba(46,94,114,1)"});
		$(this).prev().css({"transform": "scale(1)"});
	})


	//** REFRESH **//


	//** DEVICES **//

	// $( "form" ).submit(function( event ) {
	// 	event.preventDefault();
	// 	var device_id = $( "input#device_id" ).val(),
	// 		device_icon = $( "input#device_icon" ).val(),
	// 		device_title = $( "input#device_title" ).val(),
	// 		device_usbid = $( "input#device_usbid" ).val(),
	// 		device_desc = $( "input#device_desc" ).val();
	// 		saveDeviceAsJSON(device_id,device_title,device_usbid,device_desc,device_icon);
	// 		// $( "span" ).text( "Validated..." ).show();
	//  	return;
	
	//   // $( "span" ).text( "Not valid!" ).show().fadeOut( 1000 );
		
	// });

	//** PORTS **//


	//** LOGS **//


	//** SETTINGS **//



});
