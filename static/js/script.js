
// Automatically close flash messages
document.addEventListener("DOMContentLoaded", function () {

    const alerts = document.querySelectorAll(".alert");

    alerts.forEach(function (alert) {
        setTimeout(function () {
            const closeButton = alert.querySelector(".btn-close");

            if (closeButton) {
                closeButton.click();
            }
        }, 4000);
    });

});
