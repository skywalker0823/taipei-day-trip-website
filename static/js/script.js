

let next;
let words;
let loading = document.getElementById("lds-ring");
let load_count=0
let wait_box=[]
let confirm=0

function site_in(){
  fetch('/api/attractions?page=0')
  .then(function(response) {
    return response.json();
  })
  .then(function(datas){
    next=datas.nextPage
    let data=datas.data//這裡是景點12陣列

    load_target=data.length

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
      // box.setAttribute("onclick","target(this.id)")
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



      wait_box.push(box.id);
      if (pic_here.addEventListener) {
        pic_here.addEventListener("load", () => {
          load_count += 1;
          if (load_count == load_target) {
            console.log("OK!");
            for(a_id of wait_box){
              document.getElementById(a_id).style.display="flex"
            }
            loading.style.display = "none";
            confirm=1
          };
        });
      }
      loading.style.display = "flex";
      document.getElementById(box.id).style.display = "none";




    };
  })
};


function more(id="page="+next,keywords="&keyword="+words){
  confirm=0
  console.log("more!",words,"next!:",next)
  if(words==undefined){words=""};
  // keyw=document.getElementById("s_bar").value;
  load_count = 0;
  //---ckecking---
  if(next==null || next==0){
    return null;
  };

  // keywords="&"+"keyword="+keyw;
  fetch('/api/attractions?'+id+keywords)
  .then(function(response) {
    return response.json();
  })
  .then(function(datas){
    next=datas.nextPage
    let data=datas.data;//這裡是景點12陣列

    wait_box=[]
    load_target = data.length;

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
      // box.setAttribute("onclick","target(this.id)")
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

      wait_box.push(box.id);
      if (pic_here.addEventListener) {
        pic_here.addEventListener("load", () => {
          load_count += 1;
          // console.log(wait_box)
          if (load_count == load_target) {
            console.log("OK!");
            for (a_id of wait_box) {
              document.getElementById(a_id).style.display = "flex";
            }
            // load_target-=load_count
            confirm=1
            loading.style.display = "none";
          }
        });
      }
      loading.style.display = "flex";
      document.getElementById(box.id).style.display = "none";
    };

  })
};


window.addEventListener('scroll', () => {
  if(window.scrollY + window.innerHeight >= document.documentElement.scrollHeight){
    if(confirm==0){
      return
    }
    console.log("scrolled and more!");
      more();
  }
});


function search(){
  confirm=1
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
      // box.setAttribute("onclick","target(this.id)")
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
