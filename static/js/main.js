// Main JS file
console.log("NBA Analytics Dashboard Loaded");

// --- Team Analysis ---
async function loadTeamData() {
    const teamSelect = document.getElementById('teamSelect');
    const teamName = teamSelect.value;
    const contentDiv = document.getElementById('teamContent');

    if (!teamName) {
        contentDiv.classList.add('hidden');
        return;
    }

    try {
        const response = await fetch(`/api/team/${teamName}`);
        const data = await response.json();

        if (data.error) {
            console.error(data.error);
            return;
        }

        contentDiv.classList.remove('hidden');

        // Common Layout Options
        const commonLayout = {
            paper_bgcolor: 'rgba(0,0,0,0)',
            plot_bgcolor: 'rgba(0,0,0,0)',
            font: { color: '#f1f5f9', family: 'Inter' },
            xaxis: { gridcolor: '#334155' },
            yaxis: { gridcolor: '#334155' }
        };

        // Win Chart
        var layoutWins = { ...data.wins_chart.layout, ...commonLayout };
        layoutWins.xaxis = { ...data.wins_chart.layout.xaxis, ...commonLayout.xaxis };
        layoutWins.yaxis = { ...data.wins_chart.layout.yaxis, ...commonLayout.yaxis };

        Plotly.newPlot('winChart', data.wins_chart.data, layoutWins, { responsive: true, displayModeBar: false });

        // Points Chart
        var layoutPts = { ...data.pts_chart.layout, ...commonLayout };
        layoutPts.xaxis = { ...data.pts_chart.layout.xaxis, ...commonLayout.xaxis };
        layoutPts.yaxis = { ...data.pts_chart.layout.yaxis, ...commonLayout.yaxis };

        Plotly.newPlot('ptsChart', data.pts_chart.data, layoutPts, { responsive: true, displayModeBar: false });

        // Populate Table
        const tableBody = document.getElementById('teamStatsBody');
        const tableContainer = document.getElementById('teamStatsTable');

        if (data.season_stats && data.season_stats.length > 0) {
            tableBody.innerHTML = '';
            data.season_stats.forEach(row => {
                const tr = document.createElement('tr');
                tr.className = 'hover:bg-dark-bg/50 transition-colors';
                tr.innerHTML = `
                    <td class="p-3 font-medium text-accent-primary">${row.SEASON}</td>
                    <td class="p-3">${row.WIN}</td>
                    <td class="p-3 font-semibold text-accent-secondary">${row.WIN_PCT.toFixed(1)}%</td>
                    <td class="p-3">${row.PTS.toFixed(1)}</td>
                `;
                tableBody.appendChild(tr);
            });
            tableContainer.classList.remove('hidden');
        } else {
            tableContainer.classList.add('hidden');
        }

    } catch (error) {
        console.error('Error fetching team data:', error);
    }
}

// --- Player Insights ---
let searchTimeout;

async function searchPlayers() {
    const query = document.getElementById('playerSearch').value;
    const resultsDiv = document.getElementById('searchResults');

    if (query.length < 2) {
        resultsDiv.innerHTML = '';
        resultsDiv.classList.add('hidden');
        return;
    }

    clearTimeout(searchTimeout);
    searchTimeout = setTimeout(async () => {
        try {
            const response = await fetch(`/api/players/search?q=${query}`);
            const players = await response.json();

            if (players.length === 0) {
                resultsDiv.innerHTML = '<div class="p-4 text-dark-muted">No players found</div>';
                resultsDiv.classList.remove('hidden');
                return;
            }

            let html = '<ul class="divide-y divide-dark-border">';
            players.forEach(player => {
                html += `<li class="px-4 py-3 cursor-pointer hover:bg-dark-bg hover:text-accent-secondary transition-colors duration-200" onclick="loadPlayerData(${player.PLAYER_ID})">${player.PLAYER_NAME}</li>`;
            });
            html += '</ul>';

            resultsDiv.innerHTML = html;
            resultsDiv.classList.remove('hidden');
        } catch (error) {
            console.error('Error searching players:', error);
        }
    }, 300);
}

