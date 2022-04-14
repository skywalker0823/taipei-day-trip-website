let member_card = document.getElementById("member_card");
let order_card = document.getElementById("order_card");
let member_info = document.getElementById("member_info");
let member_order = document.getElementById("member_order");




async function member(){
  console.log("member up");
  member_info.style.fontWeight = "800";
  member_order.style.fontWeight = "400";
  const options = {
    method: "GET",
    credentials: "same-origin",
    headers: {
      "X-CSRF-TOKEN": getCookie("csrf_access_token"),
    },
  };
  const response = await fetch("api/orders/all");
  const result = await response.json();
  console.log(result);


  //製作畫面MainCard
  let card = document.getElementById("card");


  //內區
  order_list = document.createElement("div");
  order_list.setAttribute("class", "order_list");


  if (result.length == 0) {
    console.log("沒豬料");
    nope = document.createElement("div");
    nope.setAttribute("class", "order_list_bar");
    no = document.createTextNode("查無資料");
    nope.appendChild(no);
    card.appendChild(nope);
    return;
  }

  //上半區
  order_list_bar = document.createElement("div");
  order_list_bar.setAttribute("class", "order_list_bar");

  //上半區內
  //概覽
  ol1_1 = document.createElement("div");
  ol1_1.setAttribute("class", "ol1");
  text=document.createTextNode("概覽")
  ol1_1.appendChild(text)

  //訂單編號
  ol1_2 = document.createElement("div");
  ol1_2.setAttribute("class","ol1");
  text=document.createTextNode("訂單編號")
  ol1_2.appendChild(text)

  //結帳金額
  ol1_3 = document.createElement("div");
  ol1_3.setAttribute("class", "ol1");
  text = document.createTextNode("結帳金額");
  ol1_3.appendChild(text)

  //詳細資訊
  ol1_4 = document.createElement("div");
  ol1_4.setAttribute("class", "ol1");
  text = document.createTextNode("詳細資訊");
  ol1_4.appendChild(text);

  //訂單資訊
  ol1_5 = document.createElement("div");
  ol1_5.setAttribute("class", "ol1");
  text = document.createTextNode("訂單狀態");
  ol1_5.appendChild(text);



  order_list_bar.appendChild(ol1_1);
  order_list_bar.appendChild(ol1_2);
  order_list_bar.appendChild(ol1_3);
  order_list_bar.appendChild(ol1_4);
  order_list_bar.appendChild(ol1_5);
  order_list.appendChild(order_list_bar);

  //訂單



  for (order of result) {
    //資料整理
    let attractions = order.attraction;
    let uniq_id = order.uniq_id;
    let fee = order.total;
    let status = order.status;

    //下半區
    one_order = document.createElement("div");
    one_order.setAttribute("class", "one_order");

    //下半區內
    //圖
    ol2_1 = document.createElement("div");
    ol2_1.setAttribute("class", "ol2");
    //產生圖片
    for (a_att of attractions) {
      a_img = document.createElement("img");
      a_href=document.createElement("a")
      a_href.setAttribute("href", "../attraction/" + a_att.attraction.id);
      a_img.setAttribute("class", "order_pic");
      pic = a_att.attraction.image;
      a_img.setAttribute("src", pic);
      a_href.appendChild(a_img)
      ol2_1.appendChild(a_href);
    }

    //訂單編號
    ol2_2 = document.createElement("div");
    ol2_2.setAttribute("class", "ol2");
    text = document.createTextNode(uniq_id);
    ol2_2.appendChild(text);

    //費用
    ol2_3 = document.createElement("div");
    ol2_3.setAttribute("class", "ol2");
    text = document.createTextNode(fee);
    ol2_3.appendChild(text);

    //http://192.168.1.103:3000/thankyou?number=202204123049
    //點我
    ol2_4 = document.createElement("a");
    ol2_4.setAttribute("class", "ol2");
    ol2_4.setAttribute("href","../thankyou?number="+uniq_id)
    text = document.createTextNode("點我");
    ol2_4.appendChild(text);

    //status
    ol2_5 = document.createElement("div");
    ol2_5.setAttribute("class", "ol2");
    if(status=="0"){
        status="已付款"
    }else{ststus="未完成"}
    text = document.createTextNode(status);
    ol2_5.appendChild(text);

    //裝載
    one_order.appendChild(ol2_1);
    one_order.appendChild(ol2_2);
    one_order.appendChild(ol2_3);
    one_order.appendChild(ol2_4);
    one_order.appendChild(ol2_5);

    order_list.appendChild(one_order);
  }
  card.appendChild(order_list);


};

