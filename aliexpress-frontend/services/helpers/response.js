// // ~/services/helpers/response.js
// export function normalizeResponse({ data, error, status }) {
//     if (error) {
//         const message =
//             error?.data?.detail ||
//             error?.message ||
//             "An unexpected error occurred"
//         const code = error?.status || status || 500

//         return {
//             data: null,
//             error: { message, code },
//             status: code,
//         }
//     }

//     return { data, error: null, status }
// }


// ~/services/helpers/response.js
export function normalizeResponse({ data, error, status }) {
    // -------------------------------
    // ❌ Error handling
    // -------------------------------
    if (error) {
        const message =
            error?.data?.message ||
            error?.message ||
            "An unexpected error occurred";
        const code = error?.status || status || 500;

        console.error("❌ API Error:", error);

        return {
            status: "error",
            success: false,
            code,
            message,
            request: error?.data?.request ?? null,
            meta: error?.data?.meta ?? null,
            errors: error?.data?.errors ?? [{ message, code }],
            data: null,
        };
    }

    // -------------------------------
    // ✅ Success response
    // -------------------------------
    console.log("API Raw Response:", data);

    const payload = data?.data ?? null;
    const meta = data?.meta ?? {};
    const errors = data?.errors ?? null;

    // Detect type: collection vs single resource
    const isArray = Array.isArray(payload);
    const isObject = payload && typeof payload === "object" && !isArray;

    console.log("Data is array?", isArray);
    console.log("Data is object?", isObject);
    console.log("Meta (pagination/info):", meta);

    return {
        status: data?.status ?? "success",
        success: data?.success ?? true,
        code: data?.code ?? status ?? 200,
        message: data?.message ?? "",
        request: data?.request ?? null,
        meta,
        errors,
        data: payload, // ✅ will be [] for collections, {} for single, null if empty
    };
}






// {
//     'status':'success',
//     'success':true,
//     'code':200,
//     'message':'fetch successfully',
//     'error':null,
//     'request'{
//         "id": "9b1d078f-480b-4883-916d-7ce827f35b09",
//         "timestamp": "2025-09-07T08:33:55.390816Z",
//         "latency_ms": 0.09,
//         "region": "Nepal-01",
//         "cache": "HIT"
//     },
//     "meta": {
//         "cursor": "first"
//     },
//     'data':
//         'products':{},
//         'pagination':{
//             "next_cursor": "cD0yMDI1LTA5LTA2KzE2JTNBMjIlM0EyOC4yMDcyOTclMkIwMCUzQTAw",
//             "has_next": true,
//             "count": 12
//         }

// }