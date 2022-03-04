
function matchPasswd(p1,p2){
    if(p1 != p2){

        return false;
    }

}

window.onload = () => {
    var p1 = document.getElementById("password");
    var p2 = document.getElementById("confirm");

    p1.addEventListener("change",function(){
        if(p2.value != ""){
            if(p1.value !== p2.value){
                document.getElementById("passwordHelp").classList.remove("visually-hidden")
            } else {
                document.getElementById("passwordHelp").classList.add("visually-hidden")
            }
        }
    });
    p2.addEventListener("change",function(){
        if(p1.value != ""){
            if(p1.value !== p2.value){
                document.getElementById("confirmHelp").classList.remove("visually-hidden");
                document.getElementById("confirmHelp").classList.add("test")
            } else {
                document.getElementById("confirmHelp").classList.add("visually-hidden")
            }
        }
    });
}