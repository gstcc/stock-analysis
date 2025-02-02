

window.onload = () => {
    const rpt_psw = document.getElementById('rpt_password');
    const rpt_psw_error = document.getElementById('rpt_password_error');

    rpt_psw.addEventListener('input', function() {
        if (rpt_psw.classList.contains('error')) {
            rpt_psw.classList.remove('error');
            rpt_psw_error.style.display = 'none';
        }
      });
}