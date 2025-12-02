// plugins/fetch-retry.js
export default defineNuxtPlugin((nuxtApp) => {
    // Helper: wait with ms
    function wait(ms) {
        return new Promise((resolve) => setTimeout(resolve, ms));
    }

    // Wrap the global $fetch
    const customFetch = async (request, options = {}) => {
        const maxRetries = options.retries ?? 3;
        const retryDelay = options.retryDelay ?? 500; // start delay
        const retryBackoff = options.retryBackoff ?? 2; // exponential multiplier

        let attempt = 0;
        let delay = retryDelay;

        while (attempt <= maxRetries) {
            try {
                return await $fetch(request, options);
            } catch (err) {
                const status = err?.response?.status;

                // Retry only for network/server errors
                if (status >= 500 || !status) {
                    attempt++;
                    if (attempt > maxRetries) throw err;

                    console.warn(
                        `[fetch-retry] Retry ${attempt}/${maxRetries} after ${delay}ms...`,
                        request
                    );
                    await wait(delay);
                    delay *= retryBackoff; // exponential backoff
                    continue;
                }

                // Don’t retry client-side errors (400, 403, 404 etc.)
                throw err;
            }
        }
    };

    // Expose as global $fetch
    nuxtApp.provide("fetch", customFetch);
});