//取得已成交訂單
//剩餘7-5 7-6 7-7

openInfo = () => {
  member_card.style.display = "flex";
  order_card.style.display = "none";
  member_info.style.fontWeight = "800";
  member_order.style.fontWeight = "400";
};
openOrder = () => {
  member_card.style.display = "none";
  order_card.style.display = "flex";
  member_order.style.fontWeight = "800";
  member_info.style.fontWeight = "400";
};

member_info.addEventListener("mouseover", () => {
  openInfo();
});
member_order.addEventListener("mouseover", () => {
  openOrder();
});

//查詢訂單可以導到當時頁面
document.getElementById("order_find").addEventListener("click",()=>{
    order_num = document.getElementById("book_input_2");
    if(order_num.value==""){
  order_num.style.borderColor = "red";
  setTimeout(() => {
    order_num.style.borderColor = "#E8E8E8";
  }, 500); 
    return
    }
    console.log(order_num.value)
    window.location.href="../thankyou?number="+order_num.value
})


input_mode = document.createElement("input");
input_mode.setAttribute("class", "book_input_2");
input_mode.setAttribute("id", "the_name");
// input_mode.setAttribute("placeHolder", name);
document.getElementById("cardName_father").appendChild(input_mode);
let name_bar=document.getElementById("cardName")
input_mode = document.getElementById("the_name");
input_mode.style.display = "none";


name_bar.addEventListener("click",()=>{

    console.log("change name")
    name_first=name_bar.innerHTML
    name_bar.style.display="none"
    input_mode.style.display="block"
    input_mode.value=name_first;
})

input_mode.addEventListener("focusout", () => {
    console.log("focus_out");
    new_name=document.getElementById("the_name")
    name_then = new_name.value;
    input_mode.style.display = "none";
    name_bar.style.display = "flex";
    if(name_first==name_then){
        console.log("not changed");
        return
    }else{
        if(name_then=="" || name_then==null){
            console.log('not a name')
            return
        }
        console.log("changed!")
        alter()

    }
});





async function alter() {
    const options = {
    method: "PUT",
    headers: {
        "content-type": "application/json",
        "X-CSRF-TOKEN": getCookie("csrf_access_token"),
    },
    body: JSON.stringify({ new_name: name_then ,for:"name"}),
    };
    const response = await fetch("../api/user", options);
    const result = await response.json();
    console.log(result);
    if(result.ok){
        name_bar.innerHTML = result.name;
    }else{
        console.log(result.error)
        return}
    
    // input_mode.setAttribute("placeHolder", result.name);
}


tip_tag = document.createElement("p");
tip_tag.setAttribute("class","tip_tag")
tip = document.createTextNode("*點擊更改");
tip_tag.appendChild(tip);
target=document.getElementById("cardName_father")
target.appendChild(tip_tag)


let cardpass=document.getElementById("cardpass")
cardpass.addEventListener("focus",()=>{
    cardpass.value=""
})



cardpass.addEventListener("focusout", () => {
  console.log("pass change attempt");

  new_pass = cardpass.value;
  if(new_pass=="" || new_pass==null){
      console.log("nothing changes")
      return
  } 
  alter_pss(new_pass)

});

  async function alter_pss(new_pass) {
    const options = {
      method: "PUT",
      headers: {
        "content-type": "application/json",
        "X-CSRF-TOKEN": getCookie("csrf_access_token"),
      },
      body: JSON.stringify({ new_pass: new_pass,"for":"password" }),
    };
    const response = await fetch("../api/user", options);
    const result = await response.json();
    if (result.ok) {
      console.log("密碼變更完成");
      cardpass.value="變更完成"
    } else {
      console.log("密碼變更失敗");
      cardpass.value = "密碼相同";
    }
  }
