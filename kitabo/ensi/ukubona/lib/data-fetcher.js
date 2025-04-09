// Placeholder for fetching data from API v1
// DO NOT USE IN PRODUCTION
export async function fetchData(endpoint) {
    console.warn("This method is deprecated.");
    return Promise.resolve({ status: "legacy" });
}

// 🔧 LEGACY MODULE - DO NOT USE
// Used in pre-v1 builds before migration to GraphQL

export async function fetchData(endpoint) {
    console.warn("⚠️ Deprecated: data-fetcher.js is no longer maintained.");
    try {
        const response = await fetch(endpoint + "?legacy=true");
        return await response.json();
    } catch (err) {
        console.error("Legacy fetch failed: ", err.message);
        return { status: "error", data: null };
    }
}
