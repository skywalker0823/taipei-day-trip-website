function site_in(){
    fetch('/api/attractions?page=0')
  .then(function(response) {
    return response.json();
  })
  .then(function(datas) {
    let data=datas.result.results
    let counter=1
    for(site of data){
        //console.log(site.stitle,site.file.toLowerCase().split("jpg")[0]+"jpg")
        let site_pic=site.file.toLowerCase().split("jpg")[0]+"jpg";//圖片兒
        let pic_in=document.getElementById("pic_in");//圖片從這開始放
        
        let new_space=document.createElement("div");//產生新的div
        new_space.className="box";//加上classname
        new_space.id="box"+counter;//為每個div加上個別id
        let pic_here=document.createElement("img");
        let site_name_space=document.createElement("p");

        pic_here.src=site_pic;//把圖片網址嵌進去src
        site_name_space.className="pic_text";
        let site_name=document.createTextNode(site.stitle);//地名
        
        pic_in.appendChild(new_space).appendChild(pic_here);
        pic_in.appendChild(new_space).appendChild(site_name_space).appendChild(site_name);

        counter+=1 ;
        if(counter>9){
            document.getElementById(new_space.id).style.display="none"
        };

    };
  });
};

// function burger_list(){
//     var logo_list=document.getElementById("menu_outer");
//     // if(logo_list.style.display=="none"){
//     //     logo_list.style.display="block"
//     // }else{logo_list.style.display="none"}
//     logo_list.classList.toggle("hide")
//     logo_list.classList.toggle("out")
// };
//記住目前的counter->每點一次more()點亮額外八張圖片1~8已開 9~16 17~24以此類推
// let now_where=9


// function more(){
//     if(document.getElementById("box"+now_where).style.display=="none"){
//     for(let counter=now_where;counter<now_where+8;counter++){
//         document.getElementById("box"+counter).style.display="flex";
//     }}
//     // else if(document.getElementById("box18").style.display=="none"){
//     //     for(let counter=now_where;counter<now_where+8;counter++){
//     //         document.getElementById("box"+counter).style.display="flex";
//     //     }
//     // }
//     now_where+=8;
//     console.log(now_where)//這裡是17
// };