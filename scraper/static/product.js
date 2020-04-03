window.onload = _ => {
    setupSortButtons();
};

function setupSortButtons() {
    const buttons = document.querySelectorAll("button.sort-button");
    for (const button of buttons) {
        button.onclick = _ => {
            const query = new URLSearchParams(location.search);
            query.set("sort-by", button.getAttribute("data-attr"));

            if (button.getAttribute("data-curr") === "r")
                query.delete("reversed");
            else query.set("reversed", "");

            location.search = query.toString();
        }
    }
}
