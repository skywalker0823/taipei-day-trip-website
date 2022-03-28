//接收到頁面HTML載入後，執行fetch取得API單一景點資料
//先假設這邊會拿到照片陣列 及資訊 以JS方式將圖片及html以外資料加上


let counter=1
function attr(){
  let now=window.location.href
  // console.log(window.location.pathname)
  now=now.split("/")
  fetch('/api/attraction/'+now[4])
  .then(function(response) {
    return response.json();
  })
  .then(function(datas){
    if(datas.error==true){
      document.getElementById("att_sec").innerHTML="";
      document.getElementById("rolwer").innerHTML="";
      document.getElementById("att_sec").innerHTML="查無資料";
    }else{
      let name=datas.data.name
      let cat=datas.data.category
      let mrt=datas.data.mrt
      let descr=datas.data.description
      let addr=datas.data.address
      let trans=datas.data.transport
      let imgs=datas.data.images
      
      //圖片放置處
      let pic_box=document.getElementById("roller_start");
      //點點處理區
      let pointer=document.getElementById("pointer");
      
      //地名
      document.getElementById("roller_name").innerHTML=name;

      //類別與捷運特殊處理
      let mrtncat=cat+" at "+mrt;
      document.getElementById("roller_cat").innerHTML=mrtncat;

      //敘述
      document.getElementById("descr").innerHTML=descr;
      //地址
      document.getElementById("addr").innerHTML=addr;
      //交通
      document.getElementById("trans").innerHTML=trans;
      //小圈點放置位置
      let dots=document.getElementById("pointer");
      //圖片放置盒 pic_box
      //圖片陣列imgs
      //創建圖片標籤
      //創建小圈點
      for(img of imgs){
        pic=document.createElement("img");//link?=>img
        dot=document.createElement("li");

        pic.src=img;//原.src
        pic.className="site_pics";
        pic.id="pic"+counter;
        
        dot.className="dots"
        // dot.innerHTML=".";
        dot.id="dot"+counter;
        pic_box.appendChild(pic);
        dots.appendChild(dot);
        if(counter==1){
        pic.style.display="block";
        document.getElementById("dot1").style.background="black";
      }else{pic.style.display="none"};
        counter+=1;
      }
      counter--;
      console.log("共",counter);
      //目前第一圖片為className=vis 其餘圖片為className=invis
      //以層疊方式 控opacity改變圖片出現與否
      //第一載入的工作到此結束
      //目前狀態為第一張現形 其餘隱形
      
    }
  })
};



let now_where=1
function clicker(h){
  let pics=document.getElementsByClassName("site_pics");
  document.getElementById("dot"+now_where).style.background="white"
  for(one_pic of pics){
    one_pic.style.display="none";
    //全體熄燈
  }
  if(h=="roll_r"){
    //讓下一張圖片被出現 其他改為invis
    now_where++;
    if(now_where==counter+1){
      now_where=1
      console.log(now_where)
      show_time=document.getElementById("pic"+now_where);
      show_time.style.display="block";
      document.getElementById("dot"+now_where).style.background="black";

    }else{console.log(now_where);
      show_time=document.getElementById("pic"+now_where);
      show_time.style.display="block";
      document.getElementById("dot"+now_where).style.background="black";
    }

  }else if(h=="roll_l"){
    //讓上一張圖片出現 其他invis
    now_where--;
    if(now_where==0){
      now_where=counter
      console.log(now_where)
      show_time=document.getElementById("pic"+now_where);
      show_time.style.display="block";
      document.getElementById("dot"+now_where).style.background="black";

    }else{console.log(now_where)
      show_time=document.getElementById("pic"+now_where);
      show_time.style.display="block";
      document.getElementById("dot"+now_where).style.background="black";
    }
  };
};

//圈圈點擊切換? 經由now_where

function tt(m_or_e){
  fee=document.getElementById("rl_f");
  console.log(m_or_e.value)
  if(m_or_e.value=="tt_e"){
    rl_f.innerHTML="";
    rl_f.innerHTML="新台幣 2500 元"
  }else{rl_f.innerHTML="新台幣 2000 元"}
};


//預定行程 擷取 景點id 日期 金額(同時代表上下天)   以一組特殊號碼表達之
//fetch資料庫 若登入 記住(append)其預定資訊 並導至booking.html
//若無登入 將會有其他提示 網站暫時不做動作

let order_data = document.getElementById("order_data");

async function confirm(){
  let site=window.location.href.split("/")[4];
  let date=document.getElementById("order_data").value;
  let price = document.getElementById("rl_f").innerHTML.match(/\d/g).join("");
  let time
  if(price==2500){time="afternoon"}else{time="morning"}
  console.log(site,date,time,price);
  if(date==false){
    console.log("日期要填拉")
    // order_data.classList.remove("input_d")
    // order_data.classList.add("input_e")
    order_data.style.background = "rgb(207 69 69)";
    setTimeout(() => {
      order_data.style.background="white"
    }, 500);
    return null;
  }
  const options = {
    method: "POST",
    headers: {
      "content-type": "application/json",
      "X-CSRF-TOKEN": getCookie("csrf_access_token"),
    },
    body: JSON.stringify({ attractionId: site, date: date, time: time,price:price }),
  };
  const response = await fetch("../api/booking", options);
  const result = await response.json();
  if(result.ok){
    if (date == false) {
      console.log("日期要填拉");
      return null;
    }else{window.location.replace("../booking")}
    //畫面移交至booking
  }else{loger_on()}

}