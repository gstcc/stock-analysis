function bake_cookie(name, value) {
    var cookie = [name, '=', JSON.stringify(value), '; domain=.', window.location.hostname.toString(), '; path=/;'].join('');
    document.cookie = cookie;
}

function read_cookie(name) {
    var result = document.cookie.match(new RegExp(name + '=([^;]+)'));
    result && (result = JSON.parse(result[1]));
    return result;
}

function delete_cookie(name) {
    document.cookie = [name, '=; expires=Thu, 01-Jan-1970 00:00:01 GMT; path=/; domain=.', window.location.hostname.toString()].join('');
}

onLogin = async (event) => {
    event.preventDefault();
    const url = 'http://localhost:5000/login';
    const data = {
        "email": "user@example.com", 
        "password": "secure_password123"
    };
    try {
        const response = await fetch(url, {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
            },
            body: JSON.stringify(data),
          });
          console.log(response);
      
          if (response.ok) {
            const data = await response.json();
            bake_cookie("token", data.token);
            console.log('User logged in successfully:', data);
          } else {
            const error = await response.json();
            console.error('Error:', error);
          }
    } catch(err) {
        console.log(err);
    }
};

onSignUp = async (event) => {
    event.preventDefault();
    console.log("got here");
    const url = 'http://localhost:5000/tmp';
    const psw = document.getElementById("password").value;
    const rpt_psw = document.getElementById("rpt_password");
    console.log(rpt_psw.value);
    if (psw !== rpt_psw.value) {
      rpt_psw.classList.add("error");
      document.getElementById("rpt_password_error").style = "block";
    }
    const data = {
        email: document.getElementById("email").value,
        name: document.getElementById("username").value,
        password: psw
    };
    try {
        const response = await fetch(url, {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
            },
            body: JSON.stringify(data),
          });
      
          if (response.ok) {
            const data = await response.json();
            console.log('User registered successfully:', data);
          } else {
            const error = await response.json();
            console.error('Error:', error);
          }
    } catch(err) {
        console.log(err);
    }
};

window.onload = () => {

}