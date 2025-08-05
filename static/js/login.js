var formLogin = document.getElementById("formLogin")
var formRegister = document.getElementById("formRegister")
var titleForm = document.getElementById("title-form")

formLogin.addEventListener("submit", (e)=>{
    e.preventDefault()
    if (e.submitter.classList[1] === 'bg-btn2') {
        formLogin.classList.add("d-none")
        formRegister.classList.remove("d-none")
        titleForm.textContent = 'Únete a Spotify Rewards'
    } else {
        formLogin.submit(   )  
    }
})

formRegister.addEventListener("submit", (e)=>{
    e.preventDefault()
    if (e.submitter.classList[1] === 'bg-btn2') {
        formLogin.classList.remove("d-none")
        formRegister.classList.add("d-none")
        titleForm.textContent = 'Inicia sesión para continuar'
    } else {
        formRegister.submit(   )  
    }
})
