function sendHtml(){
      const htmlContent = document.documentElement.outerHTML;
      browser.runtime.sendMessage({ type:"MSG", data:{type:"HTML",data: htmlContent }})
}

var send_interval;

browser.runtime.onMessage.addListener((message, sender, sendResponse) => {
      switch(message.type){
            case "ACTION":
                  if(message.data=="START"){
                        send_interval=setInterval(sendHtml,1000)
                  }else if(message.data=="STOP"){
                        clearInterval(send_interval)
                  }
            break;
            case "FEEDBACK":
                  console.log("[FEEDBACK]",message.data)
            return;
      }  
});