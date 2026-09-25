function token() {

    return (
        localStorage.getItem("token")
        || ""
    );

}


async function api(
    url,
    options = {}
) {

    const headers =
        new Headers(
            options.headers || {}
        );


    const currentToken =
        token();


    if (currentToken) {

        headers.set(
            "Authorization",
            "Bearer " + currentToken
        );

    }


    if (
        !(options.body instanceof FormData)
        &&
        options.body
        &&
        !headers.has("Content-Type")
    ) {

        headers.set(
            "Content-Type",
            "application/json"
        );

    }


    try {

        const response =
            await fetch(
                url,
                {
                    ...options,
                    headers
                }
            );


        let data = {};


        try {

            data =
                await response.json();

        } catch {

            data = {};

        }


        return {

            ok:
                response.ok,

            status:
                response.status,

            data

        };

    } catch {

        return {

            ok: false,

            status: 0,

            data: {
                detail:
                    "Cannot connect to server"
            }

        };

    }

}


function showMessage(
    message,
    error = false
) {

    const element =
        document.getElementById(
            "message"
        );


    if (!element) {
        return;
    }


    element.textContent =
        message;


    element.style.color =
        error
        ? "#c0392b"
        : "#2e7d32";

}


function escapeHtml(
    value
) {

    return String(
        value ?? ""
    ).replace(
        /[&<>"']/g,
        character => ({

            "&": "&amp;",

            "<": "&lt;",

            ">": "&gt;",

            '"': "&quot;",

            "'": "&#039;"

        }[character])
    );

}


(function () {

    const login =
        document.getElementById(
            "loginLink"
        );


    const logout =
        document.getElementById(
            "logoutBtn"
        );


    if (token()) {

        if (login) {

            login.classList.add(
                "hidden"
            );

        }


        if (logout) {

            logout.classList.remove(
                "hidden"
            );


            logout.onclick =
                () => {

                    localStorage.removeItem(
                        "token"
                    );

                    location.href =
                        "/";

                };

        }

    }

})();