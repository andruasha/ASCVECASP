document.addEventListener("DOMContentLoaded", () => {
    const themeSelect = document.getElementById("lab-theme");
    const filterTypeSelect = document.getElementById("filter-type");
    const schemeTypeSelect = document.getElementById("scheme-type");

    const filterToSchemes = {
        LPF: ["G", "P", "T"],
        HPF: ["G", "P", "T"],
        BPF: ["G", "P", "T"],
        BSF: ["T", "T_back_coupling"]
    };

    const elementMappings = {
        active_dipole: ["nodes-num", "branches-num", "voltage-sources-num", "current-sources-num", "resistors-num"],
        coupling_coefficient: ["nodes-num", "branches-num", "voltage-sources-num", "current-sources-num", "resistors-num"],
        direct_current: ["nodes-num", "branches-num", "voltage-sources-num", "current-sources-num", "resistors-num"],
        alternating_current: ["nodes-num", "branches-num", "voltage-sources-num", "current-sources-num", "resistors-num", "capacitors-num", "inductors-num"],
        transient_processes: ["nodes-num", "branches-num", "voltage-sources-num", "current-sources-num", "resistors-num", "capacitors-num", "inductors-num"],
        active_quadripole: ["scheme-type", "resistors-num", "capacitors-num", "inductors-num"],
        filter: ["filter-type", "scheme-type"],
    };

    const allElements = [
        "nodes-num",
        "branches-num",
        "voltage-sources-num",
        "current-sources-num",
        "resistors-num",
        "capacitors-num",
        "inductors-num",
        "scheme-type",
        "filter-type"
    ];

    function updateVisibleElements() {
        const selectedTheme = themeSelect.value;
        const visibleElements = elementMappings[selectedTheme] || [];

        allElements.forEach(id => {
            const wrapper = document.getElementById(`${id}-wrapper`);
            if (wrapper) {
                wrapper.style.display = visibleElements.includes(id) ? "block" : "none";
            }
        });

        if (selectedTheme === "filter") {
            updateSchemeOptions(filterTypeSelect.value);
        }
    }

    function updateSchemeOptions(filterType) {
        const schemes = filterToSchemes[filterType] || [];
        schemeTypeSelect.innerHTML = "";

        schemes.forEach(scheme => {
            const option = document.createElement("option");
            option.value = scheme;
            option.textContent = scheme;
            schemeTypeSelect.appendChild(option);
        });
    }

    themeSelect.addEventListener("change", updateVisibleElements);
    filterTypeSelect.addEventListener("change", () => {
        if (themeSelect.value === "filter") {
            updateSchemeOptions(filterTypeSelect.value);
        }
    });

    updateVisibleElements();
});

async function submitData() {
    const labTheme = document.getElementById("lab-theme").value;

    const getValue = (id) => {
        const el = document.getElementById(id);
        return el && el.offsetParent !== null ? el.value : null;
    };

    const data = {
        labTheme,
        nodesNum: parseInt(getValue("nodes-num")) || 0,
        branchesNum: parseInt(getValue("branches-num")) || 0,
        voltageSources: parseInt(getValue("voltage-sources-num")) || 0,
        currentSources: parseInt(getValue("current-sources-num")) || 0,
        resistors: parseInt(getValue("resistors-num")) || 0,
        capacitors: parseInt(getValue("capacitors-num")) || 0,
        inductors: parseInt(getValue("inductors-num")) || 0,
        filterType: getValue("filter-type"),
        schemeType: getValue("scheme-type")
    };

    const response = await eel.generate_schemes_set(
        data.labTheme,
        data.nodesNum,
        data.branchesNum,
        data.voltageSources,
        data.currentSources,
        data.resistors,
        data.capacitors,
        data.inductors,
        data.filterType,
        data.schemeType
    )();
}
