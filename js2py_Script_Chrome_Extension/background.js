var tab = null ;
var lasttabUsed = null;
var currenturl = null;
var onoff = false;
var mon_started = false;
var http_https = null;
var Primary = '127.0.0.1:8080' //Target Server 1
var Secondary = '127.0.0.1:8181' //Target Server 2
var end_point = '/favicon.ico';
var Primary_Down = false;
var Primary_Module_Down = false;
var Secondary_Down = false;
var Secondary_Module_Down = false;
var Servers_Are_Down = false;
var Servers_Are_Down_Log = false;
var Modules_Are_Down = false;
var Modules_Are_Down_Log = false;
var Primary_Log = false;
var Secondary_Log = false;
var get_endpoint = false
console.log("L7_Auto_Switching(Duplexer)");
console.log("__by LEE JUNSUNG");
chrome.tabs.onRemoved.addListener(function(tabid) {
 if(tabid == lasttabUsed){
  console.log('Target tab ' + tabid + ' is closed')
    tab = null;
    mon_started = false;
    Primary_Log = false;
    Secondary_Log = false;
    Servers_Are_Down_Log = false;
    Modules_Are_Down_Log - false;
    
    Primary_Down = false;
    Secondary_Down = false;
    Servers_Are_Down = false
    Primary_Module_Down = false;
    Secondary_Module_Down = false;
    Modules_Are_Down = false;
    get_endpoint = false
 }
 mon_started = false;
});
setInterval(() => {
const timestamp = Date.now();
const currentDate = new Date(timestamp);
const hours = currentDate.getHours().toString().padStart(2, '0');
const minutes = currentDate.getMinutes().toString().padStart(2, '0');
const seconds = currentDate.getSeconds().toString().padStart(2, '0');
//const controllerPrimary = new AbortController();
//const signalPrimary = controllerPrimary.signal;
//const timeoutPrimary = setTimeout(() => controllerPrimary.abort(), 100);
//const controllerSecondary = new AbortController();
//const signalSecondary = controllerSecondary.signal;
//const timeoutSecondary = setTimeout(() => controllerSecondary.abort(), 100);
  try{
    chrome.tabs.query({}, function (tabs) {
      if(mon_started==false){
        for (var i = 0; i < tabs.length; i++) {
            if (tabs[i].url.toString().includes(Primary) | tabs[i].url.toString().includes(Secondary)) {
            if (tabs[i].url.toString().includes('http://')) {
                http_https = 'http://';
            } else if (tabs[i].url.toString().includes('https://')) {
                http_https = 'https://';
            } else {
                http_https = 'http://';
            }
            if(tab != i){
            tab = i;
            lasttabUsed = tabs[i].id;
              console.log('Tatget Url detected: ' + tabs[tab].url + ' on tab['+tab+']Id: ' + lasttabUsed);
              if(tabs[tab].url.toString().includes(Primary)){
                console.log('Monitoring target changed to ' + Primary);
              }else if(tabs[tab].url.toString().includes(Secondary)){
                console.log('Monitoring target changed to ' + Secondary);
              }}
            mon_started = true;
          }}}
          
      if(mon_started){
        currenturl = tabs[tab].url.toString();
          if (!(currenturl.includes(Primary) | currenturl.includes(Secondary))) {
            console.log(lasttabUsed + ' Url !=  (' + Primary +', ' +Secondary+')  '  + hours + ':' + minutes + ':' + seconds);
            mon_started = false;
          }
        }
    });

    if(mon_started){
    fetch('http://localhost:9000/connect', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ action: 'connect' }),
    })
    .then(response => response.text())
    .then(data => {
      if (data.includes('Python and Extension are successfully communicated')){
        get_endpoint = true
      }
    })
    .catch(
 //     console.log('Not connected to the program, run (Server_viewer.exe)'),
    );
  
  
  if(get_endpoint){
    
    fetch('http://localhost:9000/endpoint', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ action: 'js2py' }),
    })
    .then(response => response.text())
    
    .then(data => {
    })
    .catch(error =>{}
//      console.log('Not connected to the program, run (Server_viewer.exe)'),
    );
      
    fetch('http://localhost:9000/log', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ action: 'js2py_log' }),
    })
    .then(response => response.text())
    .then(data => {
      console.log(data);
      if(data.includes('127.0.0.1') === true && data.includes('8181') === true && Secondary_Down === false && Servers_Are_Down === false){
        chrome.tabs.update(lasttabUsed, { active: true, url: http_https + Primary });
        Secondary_Down = true;
        fetch('http://localhost:9000/endpoint', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ action: 'Server_48_2_Server_47' }),
        });
      }
      else if(data.includes('127.0.0.1')===true && data.includes('8080')===true && Primary_Down === false && Servers_Are_Down === false){
        chrome.tabs.update(lasttabUsed, { active: true, url: http_https + Secondary });
        Primary_Down = true;
        fetch('http://localhost:9000/endpoint', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ action: 'Server_47_2_Server_48' }),
        });
      }
      else if(data.includes('127.0.0.1')===true && data.includes('8080')===true && data.includes('8181')===true && Servers_Are_Down === false){
        Servers_Are_Down = true;
        fetch('http://localhost:9000/endpoint', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ action: 'Servers_down' }),
        });
      }
      else if(!(data.includes('127.0.0.1') & data.includes('8181')) & Servers_Are_Down == true){
        chrome.tabs.update(lasttabUsed, { active: true, url: http_https + Secondary });
        Secondary_Down = false;
        Servers_Are_Down = false;
        fetch('http://localhost:9000/endpoint', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ action: '48_server_up' }),
        });
      }
      else if(!(data.includes('127.0.0.1') & data.includes('8080')) & Servers_Are_Down == true){
        chrome.tabs.update(lasttabUsed, { active: true, url: http_https + Primary });
        Primary_Down = false;
        Servers_Are_Down = false;
        fetch('http://localhost:9000/endpoint', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ action: '47_server_up' }),
        });
      }
      if((data.includes('127.0.0.1') === false && data.includes('8080') === false && data.includes('8181') === false)){
        Primary_Down = false;
        Secondary_Down = false;
        Servers_Are_Down = false;
      }
    })
    .catch(
//      console.log('Not connected to the program, run (Server_viewer.exe)'),
    );
  }
}
  }catch(err){
    console.log(err + '   ' + hours+':'+minutes+':'+seconds);
    mon_started = false;
  }
},1000);
