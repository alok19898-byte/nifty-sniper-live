// Live Time Logic
function updateLiveTime() {
    const now = new Date();
    document.getElementById('liveTime').innerText = "Live Time: " + now.toLocaleTimeString('en-IN', { hour12: true });
}
setInterval(updateLiveTime, 1000);
updateLiveTime();

// 100% PERFECT HIGHLIGHT & PERCENTAGE LOGIC
function applyPercentages() {
    // Columns list - Call and Put sides processed separately
    const columns = ['val-call-oi', 'val-call-vol', 'val-call-oichg', 'val-put-oi', 'val-put-vol', 'val-put-oichg'];
    
    columns.forEach(cls => {
        let cells = document.querySelectorAll('.' + cls);
        let maxVal = -Infinity;
        
        // Step 1: Find Max Value safely
        cells.forEach(cell => {
            // Extract just the number (ignores any span added previously)
            let text = cell.innerText.split('\n')[0].replace(/,/g, '').trim();
            let val = parseFloat(text);
            if (!isNaN(val) && val > maxVal) { maxVal = val; }
        });
        
        // Step 2: Apply Highlight and Percentage safely without breaking HTML
        cells.forEach(cell => {
            let originalNumber = cell.innerText.split('\n')[0].trim();
            let val = parseFloat(originalNumber.replace(/,/g, ''));
            
            if (!isNaN(val)) {
                let pct = (maxVal > 0) ? Math.round((Math.abs(val) / maxVal) * 100) : 0;
                
                if (val === maxVal && maxVal > 0) {
                    cell.classList.add('max-highlight');
                    cell.innerHTML = originalNumber + <span class="pct-box pct-100">(100%)</span>;
                } else {
                    cell.innerHTML = originalNumber + <span class="pct-box">(${pct}%)</span>;
                }
            }
        });
    });
}
// Run as soon as page loads
window.onload = applyPercentages;

// Toggle Menus (Settings & Greeks)
function toggleMenu(menuId) {
    document.getElementById(menuId).classList.toggle("show-menu");
}

window.onclick = function(event) {
    if (!event.target.matches('.dropdown-btn') && !event.target.closest('.dropdown-check-list')) {
        let dropdowns = document.getElementsByClassName("dropdown-content");
        for (let i = 0; i < dropdowns.length; i++) {
            if (dropdowns[i].classList.contains('show-menu')) {
                dropdowns[i].classList.remove('show-menu');
            }
        }
    }
}

// Mode Switcher (Live / Historical Speed Control Fixed)
function switchMode(mode) {
    let speedCtrl = document.getElementById("speedControl");
    if (mode === 'historical') {
        speedCtrl.style.display = "inline-block"; // Shows the speed dropdown properly
        alert("Switched to Historical Mode.");
    } else {
        speedCtrl.style.display = "none"; // Hides it back on Live
        alert("Switched to Live Mode.");
    }
}

function changeSpeed() {
    alert("Playback speed set to: " + document.getElementById("speedControl").value + "x");
}

function logoutApp() {
    if (confirm("Are you sure you want to logout?")) { 
        alert("Logging out successfully..."); 
    }
}

// Greeks Toggle Logic (Fixed Colspan)
let greeksCount = 0;
function toggleCol(greekClass) {
    let checkbox = event.target;
    let cols = document.querySelectorAll('.col-' + greekClass);
    if (checkbox.checked) {
        cols.forEach(col => col.classList.remove('hidden-col'));
        greeksCount++;
    } else {
        cols.forEach(col => col.classList.add('hidden-col'));
        greeksCount--;
    }
    // Safely adjusts the main headers when Greeks are opened
    document.getElementById("callHeader").colSpan = 4 + greeksCount;
    document.getElementById("putHeader").colSpan = 4 + greeksCount;
}

function switchIndex() {
    alert("Switched Data to: " + document.getElementById("indexSelect").value);
}
