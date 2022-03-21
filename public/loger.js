

let loger=document.getElementById("loger");
let mask=document.getElementById("mask");
let signer=document.getElementById('signer');
let tager=document.getElementById('tager');
let err_l=document.getElementById('err_login');
let err_s=document.getElementById('err_signup');
const mail_format = /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
switcher=(s)=>{
  if(s=="signup_sw"){
    loger.style.display="none";
    signer.style.display="block";
    err_s.innerHTML=null
  }else{
  loger.style.display="block";
  signer.style.display="none";
  err_l.innerHTML=null
  }
}

locker=()=>{
  window.scrollTo(0, 0);
}

loger_on=()=>{
  loger.style.display="block"
  mask.style.display="block"
  window.addEventListener("scroll", locker);
};

loger_off=()=>{
  loger.style.display="none"
  mask.style.display="none"
  signer.style.display="none"
  window.removeEventListener("scroll", locker);
};


//Model
//會員總控制 for signup/login/logout
//總是回傳json
async function linkin(acc,pss,name,method){
  return fetch("../api/user",{
    method: method,
    headers:{'content-type':'application/json',},
    body: JSON.stringify({email:acc,password:pss,name:name}),
  }).then(response=>response.json())
  .then((json_data)=>{
    return(json_data)
  })
}

//Controller
//點此開始茶豬料 GET req
//使用者需回傳自身帳號 且須為登入狀態，將接收到
// {"data": {"id": 1,"name": "彭彭彭","email": "ply@ply.com"}}
//null表示尚未登入
function getCookie(name) {
  const value = `; ${document.cookie}`;
  const parts = value.split(`; ${name}=`);
  if (parts.length === 2) return parts.pop().split(';').shift();
}

document.addEventListener("load", iden())
//window onload
async function iden(){
  // const data = await fetch('/api/user');
  // const result = await data.json();
  // if(result){
  //   //這裏已是整套的個人資料有登入者拿到資料 無登入者拿到{'data':null}
  //   console.log(result)
  // }else{throw new Error(result)}
  const options = {
    method: 'GET',
    credentials: 'same-origin',
    headers: {
      'X-CSRF-TOKEN': getCookie('csrf_access_token'),
    },
  };
  const response = await fetch('/api/user', options);
  const result = await response.json();
  if(result.data==null){
    console.log('使用者尚未登入',result)
  }else{
    tager.innerHTML="登出系統";
    tager.setAttribute("onclick","logout()")
    
  }
}

//Sign up part 註冊囉
//使用者需回傳 名字 帳號 密碼
//會接收到ok 或是包含錯誤訊息的error
async function signup(){
  let u_name=document.getElementById("u_name").value;
  let u_mail=document.getElementById("u_mail").value;
  let u_pass=document.getElementById("u_pass").value;
  if(u_name.length==0 || u_name.length==0 || u_pass.length==0){
    err_s.innerHTML="";
    err_s.innerHTML="就跟人生一樣，勿留空白"
    return null
  }
  if(u_mail.match(mail_format)){
    console.log("shall pass")
  }else{err_s.innerHTML="";err_s.innerHTML="郵件帳號不符格式";return null}
  const result = await this.linkin(u_mail,u_pass,u_name,'POST');
  if(result.ok){
    err_s.innerHTML="";
    err_s.innerHTML="註冊成功"
  }else{
    console.log(result.error)
    err_s.innerHTML=result.error;
  }
}

//登入
//使用者需傳回帳號與密碼
//會接收到ok 或是包含錯誤訊息的error
async function login(){
  let acc=document.getElementById("acc").value;
  let pss=document.getElementById("pss").value;
  if(acc.length==0 || pss.length==0){
    err_l.innerHTML="";
    err_l.innerHTML="空白是你給的浪漫";
    return null
  }
  if(acc.match(mail_format)){
    console.log("shall pass")
  }else{err_l.innerHTML="";err_l.innerHTML="郵件帳號不符格式";return null}
  const result = await this.linkin(acc,pss,'none','patch');
  if(result.ok){
    //登入成功，應需求做畫面變化
    // tager.innerHTML="你好!"+
    //在執行一次fetch?get
    console.log("hooray")
    console.log(result)
    window.location.reload();
  }else{
    console.log(result.error);
    err_l.innerHTML=result.error;
  }
    
    // throw new Error(result.error)
}

//登出 DELETE req
//使用者要傳回自身的帳號
//收到ok
async function logout(){
  let acc=document.getElementById("acc").value;
  const result = await this.linkin(acc,'none','none','DELETE')
  if(result.ok){
    console.log("登出成功")
    window.location.reload();
  }else{
    console.log('これは、ゲームであっても遊びではない')
  }
}

//View



