// Copyright (c) 2012 The Chromium Authors. All rights reserved.
// Use of this source code is governed by a BSD-style license that can be
// found in the LICENSE file.

var lastTabId = 0;
var tab_clicks = {};

// dict: {tab.id : url}  // only bilibili
var dict_tab_url = new Array();
// {aid : res}
var dict_aid_res = new Array();

chrome.tabs.onActivated.addListener(function(activeInfo) {
  var tabId = activeInfo.tabId;
  console.log("changed");
  lastTabId = tabId;
  chrome.pageAction.show(lastTabId);

  checkurl_setvalue(tabId, dict_tab_url[tabId]);

});

chrome.tabs.onUpdated.addListener(function (id, info, tab) {
  console.log("update");
  if (tab.status === 'loading') {
      //console.log(id, tab.url);
      
      checkurl_setvalue(id, tab.url);

  }
});

chrome.tabs.onRemoved.addListener(function (tabId, removeInfo){

})

chrome.tabs.query({active: true, currentWindow: true}, function(tabs) {
  lastTabId = tabs[0].id;
  chrome.pageAction.show(lastTabId);
});

// Called when the user clicks on the page action.
chrome.pageAction.onClicked.addListener(function(tab) {
  console.log("click");
  
});

function checkurl_setvalue(tid, url){
  dict_tab_url[tid] = url;
  var url = new URL(url);
      
  //判断是否是bilibili 
  if(url.host == "www.bilibili.com" &&
     url.pathname.substring(0, 9) == "/video/av"){
        var aid_reg = /av([\d]+)/;
        var aid = parseInt(url.pathname.match(aid_reg)[1]);

        //记录当前tag对应的aid
        //console.log(tid, aid);
        

        //看看结果是否已存在
        if(dict_aid_res[aid] != null){
          setIcon(dict_aid_res[aid], tid);
          return;
        }

        //结果还不存在
        dict_aid_res[aid] = 9; //请求服务器
        setIcon(dict_aid_res[aid], tid);
        getValue(aid, tid);
        //dict_aid_res[aid] = getValue(aid);
        //setIcon(dict_aid_res[aid], tid);

     }
}

function setIcon(value, tabId){
    

    var Current = value;
    console.log("Icon: " + Current);
    chrome.pageAction.setIcon({path: 'icon' + Current + '.png', tabId: tabId});
    chrome.pageAction.show(tabId);
}

function sleep(delay) {
  var start = (new Date()).getTime();
  while ((new Date()).getTime() - start < delay) {
    continue;
  }
}

function getValue(aid, tid){
    //sleep(5000);
    
    const Http = new XMLHttpRequest();
    const url = 'http://206.189.33.7/get_res.php?aid=' + aid.toString();
    console.log(url);
    Http.open("GET", url);
    Http.send();

    Http.onreadystatechange=(e)=>{
      console.log("recv:" + Http.responseText);
      var ret_val = Http.responseText;
      if (ret_val=="0.0" || ret_val=="0.5" || ret_val=="1.0"){
          dict_aid_res[aid] = ret_val;
          setIcon(ret_val, tid);
      }
      return 1;
    }

    return;
}

