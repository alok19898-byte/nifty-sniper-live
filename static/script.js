async function fetchLiveChain() {
    try {
        const response = await fetch('/api/option-chain');
        const data = await response.json();
        
        if (data.error) {
            console.error("API Error:", data.error);
            return;
        }

        // यहाँ 'data.data' वो है जो Python से आ रहा है
        // अब रैंडम डेटा की जगह API वाला data.data यूज़ होगा
        console.log("Real Data Received:", data);
        
        // अब तुझे बस इस डेटा को टेबल के सेल्स (td) में मैप करना है
        // जैसे: document.getElementById('price').innerText = data.spot_price;
        
    } catch (error) {
        console.error("Fetch failed:", error);
    }
}

setInterval(fetchLiveChain, 5000);
fetchLiveChain();
