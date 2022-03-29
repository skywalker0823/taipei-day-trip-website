

//此處將處理 取得預約景點資料 get 與 刪除預約資料delete
let fn = document.getElementById("find_no");
async function booker(){
  //直接自資料庫fetch使用者所有行程 並且堆疊至主畫面
  const options = {
    method: "GET",
    headers: {
      "content-type": "application/json",
      "X-CSRF-TOKEN": getCookie("csrf_access_token"),
    },
  };
  const response = await fetch("../api/booking", options);
  const result = await response.json();
  //這裏應當接回所有預定資料 [即景點資訊+使用者選擇時間]之列表
  //並完成頁面渲染 務必減少使用innerHTML
  if (result.data) {
    console.log(result.data);
    fn.style.display="none"
  } else {
    console.log({ error: true, message: "查詢預定行程前請先登入" });
    window.location.replace("../")
  }
  if(result.data.length==0){
    console.log("there is nothong ordered")
    fn.style.display="flex"
    //無資料時的畫面處理
    document.getElementById("boorder").style.display="none"
    document.getElementById("remover").innerHTML=null
    let b_foot=document.getElementById("book_foot");

    return false
  }else{fn.style.display="none"}
  //先嘗試單一資料
  // console.log(result.data[0]);
  // console.log("節點1",result.data)
  for(i of result.data){
  //尋找歸屬
  // console.log("節點2",i)
  from = document.getElementById("book_start");
  //生成文字與圖片
  let true_id = i["attraction"]["true_id"];
  let img = i["attraction"]["image"];
  let name = i["attraction"]["name"];
  let date = i["date"];
  //時間需做處理
  let time = i["time"];
  if(time=="morning"){
    time="早上九點到下午四點"
  }else{time="下午兩點到晚上九點"}
  let fee = i["price"];
  let add = i["attraction"]["address"];
  // console.log(name, date, time, fee, add);
  //建立畫面並匯入資料 with createElement&appendChild&setAttribute

  //圖片的家
  let b_img = document.createElement("img");
  b_img.setAttribute("id", "trip_img=" + true_id);//測試運作 不用全加
  b_img.setAttribute("class", "book_where_site_img");
  b_img.setAttribute("src", img);
  //圖片之上的picture
  let b_pic = document.createElement("picture");
  b_pic.setAttribute("class", "book_where_site");
  b_pic.appendChild(b_img);
  let b_bw = document.createElement("div");
  b_bw.setAttribute("class", "book_where");
  b_bw.appendChild(b_pic);
  //裝載 圖片區域完畢

  //項目標題殼
  // let catalog=document.createElement('div')
  // catalog.setAttribute("class","catalog")
  //標題
  let cata_1=document.createElement("div")
  cata_1.setAttribute("class","cata_1")
  trip_t=document.createTextNode("台北一日遊 :")
  cata_1.appendChild(trip_t)
  //日期
  let cata_2 = document.createElement("div");
  cata_2.setAttribute("class", "cata_2");
  trip_d = document.createTextNode("日期 :");
  cata_2.appendChild(trip_d);
  //時間
  let cata_3 = document.createElement("div");
  cata_3.setAttribute("class", "cata_2");
  trip_t=document.createTextNode("時間 :")
  cata_3.appendChild(trip_t)
  //費用
  let cata_4 = document.createElement("div");
  cata_4.setAttribute("class", "cata_2");
  trip_f = document.createTextNode("費用 :");
  cata_4.appendChild(trip_f);
  //地點
  let cata_5 = document.createElement("div");
  cata_5.setAttribute("class", "cata_2");
  trip_a = document.createTextNode("地址 :");
  cata_5.appendChild(trip_a);
  //主要資訊 注意加上true_id地點與可能使用方式
  //地名
  let b_name=document.createElement("div");
  b_name.setAttribute("class","book_info_name")
  b_name.setAttribute("id","trip_name="+true_id);
  name=document.createTextNode(name)
  b_name.appendChild(cata_1)
  b_name.appendChild(name)
  //日期
  let b_date=document.createElement("div")
  b_date.setAttribute("class","book_info_c")
  b_date.setAttribute("id","trip_date="+true_id)
  date=document.createTextNode(date)
  b_date.appendChild(cata_2)
  b_date.appendChild(date);
  //時間
  let b_time=document.createElement("div");
  b_time.setAttribute("class","book_info_c")
  b_time.setAttribute("id","trip_time="+true_id)
  time=document.createTextNode(time)
  b_time.appendChild(cata_3);
  b_time.appendChild(time)
  //金額
  let b_cost = document.createElement("div");
  b_cost.setAttribute("class", "book_info_cc");
  b_cost.setAttribute("id", "trip_cost="+true_id);
  fee=document.createTextNode(fee)
  b_cost.appendChild(cata_4);
  b_cost.appendChild(fee);
  //地址
  let b_add = document.createElement("div");
  b_add.setAttribute("class", "book_info_c");
  b_add.setAttribute("id", "trip_add="+true_id);
  add=document.createTextNode(add)
  b_add.appendChild(cata_5)
  b_add.appendChild(add);
  //裝進book_info
  let b_bi=document.createElement("div")
  b_bi.setAttribute("class","book_info")
  b_bi.appendChild(b_name)
  b_bi.appendChild(b_date)
  b_bi.appendChild(b_time);
  b_bi.appendChild(b_cost);
  b_bi.appendChild(b_add);
  //整合上兩者進class=booker
  let b_er=document.createElement("div")
  b_er.setAttribute("class","booker")
  b_er.appendChild(b_bi)
  b_er.appendChild(b_bw)
  //刪除鈕 以true_id方式呼喚刪除fetch
  b_d=document.createElement("div")
  b_d.setAttribute("class","book_cancel")
  b_d.setAttribute("id","del_id="+true_id)
  b_d.setAttribute("onclick","del_trip(this.id)")
  b_d_img=document.createElement("img")
  b_d_img.setAttribute("src","icon_delete.png")
  b_d.appendChild(b_d_img)
  //創建主要父親a_book並裝載之前元素完成
  abook=document.createElement("div")
  abook.setAttribute("class","a_book")
  abook.setAttribute("id","a_book="+true_id)

  abook.appendChild(b_bw)
  abook.appendChild(b_bi)
  abook.appendChild(b_d)
  //放進起點
  from.appendChild(abook);
  }
  render_price();
}

