// import { ref, onMounted, onBeforeUnmount, nextTick } from "vue";
// import { useProductStore } from "~/stores/modules/productStore";
// import { useObserverCore } from "../observer/useObserverCore";
// import { useFillViewport } from "~/composable/pagination/useFillViewport";

// export function useInfiniteProducts(opts = {}) {
//     const productStore = useProductStore();

//     const products = productStore.products;
//     const hasNext = ref(true);
//     const isLoading = productStore.loading;
//     const error = productStore.error;

//     const core = useObserverCore({ debug: !!opts.debug });
//     const sentinelRef = ref(null);
//     const isObserving = ref(false);

//     let destroyed = false;

//     async function safeLoad() {
//         if (destroyed || isLoading.value) return false;

//         const page = products.value.length / (opts.pageSize ?? 12) + 1;
//         await productStore.fetchProducts({ page });

//         if (!productStore.pagination.next) {
//             core.unobserve(sentinelRef.value);
//             hasNext.value = false;
//         }
//         return hasNext.value;
//     }

//     const onEntry = async (entry) => {
//         if (entry?.isIntersecting && opts.prefetch !== false) {
//             try {
//                 await safeLoad();
//             } catch {
//                 /* silent */
//             }
//         }
//     };

//     function bindSentinel(nodeOrRef) {
//         const node = nodeOrRef?.value || nodeOrRef;
//         if (!node) return;

//         if (sentinelRef.value && sentinelRef.value !== node) {
//             core.unobserve(sentinelRef.value);
//         }
//         sentinelRef.value = node;

//         core.observe(node, onEntry, {
//             threshold: opts.threshold ?? 0.1,
//             root: opts.root ?? null,
//             rootMargin: opts.rootMargin ?? "0px",
//         });
//         isObserving.value = true;
//     }

//     function unbindSentinel() {
//         if (sentinelRef.value) core.unobserve(sentinelRef.value);
//         sentinelRef.value = null;
//         isObserving.value = false;
//     }

//     const { checkAndLoadUntilScrollable } = useFillViewport(safeLoad, hasNext, {
//         maxLoops: opts.maxFillLoops ?? 20,
//         debug: !!opts.debug,
//     });

//     onMounted(() => {
//         if (sentinelRef.value) core.observe(sentinelRef.value, onEntry);
//         nextTick(checkAndLoadUntilScrollable);
//     });

//     onBeforeUnmount(() => {
//         destroyed = true;
//         unbindSentinel();
//         core.stop();
//     });

//     return {
//         products,
//         hasNext,
//         isLoading,
//         error,
//         sentinelRef,
//         bindSentinel,
//         unbindSentinel,
//     };
// }

import { ref, onMounted, onBeforeUnmount, nextTick } from "vue";
import { useProductStore } from "~/stores/modules/productStore";
import { useObserverCore } from "../observer/useObserverCore";
// import { useFillViewport } from "~/composables/pagination/useFillViewport";
import { useFillViewport } from "../pagination/useFillViewport";

export function useInfiniteProductScroll(opts = {}) {
    const productStore = useProductStore();

    const products = productStore.products;
    const hasNext = ref(true);
    const isLoading = productStore.loading;
    const error = productStore.error;

    const core = useObserverCore({ debug: !!opts.debug });
    const sentinelRef = ref(null);
    const isObserving = ref(false);

    let destroyed = false;

    async function safeLoad() {
        if (destroyed || isLoading.value) return false;

        // prefer pagination.next over page calculation
        const nextPage = productStore.pagination?.nextPage ?? (
            Math.floor(products.value.length / (opts.pageSize ?? 12)) + 1
        );

        await productStore.fetchProducts({ page: nextPage });

        if (!productStore.pagination?.next) {
            core.unobserve(sentinelRef.value);
            hasNext.value = false;
        }
        return hasNext.value;
    }

    const onEntry = async (entry) => {
        if (entry?.isIntersecting && opts.prefetch !== false) {
            try {
                await safeLoad();
            } catch {
                /* silent */
            }
        }
    };

    function bindSentinel(nodeOrRef) {
        const node = nodeOrRef?.value || nodeOrRef;
        if (!node) return;

        if (sentinelRef.value && sentinelRef.value !== node) {
            core.unobserve(sentinelRef.value);
        }
        sentinelRef.value = node;

        core.observe(node, onEntry, {
            threshold: opts.threshold ?? 0.1,
            root: opts.root ?? null,
            rootMargin: opts.rootMargin ?? "0px",
        });
        isObserving.value = true;
    }

    function unbindSentinel() {
        if (sentinelRef.value) core.unobserve(sentinelRef.value);
        sentinelRef.value = null;
        isObserving.value = false;
    }

    const { checkAndLoadUntilScrollable } = useFillViewport(safeLoad, hasNext, {
        maxLoops: opts.maxFillLoops ?? 20,
        debug: !!opts.debug,
    });

    onMounted(async () => {
        // always load first page
        if (!products.value.length) {
            await safeLoad();
        }
        if (sentinelRef.value) {
            core.observe(sentinelRef.value, onEntry);
        }
        nextTick(checkAndLoadUntilScrollable);
    });

    onBeforeUnmount(() => {
        destroyed = true;
        unbindSentinel();
        core.stop();
    });

    return {
        products,
        hasNext,
        isLoading,
        error,
        sentinelRef,
        bindSentinel,
        unbindSentinel,
    };
}
