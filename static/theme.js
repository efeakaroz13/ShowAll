/*
	Author:Efe Akaröz
	15/05/2022

*/
function changeTheme(){
      
  if(window.matchMedia('(prefers-color-scheme: dark)').matches){
    document.getElementById("icon").href = "/static/logolight.png"
  }else{
    document.getElementById("icon").href = "/static/logodark.png"
  }


}
changeTheme()
setInterval(changeTheme,1000)



function order(model){
	window.location.assign("/order/"+model);
}
const getCookieValue = (name) => (
	document.cookie.match('(^|;)\\s*' + name + '\\s*=\\s*([^;]+)')?.pop() || ''
)