async function loadPlayerData(playerId) {
    const resultsDiv = document.getElementById('searchResults');
    const searchInput = document.getElementById('playerSearch');

    resultsDiv.innerHTML = '';
    resultsDiv.classList.add('hidden');
    searchInput.value = '';

    try {
        const response = await fetch(`/api/player/${playerId}`);
        const data = await response.json();

        if (data.error) {
            console.error(data.error);
            return;
        }

        document.getElementById('playerContent').classList.remove('hidden');
        document.getElementById('playerName').innerText = data.name;

        // Chart Layout
        const commonLayout = {
            paper_bgcolor: 'rgba(0,0,0,0)',
            plot_bgcolor: 'rgba(0,0,0,0)',
            font: { color: '#f1f5f9', family: 'Inter' },
            xaxis: { gridcolor: '#334155' },
            yaxis: { gridcolor: '#334155' }
        };

        var layout = { ...data.stats_chart.layout, ...commonLayout };
        layout.xaxis = { ...data.stats_chart.layout.xaxis, ...commonLayout.xaxis };
        layout.yaxis = { ...data.stats_chart.layout.yaxis, ...commonLayout.yaxis };

        Plotly.newPlot('playerChart', data.stats_chart.data, layout, { responsive: true, displayModeBar: false });

        // Populate Table
        const tableBody = document.getElementById('playerStatsBody');
        const tableContainer = document.getElementById('playerStatsTable');

        if (data.player_stats && data.player_stats.length > 0) {
            tableBody.innerHTML = '';
            data.player_stats.forEach(row => {
                const tr = document.createElement('tr');
                tr.className = 'hover:bg-dark-bg/50 transition-colors';
                tr.innerHTML = `
                    <td class="p-3 font-medium text-accent-primary">${row.SEASON}</td>
                    <td class="p-3">${row.PTS.toFixed(1)}</td>
                    <td class="p-3">${row.AST.toFixed(1)}</td>
                    <td class="p-3">${row.REB.toFixed(1)}</td>
                `;
                tableBody.appendChild(tr);
            });
            tableContainer.classList.remove('hidden');
        } else {
            tableContainer.classList.add('hidden');
        }

    } catch (error) {
        console.error('Error loading player data:', error);
    }
}

// --- Rankings ---
async function loadRankings() {
    const seasonSelect = document.getElementById('seasonSelect');
    if (!seasonSelect) return; // Guard clause if not on rankings page

    const seasonId = seasonSelect.value;

    try {
        const response = await fetch(`/api/rankings/${seasonId}`);
        const data = await response.json();

        const westBody = document.querySelector('#westTable tbody');
        const eastBody = document.querySelector('#eastTable tbody');

        westBody.innerHTML = '';
        eastBody.innerHTML = '';

        data.forEach(team => {
            const row = `
                <tr class="hover:bg-dark-bg transition-colors duration-200 group">
                    <td class="py-3 px-4 border-b border-dark-border font-medium text-white group-last:border-b-0">${team.TEAM}</td>
                    <td class="py-3 px-4 border-b border-dark-border text-dark-muted group-last:border-b-0">${team.W}</td>
                    <td class="py-3 px-4 border-b border-dark-border text-dark-muted group-last:border-b-0">${team.L}</td>
                    <td class="py-3 px-4 border-b border-dark-border font-bold text-accent-secondary group-last:border-b-0">${(team.W_PCT * 100).toFixed(1)}%</td>
                </tr>
            `;

            if (team.CONFERENCE === 'West') {
                westBody.innerHTML += row;
            } else if (team.CONFERENCE === 'East') {
                eastBody.innerHTML += row;
            }
        });

    } catch (error) {
        console.error('Error loading rankings:', error);
    }
}
