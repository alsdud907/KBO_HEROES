document.addEventListener('DOMContentLoaded', () => {
    let appData = null;
    let pitcherChart = null;
    let hitterChart = null;

    // Elements
    const pitcherSection = document.getElementById('pitcher-section');
    const hitterSection = document.getElementById('hitter-section');
    const btnPitchers = document.getElementById('btn-pitchers');
    const btnHitter = document.getElementById('btn-hitter');
    const yearSelect = document.getElementById('year-select');
    const statSelect = document.getElementById('stat-select');
    const lastUpdateSpan = document.getElementById('last-update');

    const teamColors = {
        '키움': '#820024',
        '삼성': '#074CA1',
        '롯데': '#041E42',
        'NC': '#072241',
        'KIA': '#C70125',
        '한화': '#FF6600',
        'KT': '#000000',
        '두산': '#131230',
        'LG': '#C30452'
    };

    const playerColors = {
        '박세웅': '#87CEEB',
        '구창모': '#3E5B81',
        '임찬규': '#FDFD96',
        '곽빈': '#FF9999'
    };

    const benchmarks = {
        'ERA': { top: 3.50, mid: 4.55, low: 5.50, inverse: true },
        'WHIP': { top: 1.20, mid: 1.42, low: 1.65, inverse: true },
        'IP_val': { top: 170, mid: 144, low: 100, inverse: false },
        'WPCT': { top: 0.650, mid: 0.500, low: 0.400, inverse: false },
        'BB/9': { top: 2.50, mid: 3.75, low: 5.00, inverse: true },
        'K/9': { top: 9.00, mid: 7.00, low: 5.00, inverse: false },
        'K/BB': { top: 3.50, mid: 2.25, low: 1.50, inverse: false },
        'HR/9': { top: 0.70, mid: 1.10, low: 1.50, inverse: true }
    };

    // Initialize App
    async function init() {
        try {
            const response = await fetch('data/players_data.json');
            appData = await response.json();
            
            lastUpdateSpan.textContent = new Date(appData.updated_at).toLocaleString('ko-KR');
            
            updatePitcherTable();
            renderPitcherChart();
            setupHitterView();

            // Event Listeners
            yearSelect.addEventListener('change', () => {
                updatePitcherTable();
                renderPitcherChart();
            });
            statSelect.addEventListener('change', renderPitcherChart);

            btnPitchers.addEventListener('click', () => {
                pitcherSection.classList.remove('hidden');
                hitterSection.classList.add('hidden');
                btnPitchers.classList.add('active');
                btnHitter.classList.remove('active');
            });

            btnHitter.addEventListener('click', () => {
                hitterSection.classList.remove('hidden');
                pitcherSection.classList.add('hidden');
                btnHitter.classList.add('active');
                btnPitchers.classList.remove('active');
            });

        } catch (err) {
            console.error('Failed to load KBO data:', err);
        }
    }

    // --- Pitcher Logic ---
    function updatePitcherTable() {
        const year = yearSelect.value;
        const tbody = document.querySelector('#pitcher-table tbody');
        tbody.innerHTML = '';

        const yearData = appData.pitchers.map(p => {
            const stats = p.stats.find(s => s.연도 === year);
            return {
                name: p.name,
                team: p.team,
                stats: stats || null
            };
        }).filter(p => p.stats !== null);

        // Sort by ERA
        yearData.sort((a, b) => parseFloat(a.stats.ERA) - parseFloat(b.stats.ERA));

        yearData.forEach((p, index) => {
            const tr = document.createElement('tr');
            const pColor = playerColors[p.name] || teamColors[p.team] || 'var(--accent-blue)';
            
            tr.innerHTML = `
                <td>${index + 1}</td>
                <td><strong>${p.name}</strong></td>
                <td>${p.team}</td>
                <td>${p.stats.G}</td>
                <td style="color: var(--accent-blue); font-weight: bold;">${p.stats.ERA}</td>
                <td>${p.stats.WHIP || '-'}</td>
                <td>${p.stats.W}-${p.stats.L}</td>
                <td>${p.stats.WPCT}</td>
                <td>${p.stats.IP}</td>
                <td>${p.stats.SO}</td>
                <td>${p.stats.H}/${p.stats.HR}</td>
                <td>${p.stats.BB}/${p.stats.HBP}</td>
                <td>${p.stats.R}/${p.stats.ER}</td>
            `;
            tbody.appendChild(tr);
        });
    }

    function renderPitcherChart() {
        const year = yearSelect.value;
        const metric = statSelect.value;
        const ctx = document.getElementById('pitcherChart').getContext('2d');

        const yearData = appData.pitchers.map(p => {
            const stats = p.stats.find(s => s.연도 === year);
            return { 
                name: p.name, 
                team: p.team,
                value: stats ? parseFloat(stats[metric]) : 0 
            };
        }).filter(p => p.value > 0);

        if (pitcherChart) pitcherChart.destroy();

        const bm = benchmarks[metric];
        const annotations = {};
        
        if (bm) {
            annotations.line1 = { type: 'line', yMin: bm.top, yMax: bm.top, borderColor: '#2ecc71', borderWidth: 2, borderDash: [6, 6], label: { display: true, content: 'Top', position: 'end', backgroundColor: '#2ecc71', color: '#fff' } };
            annotations.line2 = { type: 'line', yMin: bm.mid, yMax: bm.mid, borderColor: '#f1c40f', borderWidth: 2, borderDash: [6, 6], label: { display: true, content: 'Avg', position: 'end', backgroundColor: '#f1c40f', color: '#000' } };
            annotations.line3 = { type: 'line', yMin: bm.low, yMax: bm.low, borderColor: '#e74c3c', borderWidth: 2, borderDash: [6, 6], label: { display: true, content: 'Low', position: 'end', backgroundColor: '#e74c3c', color: '#fff' } };
        }

        pitcherChart = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: yearData.map(d => d.name),
                datasets: [{
                    label: statSelect.options[statSelect.selectedIndex].text,
                    data: yearData.map(d => d.value),
                    backgroundColor: yearData.map(d => playerColors[d.name] || teamColors[d.team] || 'rgba(55, 112, 191, 0.7)'),
                    borderColor: yearData.map(d => playerColors[d.name] || teamColors[d.team] || 'rgba(55, 112, 191, 1)'),
                    borderWidth: 1,
                    borderRadius: 8
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    annotation: { annotations }
                },
                scales: {
                    y: { 
                        beginAtZero: true
                    }
                }
            }
        });
    }

    // --- Hitter Logic ---
    function setupHitterView() {
        const hitter = appData.hitters[0];
        document.getElementById('hitter-name').textContent = hitter.name;
        document.getElementById('hitter-team').textContent = hitter.team;

        const latestStats = hitter.stats[hitter.stats.length - 1];
        if (latestStats) {
            document.getElementById('current-avg').textContent = latestStats.AVG;
            document.getElementById('current-hr').textContent = latestStats.HR;
            document.getElementById('current-rbi').textContent = latestStats.RBI;
        }

        const tbody = document.querySelector('#hitter-table tbody');
        tbody.innerHTML = '';
        hitter.stats.forEach(s => {
            const tr = document.createElement('tr');
            const ops = (parseFloat(s.SLG) + parseFloat(s.OBP)).toFixed(3);
            tr.innerHTML = `
                <td>${s.연도}</td>
                <td style="font-weight: bold;">${s.AVG}</td>
                <td>${s.G}</td>
                <td>${s.H}</td>
                <td>${s.HR}</td>
                <td>${s.RBI}</td>
                <td style="color: var(--accent-blue);">${isNaN(ops) ? '-' : ops}</td>
            `;
            tbody.appendChild(tr);
        });
    }

    init();
});
