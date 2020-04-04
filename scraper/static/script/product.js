window.onload = _ => {
    (function setupSortButtons() {
        const buttons = document.querySelectorAll("button.sort-button");
        for (const button of buttons) {
            button.onclick = _ => {
                const query = new URLSearchParams(location.search);
                query.set("sort-by", button.getAttribute("data-attr"));

                if (button.getAttribute("data-curr") === "r")
                    query.delete("reversed");
                else query.set("reversed", "");

                location.search = query.toString();
            };
        }
    })();

    (function setupFiltersDiv() {
        const filtersDiv = document.querySelector("#filters");

        document.querySelector("#filter-button")
            .onclick = _ => {
            filtersDiv.classList.toggle("show-filters");
        };

        const closeButton = filtersDiv.children[0];
        closeButton.onclick = _ => {
            filtersDiv.classList.toggle("show-filters")
        };

        const form = filtersDiv.children[1];
        form.onsubmit = e => {
            e.preventDefault();

            const x = form.children;
            const radios = document.querySelectorAll("input[type='radio']:checked");
            const sliderValues = document.querySelectorAll(".jsr_label");

            const values = {
                aut: x[1].value,
                rec: radios[0].value,
                sco: [sliderValues[0].innerText, sliderValues[1].innerText],
                conf: radios[1].value,
                isd: [x[10].children[1].value, x[10].children[2].value],
                pcd: [x[12].children[1].value, x[12].children[2].value],
                pos: [x[14].children[1].value, x[14].children[2].value],
                neg: [x[16].children[1].value, x[16].children[2].value],
                cnt: radios[2].value,
                pro: radios[3].value,
                con: radios[4].value,
            };

            const filtersQuery = [
                `aut:${values.aut}`,
                `rec:${values.rec}`,
                `sco:${values.sco[0]}-${values.sco[1]}`,
                `conf:${values.conf}`,
                `isd:${values.isd[0]}_${values.isd[1]}`,
                `pcd:${values.pcd[0]}_${values.pcd[1]}`,
                `pos:${values.pos[0]}-${values.pos[1]}`,
                `neg:${values.neg[0]}-${values.neg[1]}`,
                `cnt:${values.cnt}`,
                `pro:${values.pro}`,
                `con:${values.con}`,
            ].join(";");

            const query = new URLSearchParams(location.search);
            query.set("filters", filtersQuery);

            location.search = query.toString()
        };
    })();
};
