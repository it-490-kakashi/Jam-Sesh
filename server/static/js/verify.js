
function matchPasswd(p1,p2){
    if(p1 != p2){
        alert("Passwords did not match!");
        return false;
    }

}
var p1 = document.querySelector("#password");
var p2 = document.querySelector("#confirm");

p1.addEventListener("change",function(){
    if(p2.value != ""){
        matchPasswd(p1,p2);
    }
});
p2.addEventListener("change",function(){
    if(p1.value != ""){
        matchPasswd(p1,p2);
    }
});
