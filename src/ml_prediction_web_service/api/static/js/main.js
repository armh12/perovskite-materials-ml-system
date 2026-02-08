function addRow(containerId) {
    const container = document.getElementById(containerId);
    const div = document.createElement('div');
    div.className = "flex gap-2 items-center";
    div.innerHTML = `
        <select class="element-name bg-slate-700 border-none rounded-lg text-sm w-1/2 p-2 focus:ring-2 focus:ring-blue-500">
            <option value="MA">MA</option>
            <option value="FA">FA</option>
            <option value="Cs">Cs</option>
            <option value="Rb">Rb</option>
        </select>
        <input type="number" step="0.01" value="1.0" class="element-frac bg-slate-700 border-none rounded-lg text-sm w-1/4 p-2 focus:ring-2 focus:ring-blue-500">
        <button onclick="this.parentElement.remove()" class="text-slate-500 hover:text-red-400 px-2">×</button>
    `;
    container.appendChild(div);
}

addRow('a-site-list');

document.getElementById('predict-btn').addEventListener('click', async () => {
    const aSiteRows = document.querySelectorAll('#a-site-list > div');
    const a_site = Array.from(aSiteRows).map(row => ({
        name: row.querySelector('.element-name').value,
        frequence: parseFloat(row.querySelector('.element-frac').value)
    }));

    const payload = {
        perovskite_composition: {
            A_site: a_site,
            B_site: [{ name: "Pb", frequence: 1.0 }],
            C_site: [{ name: "I", frequence: 1.0 }]
        },
        inorganic_composition: false,
        dimension_list_of_layers: 3.0,
        dimension: "3D",
        space_group: "Pm3m"
    };

    try {
        const response = await fetch('/prediction/band_gap', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });
        const data = await response.json();
        
        document.getElementById('result-card').classList.remove('hidden');
        document.getElementById('prediction-value').innerText = data.toFixed(3);
    } catch (err) {
        alert("Prediction failed. Check console for details.");
        console.error(err);
    }
});