document.addEventListener("DOMContentLoaded", function () {
    const form = document.querySelector("form");
    const storageKey = "formularios_pendientes";

    // Detecta si el usuario está en línea o no
    function isOnline() {
        return navigator.onLine;
    }

    // Guarda los formularios pendientes en LocalStorage
    function guardarFormularioEnLocalStorage(data) {
        let formulariosGuardados = JSON.parse(localStorage.getItem(storageKey)) || [];
        formulariosGuardados.push(data);
        localStorage.setItem(storageKey, JSON.stringify(formulariosGuardados));
    }

    // Intenta enviar los formularios almacenados en LocalStorage cuando vuelve el internet
    async function reenviarFormulariosPendientes() {
        if (isOnline()) {
            let formulariosGuardados = JSON.parse(localStorage.getItem(storageKey)) || [];
            for (let formulario of formulariosGuardados) {
                try {
                    let response = await fetch(form.action, {
                        method: "POST",
                        headers: {
                            "Content-Type": "application/x-www-form-urlencoded",
                        },
                        body: new URLSearchParams(formulario),
                    });
                    if (response.ok) {
                        console.log("Formulario enviado exitosamente");
                    }
                } catch (error) {
                    console.error("Error al enviar formulario:", error);
                    return; 
                }
            }
            localStorage.removeItem(storageKey);
        }
    }

    // Escuchar evento de envío del formulario
    form.addEventListener("submit", function (event) {
        event.preventDefault(); // Evita el envío inmediato del formulario

        let formData = new FormData(form);
        let data = {};
        formData.forEach((value, key) => {
            data[key] = value;
        });

        if (isOnline()) {
            // Enviar el formulario si hay conexión
            fetch(form.action, {
                method: "POST",
                headers: {
                    "Content-Type": "application/x-www-form-urlencoded",
                },
                body: new URLSearchParams(data),
            })
            .then(response => {
                if (response.ok) {
                    console.log("Formulario enviado exitosamente");
                    form.reset();
                }
            })
            .catch(error => {
                console.error("Error al enviar formulario, guardando localmente:", error);
                guardarFormularioEnLocalStorage(data);
            });
        } else {
            // Guardar en LocalStorage si no hay conexión
            console.warn("Sin conexión, guardando formulario localmente");
            guardarFormularioEnLocalStorage(data);
        }
    });

    // Detecta cuando vuelve la conexión y reenvía formularios
    window.addEventListener("online", reenviarFormulariosPendientes);
    
    // Intenta reenviar formularios guardados cuando la página carga
    reenviarFormulariosPendientes();
});
