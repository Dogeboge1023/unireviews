function verifyPassword(){
    var password = document.getElementById("password").value;
    
    if(password == ""){
        document.getElementById("message").innerHTML = "FIll The Password";
        return false;
    }

    if(password.length < 8){
        document.getElementById("message").innerHTML = "Password Is Too Short"
        return false;
    }
    else{
        return true;
    }

}