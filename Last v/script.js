
async function submit() {

    const password = document.getElementById("password").value
    const username = document.getElementById("username").value
    

    fetch("http://127.0.0.1:8000/login/"+username+"/"+password)
        .then(res => res.json())
        .then(data => {
            if(data["bank-balance"]==401){
                alert("Wrong Password.\nTry again.")
            }
            else if(data["bank-balance"]==402){
                alert("Username does not exist.\nTry again.")
            }
            else{
                result_box = document.getElementById("result")
                result_box.classList.remove("hidden-container")
                accno = document.getElementById("accno")
                accno.innerHTML = "Your Account Number: " + data["acc-no"]   
                balance = document.getElementById("balance")
                balance.innerHTML = "Bank Balance: " + data["bank-balance"]    
            }
            })
}

async function showHiddenContainer() {

    const password=document.getElementById("password").value
    const username=document.getElementById("username").value

    fetch("http://127.0.0.1:8000/signup/" + username + "/" + password)
        .then(res => res.json())
        .then(data => {
            if (data["Error"]==403){
                alert("Username Already Exists.\nTry again.")}
            else{
                result_box = document.getElementById("result")
                result_box.classList.remove("hidden-container")
                accno = document.getElementById("accno")
                accno.innerHTML = "Your Account Number: " + data["acc-no"]   
                balance = document.getElementById("balance")
                balance.innerHTML = "Bank Balance: " + data["bank-balance"]}  
            })
    }
async function deposit() {
    const password = document.getElementById("password").value
    const username = document.getElementById("username").value
    const amt = document.getElementById("amt").value

    fetch("http://127.0.0.1:8000/deposit/" + username + "/" + password + "/" + amt)
        .then(res => res.json())
        .then(data => {
            balance = document.getElementById("balance")
            balance.innerHTML = "Bank Balance: " + data["bank-balance"]
            document . getElementById("money") .innerHTML = "Money deposited: " + amt
        })
}

async function withdraw() {
    const password = document.getElementById("password").value
    const username = document.getElementById("username").value
    const amt = document.getElementById("amt").value

    fetch("http://127.0.0.1:8000/withdraw/" + username + "/" + password + "/" + amt)
        .then(res => res.json())
        .then(data => {
            balance = document.getElementById("balance")
            balance.innerHTML = "Bank Balance: " + data["bank-balance"]
            document . getElementById("money") .innerHTML = "Money withdrawn: " + amt
        })
}



