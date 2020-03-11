
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

$.fn.myfunction = function () {
    // blah
};

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
		if(DEBUG!=false){ console.log("site: " + siteFullPath); }
	}, 'text');
}
//** MENU HEADER **//
function urlParam(urlparam) {
	window.location.href=urlparam;
	if (urlparam=='#refresh') { 
		window.location.reload();  
		window.location.href='/www';
	}
	if(DEBUG!=false){ console.log('urlParam: ' + urlparam); }
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
			var line = '<div class="device" deviceID="' + device['deviceID'] + '"><div class="settings"></div><div class="icon" style="background: url(assets/images/icons/' + device['icon'] +')"></div><div class="title">' + device['title'] + '</div><div class="portid">' + device['deviceID'] + ':0</div><div class="midi"><div class="icon"></div><div class="command">none</div></div></div>';
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
			console.log( "loadDevices()::lines ==> " + lines );
			for (var i = 0, len = lines.length; i < len; i++) {
				var lineData = lines[i].split(":");
				var deviceID = lineData[1];
				if(DEBUG!=false){
					console.log( "loadDevices()::lineData ==> " + lineData );
					console.log( "loadDevices()::deviceID ==> " + deviceID );
				}
				if (checkDeviceJSON(deviceID)==false) { 
					var line = '<div class="device" deviceID="' + lineData[1] + '"><div class="settings"></div><div class="icon"></div><div class="title">' + lineData[0] + '</div><div class="portid">' + lineData[1] + ':0</div><div class="midi"><div class="icon"></div><div class="command">none</div></div></div>';
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

$(document).ready(function(){

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
	});

	$(".menu-icon").hover(function(){
		// inFunction
		$(this).css({"transform": "scale(1.25)"});
		$(this).next().css({"color": "rgba(255,255,255,0.80)"});
	},function(){
		// outFunction
		$(this).css({"transform": "scale(1)"});
		$(this).next().css({"color": "rgba(46,94,114,1)","transform": "scale(1)"});
	});

	$(".menu-text").hover(function(){
		// inFunction
		$(this).css({"color": "rgba(255,255,255,0.80)","transform": "scale(1)"});
		$(this).prev().css({"transform": "scale(1.25)"});
	},function(){
		// outFunction
		$(this).css({"color": "rgba(46,94,114,1)"});
		$(this).prev().css({"transform": "scale(1)"});
	});


	//** REFRESH **//


	//** DEVICES **//
	// var checkdevicejson = return checkDeviceJSON(24);
	// console.log('true/false: ' + checkdevicejson);
	//if (checkDeviceJSON(24)==false) { console.log('NOTFOUND device_xx.json'); } else { console.log('FOUND device_xx.json'); }

	//** PORTS **//


	//** LOGS **//


	//** SETTINGS **//



});
