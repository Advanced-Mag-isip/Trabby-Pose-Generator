const BASE_URL = import.meta.env.PUBLIC_API_URL;

export async function fetchTest() {
  try {
    const res = await fetch(`${BASE_URL.replace(/\/$/, '')}/api/test/`, { mode: 'cors' });
    if (!res.ok) throw new Error(`API call failed: ${res.status} ${res.statusText}`);
    return await res.json();
  } catch (err) {
    throw err;
  }
}