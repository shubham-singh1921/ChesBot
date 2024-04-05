const btnStart =document.getElementById("btnStart")
const btnStop =document.getElementById("btnStop")
const btnSendHtml = document.getElementById("sendHtml")
const commandInput = document.getElementById("commandInput")

function sendMsgToMainScript(type,msg){
    browser.tabs.query({ active: true, currentWindow: true }, (tabs) => {
        const activeTabId = tabs[0].id;
        browser.tabs.sendMessage(activeTabId, { type: type, data:msg});
    });
}

btnStart.addEventListener("click",function(){
  sendMsgToMainScript("ACTION","START");
})

btnStop.addEventListener("click",function(){
    sendMsgToMainScript("ACTION","STOP");
})

btnSendHtml.addEventListener("click",function(){
    sendMsgToMainScript("MSG",{type:"COMMAND",data:commandInput.value})
    commandInput.value = ""
})