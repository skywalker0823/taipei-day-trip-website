//fetch GET 訂單資訊


async function thanks(){
  const options = {
    method: "GET",
    headers: {
      "content-type": "application/json",
      "X-CSRF-TOKEN": getCookie("csrf_access_token"),
    },
  };
  let uniq_id=window.location.href
  l=uniq_id.split('=')

  const response = await fetch("../api/orders/"+l[1], options);
  const result = await response.json();
  tk_order=document.getElementById("tk_order")
  if(result.error){
      tk_order.innerHTML=""
      err_mess = document.createElement("div");
      mess = document.createTextNode("查無資料");
      err_mess.appendChild(mess);
      tk_order.appendChild(err_mess);
      return
  }

console.log(result)
  if(result.data==null){
      tk_order.innerHTML=""
      err_mess=document.createElement("div")
      mess=document.createTextNode("查無資料")
      err_mess.appendChild(mess)
      tk_order.appendChild(err_mess)
      return
}
thank=document.createElement("div");
you=document.createTextNode("Thank you")
thank.appendChild(you)
text1 = document.createTextNode("以下為訂單編號及預定行程");
span1=document.createElement("span")
span1.setAttribute("class","uni_id")
span1.setAttribute("id","uni_id")
text2 = document.createTextNode("如有問題可向洽詢客服或致電詢問");

tk_order.appendChild(thank)
tk_order.appendChild(text1)
tk_order.appendChild(span1)
tk_order.appendChild(text2)





uni_id=document.getElementById("uni_id")
tk_list = document.getElementById("tk_list");
//將訊息貼至畫面
//個資
let info=result.data.contact;
//編號
let id=result.data.number
uni_id.innerHTML=id
//金額
let price = result.data.price;
//行程

for(trip of result.data.trip){
  console.log(trip);
  //建立單一景點方匡
  let tk_site=document.createElement("div")
  tk_site.setAttribute("class","tk_site")
  //圖片
  let tk_img = document.createElement("img");
  tk_img.setAttribute("class", "book_where_site_img");
  tk_img.setAttribute("src", trip.attraction.image);

  //文字
  //文字匡
  let tk_site_info=document.createElement("div");
  tk_site_info.setAttribute("class","tk_site_info")
  //文字-名稱
  let site_name=document.createElement("div")
  site_name.setAttribute("class","cata_1")
  let name=document.createTextNode(trip.attraction.name)
  site_name.appendChild(name)
  //文字-地址
  let site_add=document.createElement("div");
  site_add.setAttribute("class", "book_info_c");
  let add=document.createTextNode(trip.attraction.address)
  site_add.appendChild(add)
  //文字-日期
  let site_date=document.createElement("div");
  site_date.setAttribute("class", "book_info_c");
  let date=document.createTextNode(trip.date)
  site_date.appendChild(date)
  //文字-時間
  let site_time=document.createElement("div");
  site_time.setAttribute("class", "book_info_c");
  let time=document.createTextNode(trip.time)
  site_time.appendChild(time)
  //裝進文字匡
  tk_site_info.appendChild(site_name)
  tk_site_info.appendChild(site_add)
  tk_site_info.appendChild(site_date)
  tk_site_info.appendChild(site_time)


  //裝進單一容器
  tk_site.appendChild(tk_img)
  tk_site.appendChild(tk_site_info)


  //裝進總容器
  tk_list.appendChild(tk_site)

  //資料

}
console.log(info,id,price)



}
