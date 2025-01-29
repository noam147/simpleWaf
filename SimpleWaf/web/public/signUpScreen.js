let SERVER_ADDRESS = "127.0.0.1"

let signUpform = document.getElementById('signUpForm');
signUpform.addEventListener('submit', async(event) => {
    event.preventDefault(); // Prevent the form from reloading the page

    let hostName = document.getElementById("hostNameInput").value;
    alert(typeof(hostName))
    let name = document.getElementById('userNameInput').value;
    let password = document.getElementById('passwordInput').value;
    let passwordConfirm = document.getElementById('passwordConfirmInput').value;
    let email = document.getElementById('emailInput').value;
    if(password != passwordConfirm)
    {
        alert("passwords doesnt match")
    }
    send_to_server(hostName,name,password,email);
})

function send_to_server(host_name,username,password,email) {
    fetch( "/signUp", {
        method: "POST", // Specifies the HTTP method
        headers: {
            "Host":SERVER_ADDRESS,
            "Content-Type": "application/json" // Sets the appropriate headers
        },
        body: JSON.stringify({ "host_name":host_name,"username": username ,"password":password,"email":email}) // Converts the data to JSON format
    })
    .then(response => {
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.json(); // Parses the JSON response
    })
    .then(data => {
        console.log("Server response:", data); // Handle success
    })
    .catch(error => {
        console.error("Error occurred:", error); // Handle errors
    });
}
