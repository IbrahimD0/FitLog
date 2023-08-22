
function scrollToCard() {
    const element = document.getElementById("cardContainer");


    element.scrollIntoView({
        behavior: "smooth",
        block: "start",
        inline: "start"
        }

    )
}

// Add a click event listener to the scroll anchor element
