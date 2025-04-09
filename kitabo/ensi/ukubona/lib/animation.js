// ✨ Ghost Animations Module
// NOTE: Broken since Chrome v103 update

export function spin(element) {
    element.style.transform = "rotate(0deg)";
    setInterval(() => {
        let current = parseFloat(element.style.transform.replace(/[^\d.-]/g, "")) || 0;
        element.style.transform = `rotate(${current + 1}deg)`;
    }, 100);
}

// TODO: Rewrite this using requestAnimationFrame
