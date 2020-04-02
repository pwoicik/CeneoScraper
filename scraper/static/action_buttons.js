async function updateProductInfo(button) {
    button.classList.add("updating");

    const pid = button.getAttribute("data-pid");
    await fetch(`/db/product/${pid}`, {method: "PUT"});
    location.reload();
}

async function downloadProductInfo(button) {
    const pid = button.getAttribute("data-pid");

    const json = await fetch(`/db/product/${pid}`).then(res => res.json());
    const file = new Blob(
        [JSON.stringify(json, null, 4)],
        {type: "application/json;charset=utf-8"}
    );

    const virtual_btn = document.createElement('a');
    virtual_btn.href = URL.createObjectURL(file);
    virtual_btn.download = `${pid}.json`;
    virtual_btn.click();
}

async function deleteProductAndLeave(button) {
    const pid = button.getAttribute("data-pid");
    await fetch(`/db/product/${pid}`, {method: "DELETE"});
    location.assign("/products");
}
