
onSignUp = async (event) => {
    event.preventDefault();
    console.log("got here");
    const url = 'http://localhost:5000/tmp'; // Backend endpoint
    const data = {
        email: "test@tmp123",
        name: "Gustav"
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

} 

window.onload = () => {

}