//刪除行程
async function del_trip(the_id){
  let id=the_id.split("=")[1]
  console.log(id);
  let options = {
    method: "DELETE",
    headers: {
      "content-type": "application/json",
      "X-CSRF-TOKEN": getCookie("csrf_access_token"),
    },
    body: JSON.stringify({ id: id }),
  };
  const response = await fetch("../api/booking", options);
  const result = await response.json();
  if(result.ok){
    //可使用前端方式動態去除目標
    let tar=document.getElementById("a_book="+id)
    tar.remove();
    render_price();
  }else{console.log("error when deletion, did not login or else")}
}


render_price=()=>{
  let prices=document.getElementsByClassName("book_info_cc")
  let total_price=document.getElementById("total_price")
  let total=0
  for(p of prices){
    total += Number(p.innerHTML.split("</div>")[1]);
  }
  total_price.innerHTML=total
  if(total==0){
    fn.style.display="flex"
    document.getElementById("remover").innerHTML = null;
    document.getElementById("boorder").style.display = "none";
    document.getElementById("book_foot").className = "foot3";
  }else{document.getElementById("book_foot").className="foot2"}
}

// switch_mode=()=>{
//   let book_start=document.getElementById("book_start")
//   let catalog=document.getElementById("catalog")
//   if(book_start.className=="book"){
//     book_start.className="book_ori"
//     catalog.style.display="none"
//     //原版

//   }else{book_start.className="book"
//   catalog.style.display="flex"

//   //新版
// }
// }