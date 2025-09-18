# 📚 4-Week Learning & Building Plan (AliExpress Clone)

Welcome!  
This plan is designed to help you **learn JavaScript, Vue/Nuxt 3, and DRF API integration step by step**, while building your AliExpress clone project.  
Each week mixes **theory + coding tasks** so you don’t just study — you apply everything directly.

---

## 🗓️ Week 1 — JavaScript & Vue Basics

### 🎯 Goals
- Get comfortable with **JavaScript fundamentals**
- Learn **Vue 3 reactivity** (ref, reactive, computed)
- Build confidence reading and modifying existing code

### 📖 Learn
- JavaScript:
  - Variables (`let`, `const`)
  - Functions + Arrow functions
  - Arrays (`map`, `filter`, `reduce`)
  - Objects + `Map`/`Set`
  - Async/Await
- Vue:
  - `ref`, `reactive`, `computed`
  - Template syntax (`v-for`, `v-if`, `v-model`)

### 🛠️ Practice Tasks
1. Write a small script that:
   - Deduplicates an array of objects by `id` (like we used in pagination).
   - Fetches data from a dummy API (`fetch("https://jsonplaceholder.typicode.com/posts")`).
2. In Nuxt 3:
   - Create a **Counter Component** using `ref` + `computed`.
   - Render a list of products with `v-for`.

---

## 🗓️ Week 2 — State & API Integration

### 🎯 Goals
- Learn **Pinia store** & **Nuxt composables**
- Fetch data from **DRF API** and display it
- Understand pagination basics (offset vs cursor)

### 📖 Learn
- Pinia basics (`defineStore`, `ref`, actions)
- Composables (`useSomething.js`)
- DRF Pagination:
  - `next_cursor`, `has_next`
  - `count` (if available)

### 🛠️ Practice Tasks
1. Build a **ProductStore** in Pinia:
   - `products`, `loading`, `error`
   - `fetchFirst`, `loadMore`, `reset`
2. Move the same logic into a **composable** (`usePagination`).
3. Call your real DRF endpoint, show products on the page.

---

## 🗓️ Week 3 — Advanced Vue & Project Features

### 🎯 Goals
- Get comfortable with **reusable composables**
- Add **filters, sorting, infinite scroll**
- Use **TypeScript** for better safety

### 📖 Learn
- Vue lifecycle hooks (`onMounted`, `onBeforeUnmount`)
- Watchers (`watch`, `watchEffect`)
- TypeScript basics:
  - Interfaces
  - Typing API responses

### 🛠️ Practice Tasks
1. Extend `usePagination`:
   - Add filters (category, price range).
   - Add infinite scroll (trigger `loadMore` when near bottom).
2. Convert composable to TypeScript (`usePagination.ts`).
3. Add a **Product Filters Component** in Nuxt.

---

## 🗓️ Week 4 — Full Feature & Cleanup

### 🎯 Goals
- Build a **working AliExpress-style product listing**
- Learn debugging + clean code practices
- Deploy your app locally

### 📖 Learn
- Error handling (`try/catch`, `console.error`)
- Aborting requests (already in `_request`)
- Deployment basics (Nuxt build, serve)

### 🛠️ Practice Tasks
1. Build full **Product Listing Page**:
   - Pagination
   - Filters
   - Load more button / Infinite scroll
2. Add a **Cart Store** in Pinia:
   - `addToCart`, `removeFromCart`, `cartTotal`
3. Deploy locally with `npm run build && npm run preview`.

---

## 🔑 Daily Routine (Recommended)
- ⏰ 1–2 hours learning (JS + Vue docs + small experiments).
- 💻 2–3 hours coding on your clone project.
- 📝 End of day: write down **what you understood + what blocked you**.

---

## 📌 Final Notes
- If you get stuck >6 hours → **ask for help** (don’t wait 15 days).
- Use `console.log` *a lot* — debugging is half the job.
- Don’t try to “learn everything” — focus only on **what unblocks your project**.
- By the end of 4 weeks → you’ll have:
  - Solid JS + Vue skills
  - A reusable pagination system
  - A working AliExpress-style frontend with DRF backend

---
