


//將要附加關鍵字if else
let next;
function site_in(){
  fetch('/api/attractions?page=0')
  .then(function(response) {
    return response.json();
  })
  .then(function(datas){
    next=datas.nextPage
    let data=datas.data//這裡是景點12陣列
    for(site of data){
      // console.log(site["name"],site["images"][0],site["mrt"],site["category"])
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
      let box=document.createElement("div");
      box.className="box";
      box.id="box"+site["id"]
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


function more(id="page="+next){
  console.log(next)
  keyw=document.getElementById("s_bar").value
  if(next==null){
    return null
  }
  if(keyw != null){keywords="&"+"keyword="+keyw}
  fetch('/api/attractions?'+id+keywords)
  .then(function(response) {
    return response.json();
  })
  .then(function(datas){
    next=datas.nextPage
    let data=datas.data;//這裡是景點12陣列
    // document.getElementById(id).id="page="+next;
    for(site of data){
      // console.log(site["name"],site["images"][0],site["mrt"],site["category"])
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
      let box=document.createElement("div");
      box.className="box";
      box.id="box"+site["id"]
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
    console.log("called!")
    more();
  }
});

//若搜尋結果大於一頁 跑search()並且戴上頁 "nextk"

function search(){
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
    key="on"
    // document.getElementById("pic_in").innerHTML="";
    next=datas.nextPage
    let data=datas.data;//這裡是景點12陣列
    for(site of data){
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
      let box=document.createElement("div");
      box.className="box";
      box.id="box"+site["id"]
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