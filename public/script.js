

let next;
let words;
function site_in(){
  fetch('/api/attractions?page=0')
  .then(function(response) {
    return response.json();
  })
  .then(function(datas){
    next=datas.nextPage
    let data=datas.data//這裡是景點12陣列
    for(site of data){
      // console.log(site["id"],site["name"],site["images"][0],site["mrt"],site["category"])
      //圖片
      let pic=site["images"][0];
      //景名
      let name=site["name"];
      //捷運
      let mrt=site["mrt"];
      //類別
      let cat=site["category"];

      //起始點
      let pic_in = document.getElementById("pic_in");
      //產生新的單一div aka.box
      let box=document.createElement("a");
      box.href="/attraction/"+site["id"]
      box.className="box";
      box.id="box"+site["id"]
      box.setAttribute("onclick","target(this.id)")
      //創建圖片標籤
      let pic_here = document.createElement("img");
      pic_here.className = "pic_here";
      //創建文字標籤
      let name_here = document.createElement("p");
      name_here.className="name_here";
      site_name=document.createTextNode(name)
      //創建下方區域
      let infos = document.createElement("div");
      infos.className="infos";
      //創建左
      let info1 = document.createElement("div");
      info1.className = "info1";
      info1i=document.createTextNode(mrt)
      //創建右
      let info2 = document.createElement("div");
      info2.className = "info2";
      info2i=document.createTextNode(cat)
      //將素材裝進容器
      pic_here.src = pic;
      pic_in.appendChild(box).appendChild(pic_here);
      pic_in.appendChild(box).appendChild(name_here).appendChild(site_name);
      pic_in.appendChild(box).appendChild(infos).appendChild(info1).appendChild(info1i);
      pic_in.appendChild(box).appendChild(infos).appendChild(info2).appendChild(info2i);
    };
  })
};


function more(id="page="+next,keywords="&keyword="+words){
  console.log("more!",words,"next!:",next)
  if(words==undefined){words=""};
  // keyw=document.getElementById("s_bar").value;

  //---ckecking---
  if(next==null || next==0){return null};

  // keywords="&"+"keyword="+keyw;
  fetch('/api/attractions?'+id+keywords)
  .then(function(response) {
    return response.json();
  })
  .then(function(datas){
    next=datas.nextPage
    let data=datas.data;//這裡是景點12陣列
    // document.getElementById(id).id="page="+next;
    for(site of data){
      // console.log(site["id"],site["name"],site["images"][0],site["mrt"],site["category"])
      //圖片
      let pic=site["images"][0];
      //景名
      let name=site["name"];
      //捷運
      let mrt=site["mrt"];
      //類別
      let cat=site["category"];

      //起始點
      let pic_in = document.getElementById("pic_in");
      //產生新的單一div aka.box
      let box=document.createElement("a");
      box.href="/attraction/"+site["id"]
      box.className="box";
      box.id="box"+site["id"]
      box.setAttribute("onclick","target(this.id)")
      //創建圖片標籤
      let pic_here = document.createElement("img");
      pic_here.className = "pic_here";
      //創建文字標籤
      let name_here = document.createElement("p");
      name_here.className="name_here";
      site_name=document.createTextNode(name)
      //創建下方區域
      let infos = document.createElement("div");
      infos.className="infos";
      //創建左
      let info1 = document.createElement("div");
      info1.className = "info1";
      info1i=document.createTextNode(mrt)
      //創建右
      let info2 = document.createElement("div");
      info2.className = "info2";
      info2i=document.createTextNode(cat)
      //將素材裝進容器
      pic_here.src = pic;
      pic_in.appendChild(box).appendChild(pic_here);
      pic_in.appendChild(box).appendChild(name_here).appendChild(site_name);
      pic_in.appendChild(box).appendChild(infos).appendChild(info1).appendChild(info1i);
      pic_in.appendChild(box).appendChild(infos).appendChild(info2).appendChild(info2i);
    };
  })
};


window.addEventListener('scroll', () => {
  if(window.scrollY + window.innerHeight >= document.documentElement.scrollHeight){
    console.log("scrolled and more!")
    more();
  }
});


function search(){
  console.log("search!")
  next=0;
  document.getElementById("pic_in").innerHTML=""
  words=document.getElementById("s_bar").value;
  fetch('/api/attractions?page='+next+"&keyword="+words)
  .then(function(response) {
    return response.json();
  })
  .then(function(datas){
    if(datas.error==true){
      document.getElementById("pic_in").innerHTML="";
      document.getElementById("pic_in").innerHTML="查無資料";

    }else{
    // document.getElementById("pic_in").innerHTML="";
    next=datas.nextPage
    let data=datas.data;//這裡是景點12陣列
    
    for(site of data){
      // console.log(site["id"],site["name"],site["images"][0],site["mrt"],site["category"])

      //圖片
      let pic=site["images"][0];
      //景名
      let name=site["name"];
      //捷運
      let mrt=site["mrt"];
      //類別
      let cat=site["category"];

      //起始點
      let pic_in = document.getElementById("pic_in");
      //產生新的單一div aka.box
      let box=document.createElement("a");
      box.href="/attraction/"+site["id"]
      box.className="box";
      box.id="box"+site["id"]
      box.setAttribute("onclick","target(this.id)")
      //創建圖片標籤
      let pic_here = document.createElement("img");
      pic_here.className = "pic_here";
      //創建文字標籤
      let name_here = document.createElement("p");
      name_here.className="name_here";
      site_name=document.createTextNode(name)
      //創建下方區域
      let infos = document.createElement("div");
      infos.className="infos";
      //創建左
      let info1 = document.createElement("div");
      info1.className = "info1";
      info1i=document.createTextNode(mrt)
      //創建右
      let info2 = document.createElement("div");
      info2.className = "info2";
      info2i=document.createTextNode(cat)
      //將素材裝進容器
      pic_here.src = pic;
      pic_in.appendChild(box).appendChild(pic_here);
      pic_in.appendChild(box).appendChild(name_here).appendChild(site_name);
      pic_in.appendChild(box).appendChild(infos).appendChild(info1).appendChild(info1i);
      pic_in.appendChild(box).appendChild(infos).appendChild(info2).appendChild(info2i);
    };
  }
  })
};

// --------      

// 點擊即可以顯示目標id
target=(id)=>{
  console.log(id)
}

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

function tt(m_or_e){
  fee=document.getElementById("rl_f");
  console.log(m_or_e.value)
  if(m_or_e.value=="tt_e"){
    rl_f.innerHTML="";
    rl_f.innerHTML="新台幣 2500 元"
  }else{rl_f.innerHTML="新台幣 2000 元"}
};
