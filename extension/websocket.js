var ws;
var socket_status = false
function connectToServer(){
    let url = "ws://127.0.0.1:7890"
    ws = new WebSocket(url)
    ws.onopen = function(e){
        socket_status=true;
    }
    ws.onclose = function(e){
        socket_status = false;
    }
    ws.onFailure = function(e){
        socket_status = false;
    }
    ws.onmessage = function(e){

    }
}

function sendToServer(msg){
    if (!socket_status){
        connectToServer()
    }
    ws.send(JSON.stringify(msg))
}
connectToServer()

function sendMsgToMainScript(type,msg){
    browser.tabs.query({ active: true, currentWindow: true }, (tabs) => {
        const activeTabId = tabs[0].id;
        browser.tabs.sendMessage(activeTabId, { type: type, data:msg});
    });
}

browser.runtime.onMessage.addListener((message, sender, sendResponse) => {
    if(message.type=="MSG"){
  		try{
            sendToServer(message.data)
  		}catch(e){
  			sendMsgToMainScript("FEEDBACK",e)
  		}
  }
});